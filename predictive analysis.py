#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 17:09:27 2017

@author: wqa
"""

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from pandas.plotting import scatter_matrix
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from pandasStatis import load, loadCountryCode, quantify
countryCode=loadCountryCode("iso_3166_1.csv")
db=load("movieDbClean.json")
[db, df]=quantify(db,countryCode)
#eliminate the nah rows,columns
df=df.dropna()
feature_cols = ['budget', 'runtime']
# use the list to select a subset of the original DataFrame
X=df[feature_cols]
y=df['revenue']
#T-test
t=y[0:100]
print(stats.ttest_1samp(t,100000000.0))

#Parametric statistical Linear Regression
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=1)
linreg = LinearRegression()
model=linreg.fit(X_train, y_train)
print(model)
print(linreg.intercept_)
print(linreg.coef_)

######################################################
#Decision Tree Method，KNN
# Summary of data
print(df.describe())

# Plot the data

# Histogram
df.hist()
plt.show()

# Scatterplots to look at 2 variables at once
# scatter plot matrix
scatter_matrix(df)
plt.show()

######################################################
######################################################

#create a python list of feature names
feature_cols = ['budget', 'runtime']
# use the list to select a subset of the original DataFrame
df = pd.DataFrame(df,columns=['budget','revenue','class','ROI','runtime','crew','cast','genre'])
bins=[0,3,10,1000]
names=range(0,3)
#divde the class into 3 catagories due to its ROI
df['class']=pd.cut(df['ROI'],bins,labels=names)
X=df[feature_cols]
y=df['class']
z=df.sort_values(['budget'],ascending=False)
#show the most expensive films Class details
y_true=z.head(10)['class']
print(y_true)
z=X.sort_values(['budget'],ascending=False)
seed = 1
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=seed)

# Setup 10-fold cross validation to estimate the accuracy of different models
# Split data into 10 parts
# Test options and evaluation metric
num_folds = 10
num_instances = len(X_train)
scoring = 'accuracy'


# Use different algorithms to build models
# Add each algorithm and its name to the model array
models = []
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))

# Evaluate each model, add results to a results array,
# Print the accuracy results
results = []
names = []
for name, model in models:
	kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
	cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)
#Knn prediction
knn=KNeighborsClassifier()
knn.fit(X_train, y_train)
pred = knn.predict(z.head(10))
print('Knn prediction:',pred)

#DecisionTree prediction
clf=DecisionTreeClassifier()
clf=clf.fit(X_train, y_train)
pred = clf.predict(z.head(10))
print('DecisionTree prediction:',pred)
#plot the confusion matrix to describe the performance of the model
print('confusion_matrix:\n',confusion_matrix(y_true,pred))
#Plot ROC
fpr, tpr, thresholds = metrics.roc_curve(y_true,pred, pos_label=0)
# Print ROC curve
plt.plot(fpr,tpr)
plt.show() 

######################################################
######################################################
#Naive Bayes Method
clf=GaussianNB()
clf.fit(X_train,y_train)
pred=clf.predict(z.head(10))
print('Naive Bayes prediction:',pred)

######################################################
######################################################
#SVM method
clf=svm.LinearSVC()
clf.fit(X_train,y_train)
print('SVM prediction:',clf.predict(z.head(10)))

#Random Forest trees method
rfc=RandomForestClassifier(n_estimators=200)
rfc.fit(X_train,y_train)
pred=rfc.predict(z.head(10))
print('Random Forest Tree prediction:',pred)
