import numpy as np
import pandas as pd
import dask.dataframe as dd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier, VotingClassifier
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

pos_data = pd.read_csv('final_pos.csv')
neg_data = pd.read_csv('final_neg.csv')
merge_data = pd.concat([pos_data.sample(n = 8000, random_state=10), neg_data.sample(n = 8000, random_state=10)])
merge_data = merge_data.sample(frac = 1, random_state=10).reset_index(drop = True)
print("Data merged")

X = merge_data.drop(['label'], axis=1)
y = merge_data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
print(f'Data split into training and testing sets: \n\tTraining set: {X_train.shape} \n\tTesting set: {X_test.shape}')

rf = RandomForestClassifier()
gbm = GradientBoostingClassifier()
hgbm = HistGradientBoostingClassifier()
vclf = VotingClassifier(estimators=[
    ('rf', rf), ('gbm', gbm), ('hgbm', hgbm)], voting='hard')
print('Model: ', vclf, sep='\n')

sfs = SFS(vclf, k_features = 'parsimonious', forward = True, floating = False, scoring = 'accuracy', cv = 10)
sfs.fit(X_train, y_train)
print("Model fitting done.")
features = list(sfs.k_feature_names_)
print('Features: ', features, sep='\n')

vclf.fit(X_train[features], y_train)
pred = vclf.predict(X_test[features])

print("Accuracy: ", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
