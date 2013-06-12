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
import shapefile, shutil


def LoadDataFile(jsonFile):

    with open(jsonFile) as f:
        jsonStr = ''
        for line in f:
            jsonStr = jsonStr + line
        global jsonObject
        jsonObject = json.loads(jsonStr)
        print jsonStr
        
def SaveShape(w):
    # save the shapefile
    # Create unique name
    dt = datetime.now()
    fileSafeStr = dt.strftime("%Y%m%d_%H%M%S")
    w.save('shapefiles/' + fileSafeStr)
    # copy WebMercator projection
    shutil.copy('4269.prj', 'shapefiles/' + fileSafeStr + '.prj')
    print 'Created shapefile ' + fileSafeStr + '.shp'
    
def WriteAttributes(features, w):
        # Itererate over the features to create attributes
    for feature in features:
        # Add the records
        print 'creating attributes'
        rec = feature["attributes"].values()
        w.record(*rec)
        
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
        x = feature["geometry"]["x"]
        y = feature["geometry"]["y"]
        w.point(x, y)
        #w.point(37.7793, -122.4192)
    # Create the fields
    WriteFields(fields, w)
    # Populate Attributes
    WriteAttributes(features, w)
    # Save the shapefile
    SaveShape(w)
        
def WritePolygons(features, fields):
    w = shapefile.Writer(shapefile.POLYGON)
    
    # Itererate over the features to create geometries
    for feature in features:        
        # Write the geometries
        geom = feature["geometry"]["rings"]
        w.poly(parts=geom)
    # Create the fields
    WriteFields(fields, w)
    # Populate Attributes
    WriteAttributes(features, w)
    # Save the shapefile
    SaveShape(w)

        
def WritePolylines(features, fields):
    w = shapefile.Writer(shapefile.POLYLINE)
    # Itererate over the features to create geometries and attributes
    for feature in features:        
        # Write the geometries
        geom = feature["geometry"]["paths"]
        w.poly(parts=geom)
                
    # Create the fields
    WriteFields(fields, w)
    # Populate Attributes
    WriteAttributes(features, w)
    # Save the shapefile
    SaveShape(w)

# Main Entry        
LoadDataFile('lineFeatures.json')

# Determine geometry type
print jsonObject["geometryType"]
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


