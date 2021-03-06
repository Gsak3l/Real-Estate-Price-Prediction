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
        df_1['bhk'] = df_1['size'].apply(lambda x: int(x.split(' ')[0]))
    except:
        pass
    # print(df_1['bhk'].unique())
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
        df_3 = subdf[(subdf.price_per_sqft > (mean - standard)) & (subdf.price_per_sqft <= (mean + standard))]
        df_2 = pd.concat([df_2, df_3], ignore_index=True)

    return df_2


def outlier_removal(df_1):
    # average bedroom size is 312 sqft in Bengaluru (-50 for the margin of error)
    # https://www.crddesignbuild.com/blog/average-bedroom-size
    # print(df_1[(df_1.total_sqft / df_1.bhk < 312 - 50)].head().to_string())
    # print(df_1.shape)

    df_2 = df_1[~(df_1.total_sqft / df_1.bhk < 312 - 50)]
    # print(df_2.shape)

    # print(df_2.price_per_sqft.describe())

    df_3 = remove_pps_outliers(df_2)
    return df_3


# drawing a scatter plot for two and three bedroom apartments
def plot_scatter_chart(df_1, location):
    bhk2 = df_1[(df_1.location == location) & (df_1.bhk == 2)]
    bhk3 = df_1[(df_1.location == location) & (df_1.bhk == 3)]
    matplotlib.rcParams['figure.figsize'] = (15, 10)
    plt.scatter(bhk2.total_sqft, bhk2.price_per_sqft, color='blue', label='2 BHK', s=50)
    plt.scatter(bhk3.total_sqft, bhk3.price_per_sqft, marker='+', color='green', label='3 BHK', s=50)
    plt.xlabel("Total Square Feet Area")
    plt.ylabel("Price Per Square Feet")
    plt.title(location)
    plt.legend()
    # plt.show()
    plt.clf()  # clearing the plot for future use


# removing houses that have less bedrooms than the mean and higher price
# example: a house that has 1 bedroom cannot be more expensive than a house with 3
def remove_bhk_outliers(df_1):
    exclude_indices = np.array([])
    for location, location_df in df_1.groupby('location'):
        bhk_stats = {}

        for bhk, bhk_df in location_df.groupby('bhk'):
            # computing per dataframe mean, std, count
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }

        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(exclude_indices,
                                            bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values)

    return df_1.drop(exclude_indices, axis='index')


# most houses cannot have 2 bedrooms and 4 bathrooms,
# thus, this values will be dropped
def remove_bathroom_outliers(df_1):
    # print(df8.bath.unique())
    # print(df8[df8.bath > 10])

    plt.hist(df_1.bath, rwidth=0.8)
    plt.xlabel('Number of Bathrooms')
    plt.ylabel('Count')
    # plt.show()
    plt.clf()

    # print(df_1[df_1.bath > df_1.bhk + 2])
    df_2 = df_1[df_1.bath < df_1.bhk + 2]

    return df_2
