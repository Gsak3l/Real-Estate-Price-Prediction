import pandas as pd


def create_training_data(df_1):
    dummies = pd.get_dummies(df_1.location)
    # print(dummies.head(3))
    df11 = pd.concat([df_1, dummies.drop('other', axis='columns')], axis='columns')
    # print(df11.head(3))

    df12 = df11.drop('location', axis='columns')
    # print(df12.head(3), df12.shape)
    X = df12.drop('price', axis='columns')
    # print(X.head())
    y = df12.price
    # print(y.head())

    return X, y
