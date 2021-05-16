import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams['figure.figsize'] = (20, 10)

# getting to know the dataframe a bit more
df1 = pd.read_csv('./data/Bengaluru_House_Data.csv')
print(df1.head())
print(df1.shape)
# df1 = df1.groupby('city').nunique()
# print(df1)
# print(df1.shape)

print(df1.groupby('area_type')['area_type'].agg('count'))

# dropping some columns that are not that important
df2 = df1.drop(['area_type', 'availability'], axis='columns')
print(df2.head())

print(df2.isnull().sum())

df3 = df2.dropna()
print(df3.isnull().sum())

print(df3['size'])
