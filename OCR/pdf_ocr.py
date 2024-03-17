from ast import Delete
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
import pathlib
import os
import time


import pytesseract
from pdf2image import convert_from_path
from PIL import Image



"""
Optical Character Reading Program
Takes a PDF file and uses optical character reading to extract the information
input: pdf file 
output: giant string of text information from the pdf file
    - seperated with \n and \f for pages
"""
def ocr(fileName):
    start_time = time.time()
    #get file path for pytesseract
    #TODO: need to fix things here to run pytesseract on any computer
    cur_time = start_time
    convert_time = 0
    pages = []
    avg_pages = 0


    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        path_to_poppler_exe = r"C:\Users\User\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin"
    image_file_list = []
    with TemporaryDirectory() as tempdir:
        #pull current directory
        file = fileName.split('.')[0]
        parent_path = pathlib.Path(__file__).parent.resolve()
        newdirectory = "pat_" + file
        newpath= os.path.join(parent_path, newdirectory)
        ppath = os.path.join(parent_path, "media")
        currentpath = os.path.join(ppath, fileName)
        text_file = os.path.join(newpath, 'out_text.txt')
        #make directory to store patient information temporarily
        try:
            os.mkdir(newpath)
        except FileExistsError:
            print("Directory Exists")
        #convert pdf files to jpg <- different for windows vs. mac I think
        #TODO: test this part on different platform i.e. windows

        if platform.system() == "Windows":
            pdf_pages = convert_from_path(currentpath, dpi = 500, 
                output_folder = newpath, poppler_path = path_to_poppler_exe, fmt = 'jpg')
        else:
            pdf_pages = convert_from_path(currentpath, dpi = 500, output_folder = newpath, fmt='jpg')
        convert_time = time.time() - start_time
        f2 = open("imagetimes.txt", 'a')
        f2.write(str(convert_time) + '\n')
        f2.close()
        cur_time = time.time()
        #convery al diles to JPEG and store in image_file_list
        #not sure if I need this
        for page_enumeration, page in enumerate(pdf_pages, start = 1):
            filename = f"{tempdir}\page_{page_enumeration}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)
        
        #open output file to write to
        with open(text_file, 'a') as output_file:

            towrite = ''
            #run ocr for each image file
            for image_file in image_file_list:
                text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                text = text.replace("-\n", "")
                #write to output_file -> not sure why I'm doing this here
                output_file.write(text)
                towrite += text + '\f'
                #add page
                page_t = time.time() - cur_time
                cur_time = time.time()
                pages.append(page_t)
            #delete all the image files we made
            for image_file in image_file_list:
                os.remove(image_file)
            avg_pages = sum(pages)/len(pages)
            f = open("times.txt", 'a')
            for i in pages:
                f.write(str(i) + ' \n')
            f.close()
            print(f'Num Pages: {len(pages)}')
            print(f'Average Page Processing Time: {avg_pages:.4f}')
            print(f'Image Conversion Time: {convert_time:.3f}')
            print(f"Optical Character Reading Took: {(time.time() - start_time):.3f} seconds")
            return towrite
    return "Error"
