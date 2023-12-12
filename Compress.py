import io
import math
import sys
import numpy as np
from PIL import Image
import os
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import fitz
from fpdf import FPDF
import argparse
import glob
from fpdf import FPDF
import os

#------------------------------------Create PDF-------------------------------------------
def create_pdf_from_images(image_folder, output_file):
    # Get a list of image files in the folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # Create a PDF object
    pdf = FPDF()

    # Iterate over the image files
    for image_file in image_files:
        # Add a page to the PDF
        pdf.add_page()

        # Calculate image dimensions to fit the page
        page_width = pdf.w - 2 * pdf.l_margin
        page_height = pdf.h - 2 * pdf.t_margin

        # Add the image to the PDF without resizing or modification
        pdf.image(os.path.join(image_folder, image_file), x=pdf.l_margin, y=pdf.t_margin,
                  w=page_width, h=page_height)

    # Save the PDF to the output file
    pdf.output(output_file)


# ----------------------------------Compress Image---------------------------------------------

def JPEGSaveWithTargetSize(im, filename,target):
    """Save the image as JPEG with the given name at best quality that makes less than "target" bytes"""

    # Min and Max quality
    count=1

    Qmin, Qmax = 1, 96

    # Highest acceptable quality found

    Qacc = -1

    while Qmin <= Qmax:

        m = math.floor((Qmin + Qmax) /2)

        # Encode into memory and get size

        buffer = io.BytesIO()

        im.save(buffer, format="JPEG", quality=m)

        s = buffer.getbuffer().nbytes
        
        #print("s is ", s)
        #target = (int)(s *(int)(size)/100)
        #print(target)
        #target = s*factor
        

        if s <= target:#2

            Qacc = m

            print("Qacc:",Qacc)
            Qmin = m + 1

        elif s > target:#3

            Qmax = m - 1

        

        # Write to disk at the defined quality

        
        if Qacc <= -1:
            
            #print("ERROR: No acceptble quality factor found", file=sys.stderr,)
            print(f"filename:with {s} rejected", filename,":",s,":",target)
            print(Qacc)
            im.save(filename, format="JPEG", quality=m)
            #print("saved", filename)

        else:
            im.save(filename, format="JPEG", quality=Qacc)#1
            print("saved", filename,s,":",target)
            print(count)
            count=count+1
#------------------------------Get Factor------------------------------------------------
def GetFactor(folder_path,size):
	total_size = 0
	count=0
	#folder_path='/home/server/Desktop/Image_Enchance/enhance_search/FcraCompress/FCRA_IMAGES'
	for dirpath, dirnames, filenames in os.walk(folder_path):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)
			total_size += os.path.getsize(file_path)
			count+=1

	#size=total_size
	print(total_size)
	factor=(int)((.01*total_size*(int)(size))/count if 8/total_size!=0 else (.01*total_size*(int)(size))/count) 
	return factor
# --------------------------Main Function ------------------------------


def main():
    # Create an ArgumentParser object
	parser = argparse.ArgumentParser(description="first input and then output path.")
    
    # Add arguments for image folder and output file
	parser.add_argument("image_folder", help="Path to the folder containing images.")
	parser.add_argument("output_file", help="Output PDF file path.")
	parser.add_argument("size", help="compression size 0 to 100.")
	
    
    # Parse the command-line arguments
	args = parser.parse_args()
	#print(args.image_folder,":",args.output_file,":",args.Quality)
    
	img_outpath=os.getcwd()+'/tempImages1'
	if not os.path.exists(img_outpath):
		os.makedirs(img_outpath)
	
	#Getting Factor()
	factor=GetFactor(args.image_folder,args.size)

	'''outpath=args.image_folder
	file_list = os.listdir(outpath)
	for path in file_list:
		inpath=outpath+"/"+path
		
		for images in path:
			image =inpath + '/' + images
			#outpath= img_outpath+ images[:-4] +"converted"+images[-4:]'''
	file_extensions = ['.jpg', '.jpeg', '.png']		
	for root, _, files in os.walk(args.image_folder):
		for file in files:
            # Check if the file has one of the specified image extensions
			if os.path.splitext(file)[1].lower() in file_extensions:
                # Get the full path of the image file
				image_path = os.path.join(root, file)
				outt= img_outpath+"/"+file[:-4]+'converted'+file[-4:]
				im = Image.open(image_path)
				#im = Image.open(image)
				print(factor)
				JPEGSaveWithTargetSize(im, outt,factor)
	#output_file=os.getcwd()
	#print(img_outpath)
	create_pdf_from_images(img_outpath, args.output_file)		

if __name__ == "__main__":
    main()
			
