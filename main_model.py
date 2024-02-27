import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.metrics import r2_score, get_scorer_names
from module_processing import *

# set verbose mode
verbose = True

# read the feature csv file
df = pd.read_csv(os.path.join(os.path.join(os.getcwd(), "data"), "Waipara_AWS_2023_featured.csv"))

# exploratory analysis - does temperature below zero?
sns.boxplot(x=df["Tair"])
plt.show()

scores = []
lead_time = range(1, 24)

for i in lead_time:

    # set feature names based on stored hours
    feature_cols = df.columns[i:-1]

    # create the feature set and target variable
    X = df.loc[:, feature_cols]
    y = df.loc[:, 'Tair']

    # set up the k folds
    cv = KFold(n_splits=5, random_state=42, shuffle=True)

    # create linear regression model
    linreg = LinearRegression()

    # calculate mean r2 score
    scores.append(np.mean(cross_val_score(linreg, X, y, scoring='r2', cv=cv)))

df2 = {'lead_time (hours)': lead_time, 'r2_mean': scores}
sns.scatterplot(data=df2, x='lead_time (hours)', y='r2_mean')
plt.show()

print(scores)


# cross_val_score(linreg, X, y, cv=10)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# linreg.fit(X_train, y_train)
# y_pred = linreg.predict(X_test)
# print(r2_score(y_test, y_pred))

# df3 = pd.DataFrame.from_dict({'test': y_test['Tair'].to_numpy(), 'pred': y_pred[:, 0]})
# sns.scatterplot(data=df3, x='test', y='pred')
# plt.show()




