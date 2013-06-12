"""
exportShp.py
Converts JSON feature classes into shapefile using the shapefile.py created by jlawhed<at>geospatialpython.com
author: hector_cervantes<at>msn.com
date: 20130606
version: 1.0
Compatible with Python versions 2.4-3.x
"""
from datetime import datetime
import sys, os, json, urllib, urllib2
import shapefile, shutil, StringIO, zipfile

def ServiceRequest(url, values):    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    global jsonObject
    jsonObject = json.loads(the_page) 

def LoadDataFile(jsonFile):

    with open(jsonFile) as f:
        jsonStr = ''
        for line in f:
            jsonStr = jsonStr + line
        global jsonObject
        jsonObject = json.loads(jsonStr)
        
def SaveShape():
    # save the shapefile
    # Create unique name
    dt = datetime.now()
    fileSafeStr = dt.strftime("%Y%m%d_%H%M%S")
    w.save('shapefiles/' + fileSafeStr)
    # copy WebMercator projection
    shutil.copy('4269.prj', 'shapefiles/' + fileSafeStr + '.prj')
    print 'Created shapefile ' + fileSafeStr + '.shp'

def SaveShapeZip():
    # save the shapefile
    # Create unique name
    dt = datetime.now()
    fileSafeStr = dt.strftime("%Y%m%d_%H%M%S")
    
    # Set up buffers for saving
    shp = StringIO.StringIO()
    shx = StringIO.StringIO()
    dbf = StringIO.StringIO()
    # Save shapefile components to buffers
    w.saveShp(shp)
    w.saveShx(shx)
    w.saveDbf(dbf)
    # Save shapefile buffers to zip file 
    # Note: zlib must be available for
    # ZIP_DEFLATED to compress.  Otherwise
    # just use ZIP_STORED.
    z = zipfile.ZipFile('shapefiles/' + fileSafeStr + '.zip', 'w', zipfile.ZIP_DEFLATED)
    z.writestr(fileSafeStr + '.shp', shp.getvalue())
    z.writestr(fileSafeStr + '.shx', shx.getvalue())
    z.writestr(fileSafeStr + '.dbf', dbf.getvalue())
    # write the prj file
    prjStr = ''
    with open('4269.prj') as f:        
        for line in f:
            prjStr = prjStr + line
    z.writestr(fileSafeStr + '.prj', prjStr)  
    z.close()
    
    print 'Created shapefile ' + fileSafeStr + '.shp'
    
def WriteAttributes(features, w):
        # Itererate over the features to create attributes
    for feature in features:
        # Add the records
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
    global w
    w = shapefile.Writer(shapefile.POINT)    
    # Itererate over the features to create geometries
    print 'Constructing ' + str(len(features)) + ' features'
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
    SaveShapeZip()
        
def WritePolygons(features, fields):
    global w
    w = shapefile.Writer(shapefile.POLYGON)
    print 'Constructing ' + str(len(features)) + ' features'
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
    SaveShapeZip()

        
def WritePolylines(features, fields):
    global w
    w = shapefile.Writer(shapefile.POLYLINE)
    print 'Constructing ' + str(len(features)) + ' features'
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
    SaveShapeZip()
    
# Main Entry        
#LoadDataFile('lineFeatures.json')
url = 'http://sampleserver6.arcgisonline.com/arcgis/rest/services/Military/MapServer/4/query'
values = {'geometry' : '-137,-65,132,61',
    'geometryType' : 'esriGeometryEnvelope',
    'outSR' : '4269',
    'returnZ' : 'false',
    'returnM' : 'false',
    'spatialRel' : 'esriSpatialRelIntersects',
    'returnGeometry' : 'true',
    'f' : 'pjson'}
ServiceRequest(url, values)

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


