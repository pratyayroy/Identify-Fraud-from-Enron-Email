#!/usr/bin/python

import pickle
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest, f_classif
import pandas as pd
from tabulate import tabulate
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from tester import test_classifier
import matplotlib.pyplot as plt

with open("final_project_dataset.pkl", "r") as data_file:  # opening the pickle file and reading it in a dictionary
    data_dict = pickle.load(data_file)

"""
Task 1: Basic description of the dataset
"""

df = pd.DataFrame.from_dict(data_dict, orient='index')  # converting the data into Pandas DataFrame for analysis
print "Printing Top 5 rows" + "\n"
print "\n" + tabulate(df.head(), headers='keys', tablefmt='pipe') + "\n"  # seeing how the data looks like

# answering some basic questions
print "Total Employees: " + str(df.shape[0])
print "----------------"
print "Total Features: " + str(df.shape[1])
print "---------------"
print "List of features describing each employee: "
print "------------------------------------------"
print list(df.columns.values)
print "Total POI: " + str(df['poi'][df['poi']].size)
print "----------\n"

# getting stats on NaN and empty cells
# IGNORED: FutureWarning: element-wise comparison failed; returning scalar instead, but in the future will perform
# element-wise comparison result = getattr(x, name)(y)
temp = {}
for i in list(df.columns.values):
    try:
        temp[i] = str(df[i][df[i] == 'NaN'].size / (df.shape[0] * 1.0) * 100) + "%"
    except:
        temp[i] = "0%"
temp = pd.DataFrame.from_dict(temp, orient='index')
temp.columns = ['Percentage']
print "\nPercentage of NaNs\n"
print tabulate(temp, headers='keys', tablefmt='pipe') + "\n"

# getting rid of NaN (which are actually string, so fillna() is not working)
df.replace(to_replace='NaN', value=0.0, inplace=True)

# getting the basic stats
print "Printing Basic Statistics" + "\n"
print tabulate(df.describe(), headers='keys', tablefmt='pipe')

"""
Task 2: Choosing features to study outliers and removing them 
"""
# perform data wrangling (uncomment the below code to run here or run it separately)
# from data_wrangling import *
# according to data_wrangling.py TOTAL, THE TRAVEL AGENCY IN THE PARK and LOCKHART EUGENE E are outliers
df.drop(['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E'], inplace=True)

"""
Task 3: Creating new feature(s)
"""

# feature 1: poi_email_engagement = (total email from/to poi)/(total to/from messages)
try:
    df['poi_email_engagement'] = ((df['from_poi_to_this_person'] + df['from_this_person_to_poi']) * 1.0) / (
        df['to_messages'] + df['from_messages'])
except:
    df['poi_email_engagement'] = 0

# feature 2: from_poi_ratio = (total messages from poi)/(total from messages)
try:
    df['from_poi_ratio'] = ((df['from_poi_to_this_person']) * 1.0) / df['from_messages']
except:
    df['from_poi_ratio'] = 0

# feature 3: to_poi_ratio = (total messages to poi)/(total to messages)
try:
    df['to_poi_ratio'] = ((df['from_this_person_to_poi']) * 1.0) / df['to_messages']
except:
    df['to_poi_ratio'] = 0

# feature 4: capital in hand = total payments + exercised stock
df['capital_in_hand'] = df['total_payments'] + df['exercised_stock_options']

# feature 5: email involvement = total from/to messages + shared receipt with poi
df['email_involvement'] = df['to_messages'] + df['from_messages'] + df['shared_receipt_with_poi']
df.fillna(0, inplace=True)

# selected features to be used in ranking to identify top 5
selected_features = ['poi',
                     'poi_email_engagement',
                     'from_poi_ratio',
                     'to_poi_ratio',
                     'capital_in_hand',
                     'email_involvement',
                     'salary',
                     'to_messages',
                     'deferral_payments',
                     'total_payments',
                     'exercised_stock_options',
                     'bonus',
                     'restricted_stock',
                     'shared_receipt_with_poi',
                     'restricted_stock_deferred',
                     'total_stock_value',
                     'expenses',
                     'loan_advances',
                     'from_messages',
                     'other',
                     'from_this_person_to_poi',
                     'director_fees',
                     'deferred_income',
                     'long_term_incentive',
                     'from_poi_to_this_person']

my_dataset = df.to_dict('index')
data = featureFormat(my_dataset, selected_features, sort_keys=True)
labels, features = targetFeatureSplit(data)

