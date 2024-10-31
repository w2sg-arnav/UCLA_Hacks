import dask.dataframe as dd
import os
import pandas as pd

# Load the CSV file with specified dtypes
df = dd.read_csv(r'C:\Users\sonav\Downloads\Compressed\dreamskrin\train_data_ads.csv', dtype={
    'ad_close_list_v001': 'object', 
    'ad_close_list_v002': 'object', 
    'ad_close_list_v003': 'object'
})

# Sample 20% of the data
df = df.sample(frac=0.2, random_state=8)

# Drop specified columns
df = df.drop(['ad_click_list_v001', 'ad_click_list_v002', 'ad_click_list_v003', 'log_id', 'user_id', 'ad_close_list_v001', 'ad_close_list_v002', 'ad_close_list_v003'], axis=1)

# Separate positive and negative labels
pos = df[df['label'] == 1]
neg = df[df['label'] == 0]

# Compute the Dask dataframes into pandas dataframes
pos = pos.compute()
neg = neg.compute()

# Further sample the dataframes if necessary to reduce size
# Here, we sample 80% of the positive and negative dataframes, adjust this fraction as needed
pos = pos.sample(frac=0.65, random_state=8)
neg = neg.sample(frac=0.65, random_state=8)

# Apply transformation to 'u_newsCatInterestsST' column
neg['u_newsCatInterestsST'] = neg['u_newsCatInterestsST'].apply(lambda row: 1 if '0' in row.split('^') else 0)
pos['u_newsCatInterestsST'] = pos['u_newsCatInterestsST'].apply(lambda row: 1 if '0' in row.split('^') else 0)

# Save the dataframes to CSV files
neg.to_csv('./data/final_neg.csv', index=False)
pos.to_csv('./data/final_pos.csv', index=False)