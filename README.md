shpExport
=========

PHP &amp; Python export JSON/Feature classes to shapefile
shpExport.py is a Python method to export ArcGIS Server services to a shapefile. This uses pyshp available at https://code.google.com/p/pyshp/ to create the binary shp, dbf, and shx files.  
I wrote this b/c unlike Geoserver, ArcGIS Server does not have an easy way of exporting shapefile without the use of a GP service.  This is a basic python script that reads the output of an ArcGIS Server query request, and transforms them into a shapefile.  The next step is to zip, the shapefile binary files and send that request to the user to download it.  
I am not familiar with Python, but I’ve started this script in hopes someone with more Py knowledge can fine-tune it.  It is my intent to pass in the results of a ArcGIS Server query and export as shapefile.  Another option is to save the results to a file (like I’m doing here), then as a parameter to the shpExport.py, pass in the path to the file.  I was thinking of calling this script from a PHP service.
A typical ArcGIS server request looks like this:
http://sampleserver6.arcgisonline.com/arcgis/rest/services/Military/MapServer/4/query?where=&text=&objectIds=&time=&geometry=-137.28515625%2C+-65.65827452000002%2C+132.5390625%2C+61.01572481400001%0D%0A&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=4269&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=pjson
….and the output looks like this:
{
 "displayFieldName": "uniquedesignation",
 "fieldAliases": {
  "uniquedesignation": "Unique Designation"
 },
 "geometryType": "esriGeometryPolyline",
 "spatialReference": {
  "wkid": 4269,
  "latestWkid": 4269
 },
 "fields": [
  {
   "name": "uniquedesignation",
   "type": "esriFieldTypeString",
   "alias": "Unique Designation",
   "length": 50
  }
 ],
 "features": [
  {
   "attributes": {
    "uniquedesignation": null
   },
   "geometry": {
    "paths": [
     [
      [
       -119.94105143199999,
       35.435935336999989
      ],
      [
       -119.42768272000001,
       35.435340471000018
      ],
      [
       -119.19925446299999,
       35.498991052999997
      ]
     ]
    ]
   }
  }]
}

Comments, suggestions and critics are welcome. 