# Generating top 5 features
selector = SelectKBest(f_classif, k=5)
print "+++++++++++++++++++++++++++++"
scores = pd.DataFrame.from_records(
    sorted(zip(selected_features[1:], selector.fit(features, labels).scores_), key=lambda x: x[1], reverse=True)).set_index(0)
print scores
scores.plot.bar()
plt.ylabel("SelectKBest scores")
plt.xlabel("Features")
plt.legend(["scores"])
plt.savefig("./feature_selection/1.png", bbox_inches='tight')
print "+++++++++++++++++++++++++++++"

top_5 = sorted(zip(selected_features[1:], selector.fit(features, labels).scores_), key=lambda x: x[1], reverse=True)[:5]
temp = pd.DataFrame.from_records(top_5)
temp.columns = ["features", "score ^"]
print "Printing Top 5 Features" + "\n"
print "\n" + tabulate(temp, headers='keys', tablefmt='pipe') + "\n"
selected_features = ["poi"] + map(lambda x: x[0], top_5)

data = featureFormat(my_dataset, selected_features, sort_keys=True)
labels, features = targetFeatureSplit(data)

"""
Task 4: Try a variety of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html

Task 5: Tune your classifier to achieve better than .3 precision and recall
using our testing script. Check the tester.py script in the final project
folder for details on the evaluation method, especially the test_classifier
function. Because of the small size of the dataset, the script uses
stratified shuffle split cross validation. For more info:
http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
"""


def tune_params(clf, param):
    """
    This function computes the best classifier and prints its metrics
    :param clf: The pipeline containing the classifier and the other functions to be performed
    :param param: The parameters for the functions to be performed
    :return: The best estimated classifier
    """

    # 100 corresponds to the number of re-shuffling & splitting iterations
    # If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.
    sss = StratifiedShuffleSplit(100, test_size=0.3, random_state=60)
    gs = GridSearchCV(clf, param, cv=sss, scoring='f1')
    gs.fit(features, labels)
    clf = gs.best_estimator_

    # getting score based on Udacity's tester.py
    test_classifier(clf, my_dataset, selected_features)
    return clf


# trying Naive Bayes
pca = PCA()
nb_clf = GaussianNB(priors=[0.3, 0.7])
pipeline = Pipeline([("PCA", pca), ("NaiveBayesClassifier", nb_clf)])
parameters = {"PCA__n_components": [4]}
print "\nGetting results for Naive Bayes"
print "-------------------------------"
nb_clf = tune_params(pipeline, parameters)

# trying Decision Tress
pca = PCA()
dt_clf = DecisionTreeClassifier()
pipeline = Pipeline([("PCA", pca), ("DecisionTreeClassifier", dt_clf)])
parameters = {"DecisionTreeClassifier__min_samples_leaf": range(2, 12, 3),
              "DecisionTreeClassifier__min_samples_split": range(2, 12, 3),
              "DecisionTreeClassifier__criterion": ["entropy", "gini"],
              "DecisionTreeClassifier__max_leaf_nodes": range(5, 20, 5),
              "PCA__n_components": [None]
              }
print "\nGetting results for Decision Trees"
print "----------------------------------"
dt_clf = tune_params(pipeline, parameters)

# trying Logistic Regression
pca = PCA()
lr_clf = LogisticRegression()
pipeline = Pipeline([("PCA", pca), ("LogisticRegression", lr_clf)])
parameters = {'LogisticRegression__C': [1e-09, 1e-08, 1e-07, 1e-06, 1e-03, 1e-02, 0.1],
              'LogisticRegression__tol': [0.01, 0.001, 0.0001],
              'LogisticRegression__penalty': ['l2'],
              'LogisticRegression__class_weight': ['balanced'],
              'LogisticRegression__solver': ['lbfgs', 'liblinear'],
              'LogisticRegression__random_state': [42],
              "PCA__n_components": [3],
              }
print "\nGetting results for Logistic Regression"
print "---------------------------------------"
lr_clf = tune_params(pipeline, parameters)

# trying Random Forest
pca = PCA()
rf_clf = RandomForestClassifier()
pipeline = Pipeline([("PCA", pca), ("RandomForestClassifier", rf_clf)])
parameters = {'RandomForestClassifier__max_depth': [None, 5, 10],
              'RandomForestClassifier__max_leaf_nodes': [None, 5, 10, 20],
              'RandomForestClassifier__n_estimators': [10, 15],
              'RandomForestClassifier__random_state': [42, 60],
              }
print "\nGetting results for Random Forest"
print "---------------------------------"
rf_clf = tune_params(pipeline, parameters)

"""
# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.
"""
clf = dt_clf
features_list = selected_features
dump_classifier_and_data(clf, my_dataset, features_list)
