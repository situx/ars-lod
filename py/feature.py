__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2021, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "thiery@rgzm.de"
__status__ = "beta"
__update__ = "2021-11-09"

# import dependencies
import pandas as pd
import os
import codecs
import datetime
import importlib  # py3
import sys
import json

# set UTF8 as default
importlib.reload(sys)  # py3
# reload(sys) #py2

# uncomment the line below when using Python version <3.0
# sys.setdefaultencoding('UTF8')

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set input csv
csv = "features1.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\src\\csv") + "\\" + csv

print(file_in)

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep='|',
    usecols=['obj', 'feature', 'label', 'ftype', 'n_ftype', 'mantype', 'geom']

)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []
for index, row in data.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 10000 == 0:
        print(tmpno)
    lineNo += 1
    lines.append("ars:feat_" + str(row['feature']) + " " + "rdf:type" + " lado:Feature .")
    lines.append("ars:feat_" + str(row['feature']) + " " + "rdfs:label" + " " + "'" + str(row['label']).replace('\'', '`').replace('\\', '') + "'" + ".")
    if str(row['mantype']).replace('\'', '`') != 'nan':
        if str(row['mantype']).replace('\'', '`') != 'undefined':
            lines.append("ars:feat_" + str(row['feature']) + " " + "lado:madeByString" + " " + "'" + str(row['mantype']).replace('\'', '`') + "'@en" + ".")
    lines.append("ars:feat_" + str(row['feature']) + " " + "lado:hasType" + " " + "lado:" + str(row['n_ftype']) + "" + ".")
    lines.append("ars:feat_" + str(row['feature']) + " " + "dc:identifier" + " " + "'" + str(row['feature']) + "'" + ".")
    lines.append("ars:ic_" + str(row['obj']) + " " + "lado:carries" + " " + "ars:feat_" + str(row['feature']) + ".")
    # geom
    geomstr = str(row['geom']).replace('\'', '\"')
    geomjson = json.loads(geomstr)
    lines.append("ars:feat_" + str(row['feature']) + " " + "geosparql:hasGeometry" + " ars:feat_" + str(row['feature']) + "_geom .")
    lines.append("ars:feat_" + str(row['feature']) + " " + "lado:selectedArea" + " ars:feat_" + str(row['feature']) + "_geom .")
    lines.append("ars:feat_" + str(row['feature']) + "_geom " + "rdf:type" + " sf:Polygon .")
    geom_sel = "\"<http://archaeology.link/ontology#Local3DCoordinateSystem> " + str(geomjson["selectionpolygon"]) + "\"^^geosparql:wktLiteral"
    lines.append("ars:feat_" + str(row['feature']) + "_geom " + "geosparql:asWKT " + geom_sel + ".")
    # prov-o
    lines.append("ars:feat_" + str(row['feature']) + " " + "prov:wasAttributedTo" + " ars:ImportPythonScript_ARS3D .")
    lines.append("ars:feat_" + str(row['feature']) + " " + "prov:wasDerivedFrom" + " <http://www.wikidata.org/entity/Q105268778> .")
    lines.append("ars:feat_" + str(row['feature']) + " " + "prov:wasGeneratedBy" + " ars:activity_feat_" + str(row['feature']) + " .")
    lines.append("ars:activity_feat_" + str(row['feature']) + " " + "rdf:type" + " <http://www.w3.org/ns/prov#Activity> .")
    lines.append("ars:activity_feat_" + str(row['feature']) + " " + "prov:startedAtTime '" + starttime + "'^^xsd:dateTime .")
    lines.append("ars:activity_feat_" + str(row['feature']) + " " + "prov:endedAtTime '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "'^^xsd:dateTime .")
    lines.append("ars:activity_feat_" + str(row['feature']) + " " + "prov:wasAssociatedWith" + " ars:ImportPythonScript_ARS3D .")
    lines.append("")

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing turtle files...")

f = 0
step = 100000
fileprefix = "feature_"
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX geosparql: <http://www.opengis.net/ont/geosparql#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX sf: <http://www.opengis.net/ont/sf#> \r\n"
prefixes += "PREFIX lado: <http://archaeology.link/ontology#> \r\nPREFIX ars: <http://data.archaeology.link/data/ars/> \r\nPREFIX wd: <http://www.wikidata.org/entity/> \r\n PREFIX pelagios: <http://pelagios.github.io/vocab/terms#> \r\nPREFIX oa: <http://www.w3.org/ns/oa#> \r\nPREFIX dcterms: <http://purl.org/dc/terms/> \r\nPREFIX foaf: <http://xmlns.com/foaf/0.1/> \r\nPREFIX relations: <http://pelagios.github.io/vocab/relations#> \r\nPREFIX cnt: <http://www.w3.org/2011/content#> \r\nPREFIX pleiades: <http://pleiades.stoa.org/places/> \r\nPREFIX amt: <http://academic-meta-tool.xyz/vocab#> \r\n"
prefixes += "\r\n"
for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\data") + "\\" + fileprefix + strX + ".ttl"
    file = codecs.open(filename, "w", "utf-8")
    file.write("# create triples from " + csv + " \r\n")
    file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
    file.write(prefixes)
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print("Yuhu! > " + fileprefix + strX + ".ttl")
    file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
