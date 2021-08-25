import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def clean_dataframe(df_1):
    df_2 = df_1.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')

    # print(df_2.head())
    # print(df_2.isnull().sum())
    # print(df_2.isna().sum())

    # filling all the NAN bathrooms with the median
    df_2['bath'].fillna((df_2['bath'].mean()), inplace=True)
    # dropping other NAN values
    df_3 = df_2.dropna()

    # print(df_3.isnull().sum())
    # print(df_3.head())

    return df_3


def convert_rooms(df_1):
    # converting different types of rooms into one
    try:
        df_1['number_of_rooms'] = df_1['size'].apply(lambda x: int(x.split(' ')[0]))
    except:
        pass
    # print(df_1['number_of_rooms'].unique())
    return df_1


def is_float(x):
    try:
        float(x)
    except:
        return False
    return True


def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:  # average value
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(x)
    except:
        return None


def calculate_price_per_sqft(df_1):
    df_1['price_per_sqft'] = df_1['price'] * 100000 / df_1['total_sqft']
    return df_1


def simplify_location(df_1):
    # print(len(df_1.location.unique()))
    df_1.location = df_1.location.apply(lambda x: x.strip())

    # there are locations that have just one house for sale
    location_stats = df_1.groupby('location')['location'].agg('count').sort_values(ascending=False)
    # print(location_stats)

    # number of locations that have less than 10 data points
    # print(len(location_stats[location_stats < 10]))

    location_stats_less_than_10 = location_stats[location_stats < 10]

    # if less than 10 make it 'other' else keep it
    df_1.location = df_1.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
    # print(len(df_1.location.unique()))

    return df_1


def remove_pps_outliers(df_1):
    # finding mean and standard deviation for each location
    # and filtering points that are beyond one standard deviation
    df_2 = pd.DataFrame()

    for key, subdf in df_1.groupby('location'):
        mean = np.mean(subdf.price_per_sqft)
        standard = np.std(subdf.price_per_sqft)

        # don't know how this works
        # keeping everything below and above mean+-standard and appending those dataframes per location
        reduced_df = subdf[(subdf.price_per_sqft > (mean - standard)) & (subdf.price_per_sqft <= (mean + standard))]
        df_2 = pd.concat([df_2, reduced_df], ignore_index=True)

    return df_2


def outlier_removal(df_1):
    # average bedroom size is 312 sqft in Bengaluru (-50 for the margin of error)
    # https://www.crddesignbuild.com/blog/average-bedroom-size
    # print(df_1[(df_1.total_sqft / df_1.number_of_rooms < 312 - 50)].head().to_string())
    # print(df_1.shape)

    df_2 = df_1[~(df_1.total_sqft / df_1.number_of_rooms < 312 - 50)]
    # print(df_2.shape)

    print(df_2.price_per_sqft.describe())

    df_3 = remove_pps_outliers(df_2)
    return df_3


if __name__ == '__main__':
    matplotlib.rcParams['figure.figsize'] = (20, 10)

    # getting to know the dataframe a bit more
    df1 = pd.read_csv('./data/Bengaluru_House_Data.csv')
    # print(df1.shape)
    # print(df1.head())
    # print(df1.groupby('area_type').agg('count'))

    df3 = clean_dataframe(df1)
    df3 = convert_rooms(df3)

    # there is at least an error with the number of rooms here, considering the square feet
    # print(df3[df3.number_of_rooms > 20])
    # print(df3.total_sqft.unique())

    # there are a few sqr_feet that have a range (example 150-200)
    # print(df3[~df3['total_sqft'].apply(is_float)].head())

    # print(convert_sqft_to_num('2123'))
    # print(convert_sqft_to_num('2100 - 2850'))
    # print(convert_sqft_to_num('34.46Sq. Meter'))

    df4 = df3.copy()
    df4['total_sqft'] = df4['total_sqft'].apply(convert_sqft_to_num)
    # print(df4.loc[30])

    df5 = calculate_price_per_sqft(df4)
    # print(df5.head(4))

    df6 = simplify_location(df5)
    # print(df6.head(10))

    print(df6.shape)
    df7 = outlier_removal(df6)
    print(df7.shape)
