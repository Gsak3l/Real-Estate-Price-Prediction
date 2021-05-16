import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams['figure.figsize'] = (20, 10)

# getting to know the dataframe a bit more
df1 = pd.read_csv('./data/Bengaluru_House_Data.csv')

# print(df1.groupby('area_type')['area_type'].agg('count'))

# dropping some columns that are not that important
df2 = df1.drop(['area_type', 'availability', 'society'], axis='columns')

# checking how many null values there are
# print(df2.isnull().sum())

# dropping null and nan values and checking what changes occurred
df3 = df2.dropna()
print(df3.isnull().sum())
# print(df2.shape, df3.shape)

print(df3['size'].unique())

# bhk = rooms i guess
df3['bedrooms'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))
df4 = df3.drop('size', axis='columns')
print(df4.head())
print(df4['bedrooms'].unique())