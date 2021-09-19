import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, ShuffleSplit, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.tree import DecisionTreeRegressor


# literally copied the method from reddit, not sure if this will work
def create_training_data(df_1):
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

    return X, y, X_train, X_test, y_train, y_test


# tutorial from here https://www.youtube.com/watch?v=iL_iWFSzjK8
def get_train_score(X_train, X_test, y_train, y_test):
    lr_clf = LinearRegression()
    lr_clf.fit(X_train, y_train)
    lr_clf_result = lr_clf.score(X_test, y_test)

    return lr_clf, lr_clf_result


def get_cross_validation(X, y):
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    return cross_val_score(LinearRegression(), X, y, cv=cv)


# finds the best model using GridSearchCV
# GridSearchCV does the best algorithm selection
# and also finds the best parameter for that algorithm Hyper Parameter Tuning
def find_best_model(X, y):
    # python dictionary
    algos = {
        'linear_regression': {
            'model': LinearRegression(),
            'params': {
                'normalize': [True, False]
            }
        }, 'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1, 2],
                'selection': ['random', 'cyclic']
            }
        }, 'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {
                'criterion': ['mse', 'friedman_mse'],
                'splitter': ['best', 'random']
            }
        }
    }

    scores = []
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

    # going through the python dictionary above
    for algo_name, config in algos.items():
        gs = GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
        gs.fit(X, y)
        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores, columns=['model', 'best_score', 'best_params'])


def predict_price(X, y, location, sqft, bath, bhk, lr_clf):
    # print(X.columns)
    # print(np.where(X.columns == location)[0][0])
    loc_index = np.where(X.columns == location)[0][0]

    x = np.zeros(len(X.columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    return lr_clf.predict([x])[0]
