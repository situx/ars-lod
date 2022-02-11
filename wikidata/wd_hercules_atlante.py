__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2022, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@rgzm.de"
__status__ = "beta"
__update__ = "2022-12-11"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib  # py3
import sys

# set UTF8 as default
importlib.reload(sys)  # py3
# reload(sys) #py2

# uncomment the line below when using Python version <3.0
# sys.setdefaultencoding('UTF8')

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set input csv
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set input csv
file_name = "wd_hercules_atlante.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path + "\\" + file_name

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep='|',
    usecols=['id', 'page', 'feature', 'wc'],
    na_values=['.', '??']  # take any '.' or '??' values as NA
)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []
for index, row in data.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 10 == 0:
        print(tmpno)
    lineNo += 1
    # QS
    lines.append("CREATE")
    lines.append("LAST" + "\t" + "Len" + "\t" + "\"" + str(row["id"]) + "\"")
    pages = str(row["page"])
    if "-" in pages:
        lines.append("LAST" + "\t" + "Den" + "\t" + "\"iconographic description in Atlante (1981), pp." + pages + "\"")
    else:
        lines.append("LAST" + "\t" + "Den" + "\t" + "\"iconographic description in Atlante (1981), p." + pages + "\"")
    lines.append("LAST" + "\t" + "P31" + "\t" + "Q109525730")
    lines.append("LAST" + "\t" + "P31" + "\t" + "Q838948")
    lines.append("LAST" + "\t" + "P361" + "\t" + "Q109525400")  # Atlante Book (1981)
    lines.append("LAST" + "\t" + "P361" + "\t" + "Q105268778")
    lines.append("LAST" + "\t" + "P170" + "\t" + "Q3803714")
    lines.append("LAST" + "\t" + "P195" + "\t" + "Q109525400")  # Atlante Book (1981)
    lines.append("LAST" + "\t" + "P304" + "\t" + "\"" + pages + "\"")
    if str(row['feature']) != 'nan':
        lines.append("LAST" + "\t" + "P6500" + "\t" + "\"" + "https://zenodo.org/record/5645237/files/" + str(row["feature"]) + ".png " + "\"" + "\t" + "S248" + "\t" + "Q105268778")
    if str(row['wc']) != 'nan':
        lines.append("LAST" + "\t" + "P18" + "\t" + "\"" + "" + str(row["wc"]).replace("_", " ") + "\"" + "\t" + "S248" + "\t" + "Q105268778")

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing QS file")

f = 0
step = 100000
fileprefix = "wd_hercules_atlante"
for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\ttl") + "\\" + fileprefix + ".qs"
    file = codecs.open(filename, "w", "utf-8")
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print("Yuhu! > " + fileprefix + strX + ".txt")
    file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
