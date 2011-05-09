#! /usr/bin/env python

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from xml.dom.minidom import parseString
import csv

inputfile = "test.xml"
outputfile = "output.csv"
infile = open(inputfile, "r")
data = infile.read()
xmldoc = parseString(data)
infile.close()

McCabes = []
noStatements = []
noMethodsCalled = []
noMethods = 0
metricsrow = []
metricscsv = []
revision = "temp"

method_metrics = xmldoc.getElementsByTagName("method_metrics")
metricsTags = xmldoc.getElementsByTagName("method")

for file in method_metrics:
    noMethods += int(file.getAttribute("method_count"))
    
metricsrow.append("revision")
metricsrow.append("#nomethods")
metricsrow.append("mccabe")
metricsrow.append("#nostatements")
metricsrow.append("nomethodcalls")

metricscsv.append(metricsrow)

for method in metricsTags:
    if int(method.getElementsByTagName("complexity").item(0).firstChild.data) != 1550214256:
        McCabes.append(int(method.getElementsByTagName("complexity").item(0).firstChild.data))
    if int(method.getElementsByTagName("statements").item(0).firstChild.data) != 1550214256:
        noStatements.append(int(method.getElementsByTagName("statements").item(0).firstChild.data))
    if int(method.getElementsByTagName("calls").item(0).firstChild.data) != 1550214256:
        noMethodsCalled.append(int(method.getElementsByTagName("calls").item(0).firstChild.data))
        
for i in range(len(McCabes)):
    metricsrow = []
    metricsrow.append(revision)
    metricsrow.append(noMethods)
    metricsrow.append(McCabes[i])
    metricsrow.append(noStatements[i])
    metricsrow.append(noMethodsCalled[i])
    
    metricscsv.append(metricsrow)
    
outputline = ""

outfile = open(outputfile, "w")

for i in range(len(metricscsv)):
    for j in range(len(metricscsv[i])):
        outputline += str(metricscsv[i][j]) + ","
    outputline = outputline.rstrip(",")
    outputline += "\n"
    outfile.write(outputline)
    outputline = ""
    

outfile.close()

r = robjects.r

print "Mean McCabe: " + str(r.mean(robjects.IntVector(McCabes))[0])
print "Mean number of statements: " + str(r.mean(robjects.IntVector(noStatements))[0])
print "Mean number of methods called: " + str(r.mean(robjects.IntVector(noMethodsCalled))[0])

print

print "Median McCabe: " + str(r.median(robjects.IntVector(McCabes))[0])
print "Median number of statements: " + str(r.median(robjects.IntVector(noStatements))[0])
print "Median number of methods called: " + str(r.median(robjects.IntVector(noMethodsCalled))[0])

print

ineq = importr("ineq")

print "Coeffecient of Variation McCabe: " + str(ineq.var_coeff(robjects.IntVector(McCabes))[0])
print "Coeffecient of Variation number of statements: " + str(ineq.var_coeff(robjects.IntVector(noStatements))[0])
print "Coeffecient of Variation number of methods called: " + str(ineq.var_coeff(robjects.IntVector(noMethodsCalled))[0])

print

moments = importr("moments")

print "Skewness of McCabe: " + str(moments.skewness(robjects.IntVector(McCabes))[0])
print "Skewness of number of statements: " + str(moments.skewness(robjects.IntVector(noStatements))[0])
print "Skewness of number of methods called: " + str(moments.skewness(robjects.IntVector(noMethodsCalled))[0])

print 

print "Gini McCabe: " + str(ineq.Gini(robjects.IntVector(McCabes))[0])
print "Gini number of statements: " + str(ineq.Gini(robjects.IntVector(noStatements))[0])
print "Gini number of methods called: " + str(ineq.Gini(robjects.IntVector(noMethodsCalled))[0])

print

print "Theil McCabe: " + str(ineq.Theil(robjects.IntVector(McCabes))[0])
print "Theil number of statements: " + str(ineq.Theil(robjects.IntVector(noStatements))[0])
print "Theil number of methods called: " + str(ineq.Theil(robjects.IntVector(noMethodsCalled))[0])


