
from pathlib import Path
import math
import pandas as pd
import numpy as np


def fixLat(latitude):
    usLatMin = 24
    usLatMax = 49

    first = str(latitude)[:2]

    if (int(first) < usLatMin or int(first) > usLatMax):
        msg = "latitude not in america: " + str(latitude)
        print(msg)
        # raise Exception(msg)
        return np.nan

    second = str(latitude)[2:]

    result = first + "." + second

    return float(result)


def fixLon(longitude):
    usLonMin = -68
    usLonMax = -125

    position = 3

    if(str(longitude)[1] == "1"):
        position = 4

    first = str(longitude)[:position]

    if (int(first) > usLonMin or int(first) < usLonMax):
        msg = "longitude not in america: " + str(longitude)
        print(msg)
        # raise Exception(msg)
        return np.nan

    second = str(longitude)[position:]

    result = first + "." + second

    return float(result)


data = pd.read_csv("data/positions-ll.csv", ",")


fixedLat = data.apply(
    lambda row: fixLat(row['LATITUDE']), axis=1)

fixedLon = data.apply(
    lambda row: fixLon(row['LONGITUDE']), axis=1)


data["fixed-LATITUDE"] = fixedLat
data["fixed-LONGITUDE"] = fixedLon

totalCount = data.count()["LATITUDE"]
data = data.dropna()
validCount = data.count()["LATITUDE"]

print(data)

print("totalCount: " + str(totalCount))
print("validCount: " + str(validCount))
print("validPercentage: " + str(round(int(validCount)/int(totalCount)*100, 2)) + " %")

data.to_csv("data/fixed-positions-ll.csv", index=False)


'''
maxLength = 5000
buckets = validCount / maxLength
buckets = math.ceil(buckets)
buckets = buckets

print("buckets: " + str(buckets))

dataBuckets = np.array_split(data, buckets)

# print(dataBuckets)
path = "data/buckets/"
Path(path).mkdir(parents=True, exist_ok=True)
for count, db in enumerate(dataBuckets):
    db.to_csv(path+"fixed-positions-ll_" +
              str(count) + ".csv", index=False)


data.set_index("Number")
cols = ["Number", "fixed-LATITUDE", "fixed-LONGITUDE"]
jsonData = data[cols].to_json(orient="values")
file1 = open('data/array.txt', 'w')
file1.write(jsonData)
file1.close()
'''


