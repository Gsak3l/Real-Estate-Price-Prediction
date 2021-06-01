import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams['figure.figsize'] = (20, 10)

# getting to know the dataframe a bit more
df1 = pd.read_csv('./data/Bengaluru_House_Data.csv')

# print(df1.shape)
# print(df1.head())
# print(df1.groupby('area_type').agg('count'))

df2 = df1.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')

# print(df2.head())
# print(df2.isnull().sum())
# print(df2.isna().sum())

# filling all the NAN bathrooms with the median
df2['bath'].fillna((df2['bath'].mean()), inplace=True)
# dropping other NAN values
df3 = df2.isnull()
print(df3.isnull().sum())
