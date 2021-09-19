import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

import data_clean as dc
import training

if __name__ == '__main__':
    matplotlib.rcParams['figure.figsize'] = (20, 10)

    desired_width = 320
    pd.set_option('display.width', desired_width)

    # getting to know the dataframe a bit more
    df1 = pd.read_csv('./data/Bengaluru_House_Data.csv')
    # print(df1.shape)
    # print(df1.head())
    # print(df1.groupby('area_type').agg('count'))

    df3 = dc.clean_dataframe(df1)
    df3 = dc.convert_rooms(df3)

    # there is at least an error with the number of rooms here, considering the square feet
    # print(df3[df3.bhk > 20])
    # print(df3.total_sqft.unique())

    # there are a few sqr_feet that have a range (example 150-200)
    # print(df3[~df3['total_sqft'].apply(is_float)].head())

    # print(convert_sqft_to_num('2123'))
    # print(convert_sqft_to_num('2100 - 2850'))
    # print(convert_sqft_to_num('34.46Sq. Meter'))

    df4 = df3.copy()
    df4['total_sqft'] = df4['total_sqft'].apply(dc.convert_sqft_to_num)
    # print(df4.loc[30])

    df5 = dc.calculate_price_per_sqft(df4)
    # print(df5.head(4))

    df6 = dc.simplify_location(df5)
    # print(df6.head(10))

    # print(df6.shape)
    df7 = dc.outlier_removal(df6)
    # print(df7.shape)

    dc.plot_scatter_chart(df7, 'Rajaji Nagar')

    df8 = dc.remove_bhk_outliers(df7)
    # print(df8.shape)

    # plot_scatter_chart(df8, 'Hebbal')

    matplotlib.rcParams['figure.figsize'] = (20, 10)
    plt.hist(df8.price_per_sqft, rwidth=0.8)
    plt.xlabel('Price per Square Feet')
    plt.ylabel('Count')
    # plt.show()
    plt.clf()

    df9 = dc.remove_bathroom_outliers(df8)
    # print(df9.shape)

    # size = bhk
    # price_per_sqft does not seem important from this point and forward, not sure tho
    df10 = df9.drop(['size', 'price_per_sqft'], axis='columns')
    # print(df10.head(3))

    X, y, X_train, X_test, y_train, y_test = training.create_training_data(df10)
    # print(X, y, X_train, X_test, y_train, y_test)

    lr_clf, lr_clf_result = training.get_train_score(X_train, X_test, y_train, y_test)
    # print(lr_clf_result)

    cross_validation_score = training.get_cross_validation(X, y)
    # print(cross_validation_score)

    # Linear Regression model seems to be the best one out of the three due to higher score
    training.find_best_model(X, y)

    print(training.predict_price(X, y, '1st Phase JP Nagar', 1000, 2, 2, lr_clf))
    print(training.predict_price(X, y, '1st Phase JP Nagar', 1000, 4, 3, lr_clf))
