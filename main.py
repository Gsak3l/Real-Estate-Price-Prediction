import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def clean_dataframe(df_1):
    df_2 = df_1.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')

    print(df_2.head())
    print(df_2.isnull().sum())
    print(df_2.isna().sum())

    # filling all the NAN bathrooms with the median
    df_2['bath'].fillna((df_2['bath'].mean()), inplace=True)
    # dropping other NAN values
    ddf3 = df_2.dropna()

    print(ddf3.isnull().sum())
    print(ddf3.head())

    return ddf3


def is_float(x):
    try:
        float(x)
    except:
        return False
    return True


if __name__ == '__main__':
    matplotlib.rcParams['figure.figsize'] = (20, 10)

    # getting to know the dataframe a bit more
    df1 = pd.read_csv('./data/Bengaluru_House_Data.csv')
    print(df1.shape)
    print(df1.head())
    print(df1.groupby('area_type').agg('count'))

    df3 = clean_dataframe(df1)

    # converting different types of rooms into one
    print('nob: number of bedrooms')
    try:
        df3['nob'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))
    except:
        pass

    print(df3['nob'].unique())
    # there is at least an error with the number of rooms here, considering the square feet
    print(df3[df3.nob > 20])

    print(df3.total_sqft.unique())
