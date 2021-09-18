import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# literally copied the method from reddit, not sure if this will work
def create_training_data(df_1):
    print('i am here')
    dummies = pd.get_dummies(df_1.location)
    # print(dummies.head(3))
    df_2 = pd.concat([df_1, dummies.drop('other', axis='columns')], axis='columns')
    # print(df11.head(3))

    df_3 = df_2.drop('location', axis='columns')
    # print(df12.head(3), df12.shape)
    X = df_3.drop('price', axis='columns')
    # print(X.head())
    y = df_3.price
    # print(y.head())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    get_train_score(X_train, X_test, y_train, y_test)


def get_train_score(X_train, X_test, y_train, y_test):
    # tutorial from here https://www.youtube.com/watch?v=iL_iWFSzjK8
    lr_clf = LinearRegression()
    lr_clf.fit(X_train, y_train)
    lr_clf_result = lr_clf.score(X_test, y_test)

    print(lr_clf_result)
