
# User Feature Distribution Analysis for Ad Clicks (Handling Missing Values and Single Plot)

## Description

This Python script suite provides functionalities to analyze the distributions of user features in a dataset (`merged_train_data.csv`) and compare them between all users and users who clicked on ads (`label = 1`). It employs Seaborn's `kdeplot` function to create kernel density plots, which visually represent the probability density of each feature. The code offers two approaches:

### Multiple Subplots with Missing Value Handling (Version 1 & 2):

- Analyzes multiple features specified in a list.
- Creates separate subplots for each feature, allowing for a more detailed comparison.
- Explicitly handles missing values using `dropna()` before plotting for accurate representation.

### Single Plot for Specific Feature (Version 3):

- Analyzes a single feature (`slot_id` in this example).
- Creates a single plot with overlaid kernel density distributions for both all users and users who clicked ads.
- Implicit error handling is assumed (recommended to add explicit handling).

## Code Walkthrough (Version 1 & 2)

### Import Libraries

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
```

- `pandas`: Used for data manipulation and analysis (reading CSV, filtering).
- `seaborn`: Provides a high-level interface for generating statistical graphics based on Matplotlib (creating kernel density plots).
- `matplotlib.pyplot`: The core plotting library in Python (configuring plot layout and elements).

### Set File Path and Sample Size

```python
file_path = r"C:\Users\aaria\Downloads\merged_train_data.csv"
sample_size = 1000000
```

- Specify the location of your CSV file containing user data.
- `sample_size`: Define the maximum number of rows to read from the CSV file (helps with large datasets to avoid memory issues).

### Error Handling

```python
try:
    advertiser_data = pd.read_csv(file_path, nrows=sample_size)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()
except pd.errors.EmptyDataError:
    print(f"Error: File '{file_path}' is empty or cannot be read as CSV.")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()
```

This block gracefully handles potential errors that might occur while reading the CSV file:
- `FileNotFoundError`: File not found at specified location.
- `pd.errors.EmptyDataError`: File is empty or corrupt.
- `Exception`: Catches other unexpected errors.

Prints an informative error message and exits the script in case of issues.

### Filter Clicked Users

```python
clicked_data = advertiser_data[advertiser_data['label'] == 1]
```

Extracts only the rows where the `label` column is 1, representing users who clicked ads. This creates a new DataFrame (`clicked_data`) containing these users.

### Select Features

```python
features = ['creat_type_cd', 'inter_type_cd', 'app_second_class']  # Version 1 Example
# OR
features = ['gender', 'emui_dev', 'net_type', 'adv_prim_id', 'hispace_app_tags', 'app_score', 'u_refreshTimes', 'u_feedLifeCycle']  # Version 2 Example
```

Define a list of features for which you want to compare distributions across all users and those who clicked ads. You can modify these lists to analyze different features in your dataset.

### Create Subplots and Kernel Density Plots

```python
fig, axes = plt.subplots(len(features), 1, figsize=(12, 15))  # One row per feature

for i, column in enumerate(features):
    sns.kdeplot(advertiser_data[column].dropna(), label='All Users', shade=True, ax=axes[i])
    sns.kdeplot(clicked_data[column].dropna(), label='Users Who Clicked Ads', shade=True)
    axes[i].set_title(f'Distribution of {column}')
    axes[i].legend()

plt.tight_layout()
plt.show()

```

This section of code does the following:
- Creates a figure with subplots, one for each feature.
- Iterates through each feature in the list and generates kernel density plots for both all users and users who clicked ads.
- Adds titles to each subplot and includes a legend for better clarity.
- Uses `tight_layout` to adjust subplot parameters for a cleaner appearance.
- Displays the plots.

## Code Walkthrough (Version 3)

### Single Plot for Specific Feature

```python
# Import Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set File Path and Sample Size
file_path = r"C:\Users\aaria\Downloads\merged_train_data.csv"
sample_size = 1000000

# Error Handling
try:
    advertiser_data = pd.read_csv(file_path, nrows=sample_size)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()
except pd.errors.EmptyDataError:
    print(f"Error: File '{file_path}' is empty or cannot be read as CSV.")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()

# Filter Clicked Users
clicked_data = advertiser_data[advertiser_data['label'] == 1]

# Single Feature Analysis
feature = 'slot_id'

# Create Single Plot
plt.figure(figsize=(10, 6))
sns.kdeplot(advertiser_data[feature].dropna(), label='All Users', shade=True)
sns.kdeplot(clicked_data[feature].dropna(), label='Users Who Clicked Ads', shade=True)
plt.title(f'Distribution of {feature}')
plt.legend()
plt.show()
```

This section outlines the steps to create a single plot for a specific feature:
- Imports necessary libraries.
- Sets the file path and sample size.
- Handles potential errors while reading the CSV file.
- Filters the data for users who clicked ads.
- Specifies the feature to analyze.
- Creates a single plot with overlaid kernel density distributions for both all users and users who clicked ads.
- Adds a title and legend to the plot.
- Displays the plot.

## Conclusion

These Python scripts provide a flexible framework for analyzing user feature distributions in ad click datasets. Whether you need detailed comparisons across multiple features or a focused analysis of a single feature, the provided code can be adapted to meet your needs. Remember to handle missing values and errors appropriately to ensure accurate and robust analyses.
