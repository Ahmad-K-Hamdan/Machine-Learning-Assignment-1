import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("./data/Customer_Data.csv")

print("\nFile Loaded.\n")

print("\nInspecting first few rows: \n")

print(data.head())
print("\n")

print("Checking general information: \n")

print(data.info())
print("\n")

print("Summary statistics: \n")
print(data.describe())
print("\n")

print("Number of null values in each column: \n")
print(data.isnull().sum())
print("\n")

print("Handling missing values for Age by finding the mean for male and female.\n")
meanAgeFemale = data[data["Gender"] == 1]["Age"].mean()
meanAgeMale = data[data["Gender"] == 0]["Age"].mean()

data.loc[data["Gender"] == 1, "Age"] = data.loc[data["Gender"] == 1, "Age"].fillna(meanAgeFemale)

data.loc[data["Gender"] == 0, "Age"] = data.loc[data["Gender"] == 0, "Age"].fillna(meanAgeMale)


print("Handling missing values for SupportCalls by filling it with zeros.\n")
data["SupportCalls"] = data["SupportCalls"].fillna(0)


print("Handling missing values for Income by grouping customers based on Age and filling with the median Income of each group.\n")
bins = [10, 20, 30, 40, 50, 60, 70]
labels = ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69"]
data["GroupByAge"] = pd.cut(data["Age"], bins=bins, labels=labels, right=False)

medianPerGroup = data.groupby("GroupByAge")["Income"].median()

for group in medianPerGroup.index:
    data.loc[(data["GroupByAge"] == group) & (data["Income"].isnull()), "Income"] = medianPerGroup[group]

data.drop("GroupByAge", axis=1, inplace=True)


totalMissingTenure = data["Tenure"].isnull().sum()
print(f"Total missing Tenure values: {totalMissingTenure}")

print("Handling missing Tenure values based on Churn status and predefined group ratios.\n")
""" Explanation: When grouping the data by tenure, we notice two things:
        1. All people who churn have been with the company for less than two years
        2. People who don't churn are split among the three groups, we will fill the missing data according to the existing ratio:
            0-2 -> 0.175
            3-5 -> 0.35
            6-9 -> 0.475

The code for what we explained:
    bins = [0, 3, 6, 10]
    labels = ['0-2', '3-5', '6-9']
    tenureGroupData = pd.cut(data[(data['ChurnStatus'] == 0) & (data['Tenure'].notnull())]['Tenure'], bins=bins, labels=labels, right=False)
    ratios = tenureGroupData.value_counts(normalize=True)
"""

for i in data.index:
    if pd.isnull(data.loc[i, "Tenure"]):
        if data.loc[i, "ChurnStatus"] == 1:
            data.loc[i, "Tenure"] = np.random.uniform(0, 2)
        else:
            r = np.random.rand()
            if r < 0.175:
                data.loc[i, "Tenure"] = np.random.uniform(0, 2)
            elif r < 0.525:
                data.loc[i, "Tenure"] = np.random.uniform(3, 5)
            else:
                data.loc[i, "Tenure"] = np.random.uniform(6, 9)

print("Number of null values in each column after solving missing values: \n")
print(data.isnull().sum())
print("\n")