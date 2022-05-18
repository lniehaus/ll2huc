# LL2HUC

This Repository contains scripts to convert Latitude and Longitude (LL) values into Hydrologic Unit Codes (HUC).

HUCs are used to separate the USA into different Hydrologic regions. They can range from 2 to 12 digits. https://nas.er.usgs.gov/hucs.aspx

The conversion from Latitude and Longitude into the Hydrologic Unit Codes is done with the Google Earth Engine. https://earthengine.google.com/

Pre- and postprocessing is done in Python and the actual collection of the HUCs is done inside the Earth Engine Code Editor. https://developers.google.com/earth-engine/guides/playground

As Input and output for the Earth Engine, we use the CSV Format.

# Preprocessing

We do know that the Latitude and Longitude values are using the "Decimal Degree" format, but unfortunately, our data is corrupted, and the floating points are missing.

For example: our latitude and longitude values do look like this: 3975231,-10499906. But in realty they should look like this: 39.75231170654297,-104.99906158447266.

First of all we know that the latitude ranges from -90 to +90 and the longitude ranges from -180 to +180. So for the latitude we know that the floating point can be at the second position max and for the longitude it is the third (or forth if we pay attention to the minus).

Since this information is not enough to clearly identify the floating point position, we need more information. Luckily, HUC is mainly used in the USA, so we can ignore all latitude and longitude values that are outside their borders. The USA ranges in latitude from 24 to 39 and in longitude from -68 to -125. This Information helps us to identify all the latitude and longitude values since all the latitude values are separated after the second digit and the longitude values are separated at the second value unless the number starts with a 1 which leads to the floating point being at the third position.

Fixing the latitude and longitude can be done by executing fixLL.py

# HUC Collection

Now we need to use the Earth Engine to get the Hydrologic units codes from the latitude and longitude values. The Online Code Editor can be found under. https://code.earthengine.google.com/
To use the Earth Engine, you need to register an account. After the registration is done, you will get access to the Code Editor.

If you know a bit of JavaScript, that is perfect, but unfortunately that is not enough to get you through your Earth Engine journey. For loops, if conditions or setting variables does have their own syntax inside the Earth Engine since some code will be executed on the client-side and some on the server-side. It can be hard to determine which code gets executed where, but as a rule of thumb, all the "ee." objects get executed on the server.

I highly recommend checking the documentation for further information about the dos and don'ts of the Earth Engine (it is actually well written) https://developers.google.com/earth-engine/guides/client_server

First you want to upload your csv file to the Code Editor by clicking on "Assets" at the top left and then on new to "Table Upload" a "CSV file". In this case we upload the file "fixed-positions-ll.csv".

Now you can go back to "Scripts" and copy the code from CollectHUC.js into your Code Editor window in the top-middle.

By changing the path of the following command, you can select your uploaded csv file

<code>
var positions = ee.FeatureCollection("projects/ee-lniehaus/assets/fixed-positions-ll");
</code>

By setting the following names, you can change which columns of the csv should be used as latitude and longitude.

<code>
var lat = f.get('fixed-LATITUDE');

var lon = f.get('fixed-LONGITUDE');
</code>

After all is set to the correct values, you can press the "Run" button on the top. This will not directly run the code on the Earth Engine server. After you pressed "Run" you need to click on "Tasks" in the right window and then click on the blue "RUN" buttons at the "UNSUBMITTED TASKS".

Now you will be asked where you want to save your new csv file which contains the HUC values. Click on "RUN" and the code will be executed, and your file will be created after it is done.

Congratulations! You now have converted your latitude and longitude values into HUC12 regions.

# Postprocessing

There are some latitude and longitude combinations which are valid because they are in the USA, but do not have a HUC region assigned to them. For example, if the latitude and longitude is inside the Gulf of Mexico. The HUC12 value of these rows will be set to -1.

If you do not want to have these rows in your dataset, you can execute fixHUC.py. It will delete all rows which do have a -1 as HUC12 value.

# Data

1. We start with a file that has a reference number and the corrupted latitude and longitude values

| Number | LATITUDE   | LONGITUDE   |
| ------ | ---------- | ----------- |
| 1001   | 2978037    | -956295     |
| 1002   | 18445975   | -66391282   |
| 1003   | 367452     | -1074455    |
| 1004   | 2629555555 | -9489777777 |
| 1005   | 430611     | -760819     |

2. fixLL.py converts these rows into correct values, that are in the USA. In this process, 1 row (1002) gets dropped.

| Number | LATITUDE   | LONGITUDE   | fixed-LATITUDE | fixed-LONGITUDE |
| ------ | ---------- | ----------- | -------------- | --------------- |
| 1001   | 2978037    | -956295     | 29.78037       | -95.6295        |
| 1003   | 367452     | -1074455    | 36.7452        | -107.4455       |
| 1004   | 2629555555 | -9489777777 | 26.29555555    | -94.89777777    |
| 1005   | 430611     | -760819     | 43.0611        | -76.0819        |

3. The Google Earth Engine collects the HUC12 values for the given latitude and longitude values.

| system:index         | HUC12        | LATITUDE   | LONGITUDE   | Number | fixed-LATITUDE     | fixed-LONGITUDE     | .geo                                   |
| -------------------- | ------------ | ---------- | ----------- | ------ | ------------------ | ------------------- | -------------------------------------- |
| 00000000000000000000 | 120401040303 | 2978037    | -956295     | 1001   | 29.780370712280273 | -95.62950134277344  | {"type":"MultiPoint","coordinates":[]} |
| 00000000000000000001 | 140801011604 | 367452     | -1074455    | 1003   | 36.745201110839844 | -107.44550323486328 | {"type":"MultiPoint","coordinates":[]} |
| 00000000000000000002 | -1           | 2629555555 | -9489777777 | 1004   | 26.29555555        | -94.89777777        | {"type":"MultiPoint","coordinates":[]} |
| 00000000000000000003 | 041402011508 | 430611     | -760819     | 1005   | 43.061100006103516 | -76.08190155029297  | {"type":"MultiPoint","coordinates":[]} |

4. fixHUC.py deletes all rows where no HUC12 was found and drops the columns "system:index" and ".geo" which were added by the Google Earth Engine. In this process, 1 row (1004) gets dropped.

| HUC12        | LATITUDE | LONGITUDE | Number | fixed-LATITUDE     | fixed-LONGITUDE     |
| ------------ | -------- | --------- | ------ | ------------------ | ------------------- |
| 120401040303 | 2978037  | -956295   | 1001   | 29.780370712280277 | -95.62950134277344  |
| 140801011604 | 367452   | -1074455  | 1003   | 36.74520111083984  | -107.44550323486328 |
| 41402011508  | 430611   | -760819   | 1005   | 43.06110000610352  | -76.08190155029297  |

# Results

The results are stored in the "data/fixed-positions-huc.csv" file, where the latitude and longitude values are matched with their respective HUC12 value.

To create a HUC8 out of a HUC12 the last 4 digits can be removed:

120401040303 (HUC12) -> 12040104 (HUC8)
