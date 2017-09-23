#!/usr/bin/python

import pickle
from feature_format import featureFormat
import matplotlib.pyplot as plt
from pprint import pprint


def get_name(k1, v1, k2, v2):
    """
    This function returns the names of those employees whose salary and bonus are passed as parameters
    :param k1: the name of the feature ("salary" in this case)
    :param v1: the value of the salary
    :param k2: the name of the feature ("bonus" in this case)
    :param v2: the value of bonus
    :return: the name of the Enron employee
    """
    for i in data_dict:
        if data_dict[i][k1] == v1 and data_dict[i][k2] == v2:
            print "**OUTLIER: {}".format(i)
            return i


with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# trying for outliers in salary and bonus -- 1
print "Run 1 :: Detecting outliers in plotting salary and bonus.."
print "----------------------------------------------------------"
features = ["salary", "bonus"]
data = featureFormat(data_dict, features)
plt.figure(1)
for point in data:
    salary = point[0]
    bonus = point[1]
    plt.scatter(salary, bonus)
    if salary > 20000000:
        plt.annotate(
            get_name("salary", salary, "bonus", bonus) + "\nsalary: {}\nbonus: {}".format(salary, bonus),
            (salary, bonus))
plt.xlabel("salary")
plt.ylabel("bonus")
plt.savefig("./outlier_plots/salary_bonus1.png", bbox_inches='tight')
# plt.show()

# removing TOTAL (outlier from run 1)
data_dict.pop("TOTAL")
data = featureFormat(data_dict, features)

# trying for outliers in salary and bonus -- 2
print "\nRun 2 :: Detecting outliers in plotting salary and bonus.."
print "----------------------------------------------------------"
plt.figure(2)
for point in data:
    salary = point[0]
    bonus = point[1]
    plt.scatter(salary, bonus)
    if salary > 800000 or bonus > 5000000:
        plt.annotate(
            get_name("salary", salary, "bonus", bonus), (salary, bonus))
plt.xlabel("salary")
plt.ylabel("bonus")
plt.savefig("./outlier_plots/salary_bonus2.png", bbox_inches='tight')
# plt.show()

# printing outliers where salary or bonus is NaN
print "\nRun 3 :: Detecting outliers in plotting salary and bonus.."
print "----------------------------------------------------------"
for i in data_dict:
    if data_dict[i]["salary"] == "NaN" and data_dict[i]["bonus"] == "NaN":
        print "**OUTLIER (NaN values): {}".format(i)

# details of THE TRAVEL AGENCY IN THE PARK
print "\nFeature details of THE TRAVEL AGENCY IN THE PARK :: {}".format(data_dict["THE TRAVEL AGENCY IN THE PARK"])
print "------------------------------------------------"

# searching for percentages of NaN(s)
print "\nNaN percentage of the Enron employees (top 10)"
print "----------------------------------------------"
feat = data_dict[data_dict.keys()[1]].keys()
per = []
for i in data_dict:
    cnt = 0
    for j in feat:
        if data_dict[i][j] == "NaN":
            cnt += 1
    per.append([i, cnt / (len(feat) * 1.0) * 100])
pprint(sorted(per, key=lambda x: x[1], reverse=True)[:10])
