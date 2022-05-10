var positions = ee.FeatureCollection(
  "projects/ee-lniehaus/assets/fixed-positions-ll"
);
var table = ee.FeatureCollection("USGS/WBD/2017/HUC12");

// Do something to every element of a collection.
// can not be a normal for loop with setting some variables
// https://developers.google.com/earth-engine/guides/debugging#mapped-functions
var withMoreProperties = positions.map(function (f) {
  // Set Latitude and Longitude
  var lat = f.get("fixed-LATITUDE");
  var lon = f.get("fixed-LONGITUDE");
  var point = ee.Geometry.Point([lon, lat]);

  // 2: get HUC associated with the location
  var HUC = table.filterBounds(point);

  // Normal If-Else constructs can not be used since this code gets executed on the server
  // https://developers.google.com/earth-engine/guides/client_server#conditionals
  var size = HUC.size();
  var serverConditional = ee.Algorithms.If(
    // size is a number, but gets cast into a Boolean
    size,
    // get HUC code
    f.set("HUC12", ee.Feature(HUC.first()).getString("huc12")),
    // If HUC Code not avaiable, set it to -1
    f.set("HUC12", -1)
  );

  return serverConditional;
});

// Save the data as csv
// https://developers.google.com/earth-engine/guides/exporting#to-drive_1
Export.table.toDrive({
  collection: withMoreProperties,
  description: "positions-huc",
  fileFormat: "CSV",
});
