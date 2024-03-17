#PDF Extraction Import

import os
try:
    os.system('pip --version')
except:
    os.system('python get-pip.py')
try:
    from pdfminer.high_level import extract_text
except:
    os.system("pip install pdfminer.high_level")
#Comandline Import
import sys, getopt
#pdf image processing import
try:
    import platform
except:
    os.system("pip install platform")
try:
    from tempfile import TemporaryDirectory
except:
    os.system("pip install tempfile")
try:
    from pathlib import Path
except:
    os.system("pip install pathlib")
try:
    import pytesseract
except:
    os.system("pip install pytesseract")
try:
    from pdf2image import convert_from_path
except:
    os.system("pip install pdf2image")
try:
    from PIL import Image
except:
    os.system("pip install PIL")

from pdf_ocr import *
from parser_1 import *
try:
    import time
except:
    os.system("pip install time")
try:
    import ast
except:
    os.system("pip install ast")
try:
    import csv
except:
    os.system("pip install csv")
try:
    import re
except:
    os.system("pip install re")
try:
    import shutil
except:
    os.system("pip install shutil")
  
# Source path
parent = pathlib.Path(__file__).parent.resolve()
tessdoc = "Tesseract-OCR"
source = os.path.join(parent, tessdoc)
  
# Destination path
# if platform.system() == "Windows":

#         destination = (r"C:\Program Files")
#         try:
#             dest = shutil.move(source, destination)
#         except shutil.Error:
#             pass

  
# Move the content of
# source to destination

#import sqlite3 as sq

#INSTALLS NEEDED
"""
pytesseract
pillow
pdf2image
pdfminer
poppler-utils
"""

def main(argv):
    print(argv)
    print(argv)
    start_time = time.time()
    inputFile = ''
    outputFile = ''
    argumentssize = len(argv)
    #get input and output file from command line arguments
    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("File Error: Arguments Not Found.")
        print("Aborting Program")
        sys.exit(2)
    
    for opt, arg in opts:
      if opt == '-h':
         print ('usage: pdf_processor.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputFile = arg
      elif opt in ("-o", "--ofile"):
         outputFile = arg

    #check on input and output file 
    if outputFile == '':
        outputFile = 'patient_'+inputFile
    if inputFile == '':
        print("File Error: Input File Not Found In Arguments.")
        print("Aborting Program.")
        sys.exit(2)
    #print(f"Input File: {inputFile}\nOutput File: {outputFile}")
    parent_path = pathlib.Path(__file__).parent.resolve()
    newpath = "media"
    parent_path = os.path.join(parent_path, newpath)
    currentpath = os.path.join(parent_path, inputFile + ".pdf")
    try:
        pdffile = open(currentpath, 'rb')
    except:
        pdffile = open(currentpath.replace('pdf', "PDF"), 'rb')



    #EXTRACT TEXT METHOD
    text = ""
    #try extract text method 
    try:
        text = extract_text(pdffile)
        pdffile.close()
    except FileNotFoundError:
        print("File Not Found. Ensure Input File Is In Current Directory.")
        print("Aborting Program.")
        sys.exit(2)
    newtext = text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\f', '')
    
    # run ocr if extract text failed
    if newtext == '':
        print("Extract Text Failed. Running OCR Method. ")
        text = ocr(inputFile + '.pdf')
    
    

    
    f = open(outputFile + '.txt', 'w')
    f.write(text)#, "pat_" + inputFile)
    
    f.close()
    
    parser(text, inputFile)

    
    #make dictionary of patient information
    # patient_info = [
    #     {'Patient Name:':""}, 

    #     {"Primary Insurance:": "",
    #     "Insurance Name:": "",
    #     "ID #:": ""},
        
    #     {"Secondary Insurance;": "",
    #     "Insurance Name:": "",
    #     "ID #:":""}
    #     ]
    # for i in patient_info:
    #     #go through keys
    #     keys = i.keys()
    #     #find first key index
    print(f"Total run time: {(time.time() - start_time):.3f} seconds")

if __name__ == "__main__":
   #print(sys.argv)
   main(sys.argv)
