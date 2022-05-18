import string
import pandas as pd
import numpy as np

data = pd.read_csv("data/positions-huc.csv", ",", dtype=object)

print(data)

totalCount = data.count()["Number"]

data[data['HUC12'] == '-1'] = np.nan

# drop rows with nan values
data = data.dropna()

# drop earthengine columns
data.drop('system:index', axis=1, inplace=True) 
data.drop('.geo', axis=1, inplace=True) 

validCount = data.count()["Number"]

print("totalCount: " + str(totalCount))
print("validCount: " + str(validCount))
print("validPercentage: " + str(round(int(validCount)/int(totalCount)*100, 2)) + " %")

data.to_csv("data/fixed-positions-huc.csv", index=False)
