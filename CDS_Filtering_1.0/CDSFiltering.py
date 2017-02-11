#!/usr/bin/python
# -*- coding: utf8 -*-

##CDS FILTERING :
#Copyright 2016 KnopLab, ZMBH - Universität Heidelberg, Germany
#Author : Yoann PAGEAUD - yoann.pageaud@gmail.com
#Runs under Python Version 2.7.11

##IMPORT PACKAGE
import os 
import re

##FILES & PARAMETERS DEFINITION
print "1- Paste below (-6) the path you want to open your file (You will find it by clicking the adress bar of your window)."
print "2- Replace all the <\> by </> in the path."
print "3- Don't forget to type the extension of your file (.txt .fasta ...) at the end of the path."
print "4- Do not encompass the path with quotation mark."
print "5- If your dataset contain a Title or Column Names above your CDS sequences, please delete it."

path=raw_input("6- Paste and modify the path to your input file here: ")
CDSEXONSfile = open(path,"r")

temp1=raw_input("7- Type the path to the folder where you want the first temporary file to be located and its name (it will be delete after the filtering): ")
temporary1 = open(temp1,"w")

temp2=raw_input("8- Type the path to the folder where you want the second temporary file to be located and its name (it will be delete after the filtering): ")
temporary2 = open(temp2,"w")

res=raw_input("9- Type the path to the folder where you want your output file to be saved and the name of your output file: ")
listCDS = open(res,"w")

minimum = input("10- Enter the minimal value you want for the length of the CDS in your input file: ")

maximum = input("11- Enter the maximal value you want for the length of the CDS in your input file: ")

info=raw_input("12- Type the path to the folder where you want your Results and Parameters to be safed and the name of your informations file: ")
summaryfilter = open(info,"w")

##REGULAR EXPRESSION
motif = r"(^[atugcnrykmswbdhvATUGCNRYKMSWBDHV]+)"
motif_comp = re.compile(motif)

##VARIABLES INITIALIZATION
countCDSbegin = 0
countCDSend = 0
countCDSremoved = 0
maxremoved = 0
minremoved = 0
multipleremoved=0

##CDS EXTRACTION
#This part extract all the CDS from the file.

for line in CDSEXONSfile :
    retour = motif_comp.match(line)
    if retour != None :
        print >> temporary1, retour.group(1)
temporary1.close()

##MULTIPLE IDENTICAL CDS FILTER
#This part allow you to delete all the lines identical to a line which has already been read.

temporary1 = open(temp1,"r")

def filtering(cdslist):
    unique = {}
    result = []
    countmultiple = 0
    for cds in cdslist:
        if cds.strip() in unique: 
            continue
        unique[cds.strip()] = 1
        result.append(cds)
    countmultiple = countmultiple + 1
    return result

filelines = temporary1.readlines()
temporary2.writelines(filtering(filelines))

temporary2.close()

##MINIMUM/MAXIMUM TRESHOLDS FILTER & CDS COUNTERS
#This part allow you to delete all the CDS below a minimum and above a maximum, and to produce statistical results.
 
temporary1=open(temp1,"r")

for line in temporary1:
    if len(line) >= 1:
        countCDSbegin=countCDSbegin+1

temporary2 = open(temp2,"r")

for line in temporary2:
    if len(line) > minimum : 
        if len (line) < maximum+1 :
            print >> listCDS, ">cds"+str(countCDSend+1)
            countCDSend=countCDSend+1
            print >> listCDS, line,
        else:
            maxremoved=maxremoved+1
    else:
        minremoved=minremoved+1

countCDSremoved = countCDSbegin - countCDSend
multipleremoved = countCDSremoved - maxremoved - minremoved

##RESULTS PRINTERS
print ""
print "***************************************"
print ""
print "Done! Your CDS list has been filtered."
print >> summaryfilter, "Summary of your CDS Filtering:"
print >> summaryfilter, "-------------------------------------------------"
print >> summaryfilter, ""
print >> summaryfilter, "Your Parameters:"
print >> summaryfilter, "    Minimum length allowed for a CDS: ", minimum
print >> summaryfilter, "    Maximum length allowed for a CDS: ", maximum
print >> summaryfilter, "-------------------------------------------------"
print >> summaryfilter, ""
print >> summaryfilter, "Your Results:"
print >> summaryfilter, "    Your input file contained", countCDSbegin, "CDS."
print >> summaryfilter, "    Your new CDS List file contain", countCDSend, "CDS."
print >> summaryfilter, ""
print >> summaryfilter, "    ", countCDSremoved, "CDS were removed from your CDS list."
print >> summaryfilter, "        ", minremoved, "CDS were shorter than the minimal value you entered."
print >> summaryfilter, "        ", maxremoved, "CDS were longer than the maximal value you entered."
print >> summaryfilter, "        ", multipleremoved, "CDS were represented more than one time."

##CLOSE FILES
temporary2.close()
listCDS.close()
temporary1.close()
os.remove(temp1)
os.remove(temp2)

##REFERENCE
print >> summaryfilter, ""
print >> summaryfilter, "***************************************************************************"
print >> summaryfilter, "How to cite : Yoann Pageaud. 'CDS Filtering in Python'. KnopLab, ZMBH - Universität Heidelberg. 2016."
summaryfilter.close()