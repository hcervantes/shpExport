"""
exportShp.py
Converts JSON feature classes into shapefile using the shapefile.py created by jlawhed<at>geospatialpython.com
author: hector_cervantes<at>msn.com
date: 20130606
version: 1.0
Compatible with Python versions 2.4-3.x
"""
from datetime import datetime
import sys, os, json
import shapefile

def WriteFields(fields, w):
    # Write the fields
   
    for field in fields:
        fieldType = field["type"]
        # get the lenght if exists
        fldLen = False
        if("length" in field.keys()):
            fldLen = field["length"] 
        fieldType = fieldType.upper()
        if("GEOMETRY"  in fieldType):
            continue            
        elif("INTEGER" in fieldType):
            fieldType = "I"
        elif("string" in fieldType):
            fieldType = "C"                
        elif("DATE" in fieldType):
            fieldType = "D"
        elif("DOUBLE" in fieldType or "OID" in fieldType):
            fieldType = "N"
        else:
            fieldType = "C"
        # Now create the field
        if(fldLen != False):
            w.field(str(field["name"]), str(fieldType), str(fldLen))
        else:
            w.field(str(field["name"]), str(fieldType))
        print 'created field: ' + field['name'] + ' - fieldType: ' + fieldType
def WritePoints(features, fields):
    w = shapefile.Writer(shapefile.POINT)
    
    # Itererate over the features to create geometries
    for feature in features:        
        # Write the geometries
        print "creating geometry "
        x = feature["geometry"]["x"]
        y = feature["geometry"]["y"]
        print str(x) + ',' + str(y)
        w.point(x, y)
        #w.point(37.7793, -122.4192)
    # Create the fields
    WriteFields(fields, w)
    #w.field('FIRST_FLD')
    #w.field('SECOND_FLD', 'C', '40')
    # Itererate over the features to create attributes
    for feature in features:
        # Add the records
        print 'creating attributes'
        rec = feature["attributes"].values()
        print rec
        w.record(*rec)
        #w.record('crap', 'crap2')
    # save the shapefile
    # Create unique name
    dt = datetime.now()
    fileSafeStr = dt.strftime("%Y%m%d_%H%M%S")
    w.save('shapefiles/test/poly' + fileSafeStr)
    print 'Created shapefile ' + fileSafeStr + '.shp'
        
def WritePolygons(features, fields):
    w = shapefile.Writer(shapefile.POLYGON)
    # Create the fields
    WriteFields(fields, w)
    # Itererate over the features to create geometries
    for feature in features:        
        # Write the geometries
        print "creating geometry "
        print feature["geometry"]["rings"]
        geom = feature["geometry"]["rings"]
        w.poly(parts=geom)
    # Itererate over the features to create attributes
        # Add the records
        print 'creating attributes'
        rec = feature["attributes"].values()
        print rec
        w.record(*rec)
    # save the shapefile
    # Create unique name
    dt = datetime.now()
    fileSafeStr = dt.strftime("%Y%m%d_%H%M%S")
    w.save('shapefiles/test/poly' + fileSafeStr)
        
def WritePolylines(features, fields):
    w = shapefile.Writer(shapefile.POLYGON)
    # Create the fields
    WriteFields(fields, w)
    # Itererate over the features to create geometries and attributes
    for feature in features:        
        # Write the geometries
        geom = feature["geometry"]
        w.poly(parts=geom)
                
        # Add the records
        rec = feature["attributes"]
        w.record(rec)
        
        # save the shapefile
        w.save('shapefiles/test/poly')

# Main Entry        
if (len(sys.argv) == 0):
    print 'Expected Featureset as argument'
    exit
jsonInput = sys.argv[0]

jsonInput = u'''{
 "displayFieldName": "STATE_FIPS",
 "fieldAliases": {
  "STATE_FIPS": "STATE_FIPS"
 },
 "geometryType": "esriGeometryPoint",
 "spatialReference": {
  "wkid": 4269,
  "latestWkid": 4269
 },
 "fields": [
  {
   "name": "STATE_FIPS",
   "type": "esriFieldTypeString",
   "alias": "STATE_FIPS",
   "length": 2
  }
 ],
 "features": [
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.95355599980951,
    "y": 32.196335999706662
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.929658000316408,
    "y": 32.198095999930501
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.922701999697495,
    "y": 32.209736909031164
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.942107999784298,
    "y": 32.218989091073752
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.916962000296053,
    "y": 32.194589090913894
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.979262909155921,
    "y": 32.174601090967599
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -87.983266000225683,
    "y": 32.174265999975944
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -88.008253999622355,
    "y": 32.19314709096551
   }
  },
  {
   "attributes": {
    "STATE_FIPS": "01"
   },
   "geometry": {
    "x": -88.010408000029145,
    "y": 32.227608000209102
   }
  }
 ]
}'''

jsonObject = json.loads(jsonInput)

# Determine geometry type
geomType = jsonObject["geometryType"]
geomType = geomType.upper()

if 'POLYGON' in geomType:
    geomType = shapefile.POLYGON
    WritePolygons(jsonObject["features"], jsonObject["fields"])
elif 'LINE' in geomType:
    geomType = shapefile.POLYLINE
    WritePolylines(jsonObject["features"], jsonObject["fields"])
elif 'POINT' in geomType:
    geomType = shapefile.POINT
    WritePoints(jsonObject["features"], jsonObject["fields"])


# Create the shapefile writer
#w = shapefile.Writer(geomType)


