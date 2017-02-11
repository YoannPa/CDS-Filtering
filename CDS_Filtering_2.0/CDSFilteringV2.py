#!/usr/bin/python
# -*- coding: utf8 -*-

##CDS Filtering version 2.0

__author__ = "Yoann PAGEAUD"
__version__  = "2.0.0"
__copyright__ = "2017 KnopLab, ZMBH - Universität Heidelberg, Germany"
__date__ = "2017/01"
__mail__ = "yoann.pageaud@gmail.com"

'''This script aims at parsing and filtering CDS contained in a (multi)Fasta
file. This is the version 2.0 of the script 'CDS Filtering'. 
The version 1.0 is available to downloads at : 
researchgate.net/publication/303910491_CDS_Filtering_Program'''


#IMPORTS
import argparse
import os 
import re
import sys


#PARSER
parser= argparse.ArgumentParser() #initiate the parser
#Necessary arguments for the program

parser.add_argument("CDS_List", type=argparse.FileType('r'),\
help = "Path to the file containing your CDSs (No header in the file).")
parser.add_argument("Temp_File1", type=str,\
help = "Name of the 1st temporary file.")
parser.add_argument("Temp_File2", type=str,\
help = "Name of the 2nd temporary file.")
parser.add_argument('Output_File',type=str,\
help='Name of the output file that will contain your list of CDS.')
parser.add_argument('Summary_File',type=str,\
help='Name of the summary file that will contain parameters you selected.')

#Facultative Argument for the program 
parser.add_argument('-m','--minimum_length',type=int, default = 0,\
help='Minimum value for the length of the CDS (has to be an integer > or = 0).')
parser.add_argument('-M','--Maximum_length',type=int, default = 1000,\
help='Maximum value for the length of the CDS (has to be an integer > or = 0).')

args=parser.parse_args()


#REGEX
motif = r"(^[atugcnrykmswbdhvATUGCNRYKMSWBDHV]+)"
motif_comp = re.compile(motif)


#VARIABLES
countCDSbegin = 0
countCDSend = 0
countCDSremoved = 0
maxremoved = 0
minremoved = 0
multipleremoved=0


#CDS EXTRACTION
#This part extract all the CDS from the file.

temporary1 = open(args.Temp_File1,'a')

for line in args.CDS_List :
    retour = motif_comp.match(line)
    if retour != None :
        print >> temporary1, retour.group(1)
        
temporary1.close()


#MULTIPLE IDENTICAL CDS FILTER
'''This part allow you to delete all the lines identical to a line which has\
already been read'''

temporary1 = open(args.Temp_File1,"r")
temporary2 = open(args.Temp_File2,"w")

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
temporary1.close()


#MINIMUM/MAXIMUM TRESHOLDS FILTER & CDS COUNTERS
#This part allow you to delete all the CDS below a minimum and above a maximum. 
#It also produce statistics.

temporary1 = open(args.Temp_File1,"r") 

for line in temporary1:
    if len(line) >= 1:
        countCDSbegin=countCDSbegin+1

temporary2 = open(args.Temp_File2,"r")
output = open(args.Output_File,'w')

for line in temporary2:
    if len(line) > args.minimum_length : 
        if len (line) < args.Maximum_length+1 :
            print >> output, ">cds"+str(countCDSend+1)
            countCDSend=countCDSend+1
            print >> output, line,
        else:
            maxremoved=maxremoved+1
    else:
        minremoved=minremoved+1

countCDSremoved = countCDSbegin - countCDSend
multipleremoved = countCDSremoved - maxremoved - minremoved


#RESULTS PRINTERS

print ""
print "************************************************************************"
print ""
print "Done! Your CDS list has been filtered."

summary = open(args.Summary_File,'w')

print >> summary, "Summary of your CDS Filtering:"
print >> summary, "------------------------------------------------------------"
print >> summary, ""
print >> summary, "Your Parameters:"
print >> summary, "    Minimum length allowed for a CDS: ", args.minimum_length
print >> summary, "    Maximum length allowed for a CDS: ", args.Maximum_length
print >> summary, "------------------------------------------------------------"
print >> summary, ""
print >> summary, "Your Results:"
print >> summary, "    Your input file contained", countCDSbegin, "CDS."
print >> summary, "    Your new CDS List file contain", countCDSend, "CDS."
print >> summary, ""
print >> summary, "    ", countCDSremoved, "CDS were removed."
print >> summary, "        ", minremoved, "CDS were shorter than the minimum."
print >> summary, "        ", maxremoved, "CDS were longer than the maximum."
print >> summary, "        ", multipleremoved, "CDS appeared multiple time."


#CLOSE FILES

temporary2.close()
output.close()
temporary1.close()
os.remove(args.Temp_File1)
os.remove(args.Temp_File2)


#REFERENCE
print >> summary, ""
print >> summary, "************************************************************"
print >> summary, "How to cite : Yoann Pageaud. 'CDS Filtering in Python'."\
+ "KnopLab, ZMBH - Universität Heidelberg. 2017."
summary.close()