
# Walkthrough for Using the Code

This walkthrough will guide you through the steps required to use the provided code for identifying potential customers using historical audience interaction data. The code performs data preprocessing, feature engineering, model training, and evaluation.

## Prerequisites

Ensure you have the following packages installed in your Python environment:

- dask
- pandas
- numpy
- scikit-learn
- mlxtend

You can install them using pip:

sh
pip install dask pandas numpy scikit-learn mlxtend


## Step 1: Data Preprocessing

### 1.1 Load the CSV file with specified dtypes

The first step is to load the data using Dask to handle large datasets efficiently.

```py
import dask.dataframe as dd

df = dd.read_csv(r'C:\Users\sonav\Downloads\Compressed\dreamskrin\train_data_ads.csv', dtype={
    'ad_close_list_v001': 'object', 
    'ad_close_list_v002': 'object', 
    'ad_close_list_v003': 'object'
})
```



### 1.2 Sample 20% of the data

Next, we take a 20% sample of the dataset for faster processing.

```py
df = df.sample(frac=0.2, random_state=8)
```

### 1.3 Drop specified columns

We drop unnecessary columns to reduce the dataset's complexity.

```py
df = df.drop(['ad_click_list_v001', 'ad_click_list_v002', 'ad_click_list_v003', 'log_id', 'user_id', 'ad_close_list_v001', 'ad_close_list_v002', 'ad_close_list_v003'], axis=1)
```

### 1.4 Separate positive and negative labels

Separate the dataset into positive and negative labels based on the 'label' column.

```py
pos = df[df['label'] == 1]
neg = df[df['label'] == 0]

pos = pos.compute()
neg = neg.compute()
```

### 1.5 Further sample the dataframes to reduce size

Sample 65% of both positive and negative dataframes.

```py
pos = pos.sample(frac=0.65, random_state=8)
neg = neg.sample(frac=0.65, random_state=8)
```



### 1.6 Apply transformation to 'u_newsCatInterestsST' column

Transform the 'u_newsCatInterestsST' column to binary values.

```py
neg['u_newsCatInterestsST'] = neg['u_newsCatInterestsST'].apply(lambda row: 1 if '0' in row.split('^') else 0)
pos['u_newsCatInterestsST'] = pos['u_newsCatInterestsST'].apply(lambda row: 1 if '0' in row.split('^') else 0)
```

### 1.7 Save the dataframes to CSV files

Save the processed dataframes to CSV files for future use.

```py
neg.to_csv('./data/final_neg.csv', index=False)
pos.to_csv('./data/final_pos.csv', index=False)
```

## Step 2: Model Training and Evaluation

### 2.1 Load the processed data

Load the processed positive and negative data.

```py
import numpy as np
import pandas as pd
import dask.dataframe as dd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier, VotingClassifier
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

pos_data = pd.read_csv('./data/final_pos.csv')
neg_data = pd.read_csv('./data/final_neg.csv')
```

### 2.2 Merge and shuffle the data

Combine the positive and negative samples and shuffle the dataset.

```py
merge_data = pd.concat([pos_data.sample(n=8000, random_state=10), neg_data.sample(n=8000, random_state=10)])
merge_data = merge_data.sample(frac=1, random_state=10).reset_index(drop=True)
```

### 2.3 Split the data into training and testing sets

Split the data into training and testing sets.

```py
X = merge_data.drop(['label'], axis=1)
y = merge_data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
```

### 2.4 Initialize and train the model

Initialize the classifiers and the voting classifier, then fit the Sequential Feature Selector (SFS) to find the best features.

```py
rf = RandomForestClassifier()
gbm = GradientBoostingClassifier()
hgbm = HistGradientBoostingClassifier()
vclf = VotingClassifier(estimators=[('rf', rf), ('gbm', gbm), ('hgbm', hgbm)], voting='hard')

sfs = SFS(vclf, k_features='parsimonious', forward=True, floating=False, scoring='accuracy', cv=10)
sfs.fit(X_train, y_train)
features = list(sfs.k_feature_names_)
```

### 2.5 Train the model with selected features

Train the voting classifier with the selected features.

```py
vclf.fit(X_train[features], y_train)
```


### 2.6 Make predictions and evaluate the model

Make predictions on the test set and evaluate the model using accuracy and classification report.

```py
pred = vclf.predict(X_test[features])

print("Accuracy: ", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
```


This completes the walkthrough for using the code. By following these steps, you can preprocess your data, train the model, and evaluate its performance.