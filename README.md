Investigate a Dataset
==========================

This repo contains files for my "P8 | Identify Fraud From Enron Mail", done as a part of Data Analyst Nanodegree in Udacity.



Documents
---------

*  **outlier_plots**: Folder containing the plots used to identify the outliers and is used in the report.
*  **data_wrangling.py**: Th python script to wrangle and clean the data having outliers.
*  **enron61702insiderpay.pdf**: The details of the Enron Employee containing details of their payments and their stocks.
*  **feature_format.py**: The python script supplied by Udacity to perform conversions of the data dictionary to necessary formats is input to the classifiers
*  **final_project_dataset.pkl**: The pickle converted version of the Enron pdf.
*  **Identify Fraud from Enron Email.ipynb**: The report in Jupyter Notebook format.
*  **Identify Fraud from Enron Email.html**: The report in HTML format.
*  **my_classifier.pkl**: The best classifier with the tuned parameters exported from the driver program to be used for evaluation.
*  **my_dataset.pkl**: The cleaned dataset on which the classifiers were trained and tuned exported from the driver program to be used for evaluation.
*  **my_feature_list.pkl**: The top 5 features on which the classifiers were trained and tuned exported from the driver program to be used for evaluation.
*  **poi_id.py**: The driver program of the project that operates on the clean data and reduced features for the training of the classifiers.
*  **tester.py**: The python script supplied by Udacity for evaluation of the best classifier found by the driver program and reports its [erformance.]

> **Notes**
>
> poi_id.py directly removes the outliers as found by data_wrangling.py.
> Two warnings
    1. DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also, note that the interface of the new CV iterators is different from that of this module. This module will be removed in 0.20.
    "This module will be removed in 0.20.", DeprecationWarning)
    2. FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
    result = getattr(x, name)(y) 
    are ignored.

---