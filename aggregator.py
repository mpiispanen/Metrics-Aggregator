#! /usr/bin/env python

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from xml.dom.minidom import parseString
import csv

inputfile = "input.xml"
outputfile = "output.csv"
infile = open(inputfile, "r")
data = infile.read()
xmldoc = parseString(data)
infile.close()

#Lists that hold the metric data
McCabes = []
noStatements = []
noMethodsCalled = []
noMethods = 0
metricsrow = []
metricscsv = []
revision = "temp"

#Aggregated metrics
meanMcCabe = None
meanNoStatements = None
meanNoMethodCalls = None

medianMcCabe = None
medianNoStatemens = None
medianNoMethodCalls = None

coeffMcCabe = None
coeffNoStatemens = None
coeffNoMethodCalls = None

skewnessMcCabe = None
skewnessNoStatemens = None
skewnessNoMethodCalls = None

gininMcCabe = None
giniNoStatemens = None
giniNoMethodCalls = None

theilMcCabe = None
theilNoStatemens = None
theilNoMethodCalls = None

method_metrics = xmldoc.getElementsByTagName("method_metrics")
metricsTags = xmldoc.getElementsByTagName("method")

#Write metrics to a CSV file

for file in method_metrics:
    noMethods += int(file.getAttribute("method_count"))
    
metricsrow.append("revision")
metricsrow.append("#nomethods")
metricsrow.append("mccabe")
metricsrow.append("#nostatements")
metricsrow.append("nomethodcalls")

metricscsv.append(metricsrow)

#Parse XML and ignore incorrect metrics from SourceMonitor
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
ineq = importr("ineq")
moments = importr("moments")


#Aggregate metrics
meanMcCabe = r.mean(robjects.IntVector(McCabes))[0]
meanNoStatements = r.mean(robjects.IntVector(noStatements))[0]
meanNoMethodCalls = r.mean(robjects.IntVector(noMethodsCalled))[0]

medianMcCabe =r.median(robjects.IntVector(McCabes))[0]
medianNoStatements = r.median(robjects.IntVector(noStatements))[0]
medianNoMethodCalls = r.median(robjects.IntVector(noMethodsCalled))[0]

coeffMcCabe = ineq.var_coeff(robjects.IntVector(McCabes))[0]
coeffNoStatements = ineq.var_coeff(robjects.IntVector(noStatements))[0]
coeffNoMethodCalls = ineq.var_coeff(robjects.IntVector(noMethodsCalled))[0]

skewnessMcCabe = moments.skewness(robjects.IntVector(McCabes))[0]
skewnessNoStatements = moments.skewness(robjects.IntVector(noStatements))[0]
skewnessNoMethodCalls = moments.skewness(robjects.IntVector(noMethodsCalled))[0]

giniMcCabe = ineq.Gini(robjects.IntVector(McCabes))[0]
giniNoStatements = ineq.Gini(robjects.IntVector(noStatements))[0]
giniNoMethodCalls = ineq.Gini(robjects.IntVector(noMethodsCalled))[0]

theilMcCabe = ineq.Theil(robjects.IntVector(McCabes))[0]
theilNoStatements = ineq.Theil(robjects.IntVector(noStatements))[0]
theilNoMethodCalls = ineq.Theil(robjects.IntVector(noMethodsCalled))[0]

print "Mean McCabe: " + str(meanMcCabe)
print "Mean number of statements: " + str(meanNoStatements)
print "Mean number of methods called: " + str(meanNoMethodCalls)

print

print "Median McCabe: " + str(medianMcCabe)
print "Median number of statements: " + str(medianNoStatements)
print "Median number of methods called: " + str(medianNoMethodCalls)

print

print "Coeffecient of Variation McCabe: " + str(coeffMcCabe)
print "Coeffecient of Variation number of statements: " + str(coeffNoStatements)
print "Coeffecient of Variation number of methods called: " + str(coeffNoMethodCalls)

print

print "Skewness of McCabe: " + str(skewnessMcCabe)
print "Skewness of number of statements: " + str(skewnessNoStatements)
print "Skewness of number of methods called: " + str(skewnessNoMethodCalls)

print 

print "Gini McCabe: " + str(giniMcCabe)
print "Gini number of statements: " + str(giniNoStatements)
print "Gini number of methods called: " + str(giniNoMethodCalls)

print

print "Theil McCabe: " + str(theilMcCabe)
print "Theil number of statements: " + str(theilNoStatements)
print "Theil number of methods called: " + str(theilNoMethodCalls)

outputAggregated = "aggregated.csv"

#Print aggregated metrics to a CSV file
outfile = open(outputAggregated, "w")

outputline = "Revision,Number of Methods,"
outputline += "Mean McCabe,Mean Number of Statements,Mean Number of Method Calls,"
outputline += "Median McCabe,Median Number of Statements,Median Number of Method Calls,"
outputline += "Coeffecient of Variation McCabe,Coeffecient of Variation Number of Statements,Coeffecient of Variation Number of Method Calls,"
outputline += "Skewness McCabe,Skewness Number of Statements,Skewness Number of Method Calls,"
outputline += "Gini McCabe,Gini Number of Statements,Gini Number of Method Calls,"
outputline += "Theil McCabe,Theil Number of Statements,Theil Number of Method Calls\n"

outfile.write(outputline)

outputline = "RevisionPlaceHolder," + str(noMethods) + "," + str(meanMcCabe) + "," + str(meanNoStatements) + "," + str(meanNoMethodCalls) + ","
outputline += str(medianMcCabe) + "," + str(medianNoStatements) + "," + str(medianNoMethodCalls) + ","
outputline += str(coeffMcCabe) + "," + str(coeffNoStatements) + "," + str(coeffNoMethodCalls) + ","
outputline += str(skewnessMcCabe) + "," + str(skewnessNoStatements) + "," + str(skewnessNoMethodCalls) + ","
outputline += str(giniMcCabe) + "," + str(giniNoStatements) + "," + str(giniNoMethodCalls) + ","
outputline += str(theilMcCabe) + "," + str(theilNoStatements) + "," + str(theilNoMethodCalls)

outfile.write(outputline)

outfile.close()
