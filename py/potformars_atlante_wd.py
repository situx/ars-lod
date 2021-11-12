__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2021, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "thiery@rgzm.de"
__status__ = "beta"
__update__ = "2021-11-12"

# import dependencies
import pandas as pd
import os
import codecs
import datetime
import importlib  # py3
import sys
from SPARQLWrapper import SPARQLWrapper2

# set UTF8 as default
importlib.reload(sys)  # py3
# reload(sys) #py2

# uncomment the line below when using Python version <3.0
# sys.setdefaultencoding('UTF8')

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set input from SPARQL endpoint
sparql = SPARQLWrapper2("https://java-dev.rgzm.de/rdf4j-server/repositories/ars3d-lod")
sparql.setQuery("""
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ars: <http://ars3D/documentation/ontology/arsonto#>
    PREFIX lado: <http://archaeology.link/ontology#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    SELECT DISTINCT ?pf ?creator ?label ?bc (GROUP_CONCAT(DISTINCT ?image; SEPARATOR=",") AS ?images) WHERE {
    ?pf rdfs:label ?label.
    ?pf lado:derivedFrom wd:Q109525400.
    ?pf lado:createdBy ?creator.
    ?pf dcterms:bibliographicCitation ?bc.
    OPTIONAL {
  	?obj lado:representedBy ?pf.
  	?obj lado:hasConditionString "complete"@en .
    ?obj lado:hasImage ?image.
    }
    } GROUP BY ?pf ?creator ?label ?bc
""")

lines = []
for result in sparql.query().bindings:

    print("*****************************************")
    # QS
    lines.append("CREATE")
    lines.append("LAST" + "\t" + "Len" + "\t" + "\"" + result["label"].value + "\"")
    pages = result["bc"].value.split(".")[1]
    pages = pages.strip()
    if "-" in pages:
        lines.append("LAST" + "\t" + "Den" + "\t" + "ceramic form in Atlante (1981), pp." + pages + "\"")
    else:
        lines.append("LAST" + "\t" + "Den" + "\t" + "ceramic form in Atlante (1981), p." + pages + "\"")
    lines.append("LAST" + "\t" + "P31" + "\t" + "Q109532996")
    lines.append("LAST" + "\t" + "P31" + "\t" + "Q838948")
    lines.append("LAST" + "\t" + "P361" + "\t" + "Q109525400")  # Atlante Book
    lines.append("LAST" + "\t" + "P361" + "\t" + "Q105268778")
    lines.append("LAST" + "\t" + "P170" + "\t" + result["creator"].value.replace("http://www.wikidata.org/entity/", ""))  # Atlante Intitute
    lines.append("LAST" + "\t" + "P195" + "\t" + "Q109525400")  # Atlante Book
    lines.append("LAST" + "\t" + "P304" + "\t" + "\"" + pages + "\"")
    images = result["images"].value.split(",")
    for img in images:
        if "zenodo" in img:
            print("P6500", img, "S248", "Q105268778")
            lines.append("LAST" + "\t" + "P6500" + "\t" + "\"" + img + "\"" + "\t" + "S248" + "\t" + "Q105268778")
    lines.append("LAST" + "\t" + "P2888" + "\t" + "\"" + result["pf"].value + "\"" + "\t" + "S248" + "\t" + "Q105268778")
# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing QS files...")

f = 0
step = 100000
fileprefix = "create_pf_atlante"
filename = dir_path.replace("py", "wikidata") + "\\quickstatements\\" + fileprefix + ".qs"
print(filename)
file = codecs.open(filename, "w", "utf-8")
for i, line in enumerate(lines):
    if (i > f - 1 and i < f + step):
        file.write(line)
        file.write("\r\n")
f = f + step
print("Yuhu! > " + fileprefix + ".qs")
file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
