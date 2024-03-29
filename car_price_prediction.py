# -*- coding: utf-8 -*-
"""Car_Price_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gj8Ua1oKSicbuAaMa2p6AZdBNZGMol6I
"""

import pandas as pd
import numpy as np

data = pd.read_csv('car data.csv')
data.head()

data.shape

data.columns

data.describe()

data.isnull().sum()

data['Fuel_Type'].unique()

data.drop('Car_Name',axis = 1, inplace = True)
data.head()

data['Current_Year'] = 2021
data.head()

data['No_of_Years'] = data['Current_Year'] - data['Year']
data.head()

data.drop('Year', axis =1, inplace = True)
data.head()

#Getting Dummy variables for categorical attributes

final_data = pd.get_dummies(data,drop_first = True)
final_data.head()

#saving the final dataset
final_data.to_csv('carData.csv')

final_data.drop('Current_Year',axis = 1, inplace = True)
#Calculating the Correlation between attributes
final_data.corr()

import seaborn as sns
corr = final_data.corr()
sns.heatmap(corr, annot = True)

#Separating attributes and targets
X = final_data.iloc[:,1:]
Y = final_data.iloc[:,0]
print(X.head())
print(Y.head())

import sklearn
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 2)

print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

# Random Forest

"""#Random Forest Model"""

from sklearn.ensemble import RandomForestRegressor

Forest = RandomForestRegressor(n_estimators=100, random_state = 42)

Forest.fit(X_train, Y_train)

Forest_pred = Forest.predict(X_test)
print(Forest_pred)

"""#Evaluation"""

Forest.score(X_test, Y_test)

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
print('The accuracy score is: ',r2_score(Y_test,Forest_pred))
print('Mean Squared Error: ', mean_squared_error(Y_test, Forest_pred))
print('Mean Absolute Error: ', mean_absolute_error(Y_test, Forest_pred))
print('Root Mean Squared Error: ', np.sqrt(mean_squared_error(Y_test, Forest_pred)))



"""#Linear Regression Model"""

from sklearn.linear_model import LinearRegression
Lin_model = LinearRegression()

Lin_model.fit(X_train, Y_train)

Lin_pred = Lin_model.predict(X_test)
print(Lin_pred)

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
print('The accuracy score is: ',r2_score(Y_test,Lin_pred))
print('Mean Squared Error: ', mean_squared_error(Y_test, Lin_pred))
print('Mean Absolute Error: ', mean_absolute_error(Y_test, Lin_pred))
print('Root Mean Squared Error: ', np.sqrt(mean_squared_error(Y_test, Lin_pred)))



"""#Decision Tree model """

from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor()
tree.fit(X_train, Y_train)

tree_pred = tree.predict(X_test)
print(tree_pred)

from sklearn.metrics import r2_score
print("Accuracy score: ", r2_score(Y_test, tree_pred))

from sklearn import tree
clf = tree.DecisionTreeRegressor(max_depth=2)
clf.fit(X_train,Y_train)
tree.plot_tree(clf)



"""#Feature Importance"""

from sklearn.ensemble import ExtraTreesRegressor

model = ExtraTreesRegressor()

model.fit(X, Y)

print(model.feature_importances_)

feat_imp = pd.Series(model.feature_importances_, index = X.columns)

import matplotlib.pyplot as plt

feat_imp.nlargest(5).plot(kind = 'bar')
plt.show()

"""# Hyperparameter Tuning for Random Forest Regressor"""

#n_estimators = the no. of trees in the forest
n_esimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
print(n_esimators)

# RandomizedSearchCV
from sklearn.model_selection import RandomizedSearchCV

#n_estimators = the no. of trees in the forest.
n_esimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]

#Number of features to consider at every split.
max_features = ['auto','sqrt']

#Max no of levels in the tree.
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]

#Min no. of samples required to split a node.
min_samples_split = [2, 5, 10, 15, 100]

#Min no. of samples required at each leaf node.
min_samples_leaf = [1, 2, 5, 10]

# create a random grid
random_grid = {
    'n_estimators': n_esimators,
    'max_features': max_features,
    'max_depth':max_depth,
    'min_samples_split':min_samples_split,
    'min_samples_leaf': min_samples_leaf
}

print(random_grid)

# create a base model to tune
Forest = RandomForestRegressor()

rf_random = RandomizedSearchCV(estimator = Forest, param_distributions=random_grid, scoring = 'neg_mean_squared_error', n_iter=100, cv = 5, verbose=2, random_state = 42, n_jobs = 1)

rf_random.fit(X_train, Y_train)

rf_random.best_params_

rf_random.best_score_

"""# Final Prediction and Evaluation"""

#Prediction
Y_pred = rf_random.predict(X_test)
print(Y_pred)

#Evaluation
print('MAE: ',mean_absolute_error(Y_test, Y_pred))
print('MSE: ', mean_squared_error(Y_test, Y_pred))
print('RMSE: ', np.sqrt(mean_squared_error(Y_test, Y_pred)))
print('R2_Score: ', r2_score(Y_test, Y_pred))

"""# Saving the model"""

import pickle
file = open('car_price_model.pkl', 'wb')

pickle.dump(rf_random, file)