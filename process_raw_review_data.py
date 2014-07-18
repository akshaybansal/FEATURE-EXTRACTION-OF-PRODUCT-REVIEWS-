# BEFORE RUNNING THIS FILE CREATE A FOLDER NAMED 'list of products' IN THE SAME DIRECTORY AS THIS FILE
# AND REPLACE THE 'main_filename' variable with the file name of the file containing the reviews

import os

"""
	This file takes data from review file and classifies the data into files with names as their respective product ids.
	For this script to run successfully the review data should have the following mandatory fields:
		product/productId: followed by a semi colon and the id of the respective product
		product/name: this field contains the name of product(s) belonging to the id above
		review/text: this field contains the review of the above product. also for each and every review this field should be present in the end followed by a new line before a new review is begun!

	This script also creates a new file that maps the respective product ids to thier names for using later for specification of product while evaluating reviews.

	If review file does not follow this pattern then use the 'feature extraction.py' script for tagging and classification!
"""
review_data_file_name = "Cell_Phones_&_Accessories.txt"		  # The file in the current directory that conains the raw review data

try:
	fin = open(review_data_file_name, "r")
except IOError:
	print "Input Output Error Occured. Could Not Open File. Press Any Key To Stop Execution Of Script"
	raw_input()
	exit()

if not os.path.isdir('list of products'):
	os.makedirs('list of products')

f_map = open('product names.txt', 'w')

# Initiating variables

line = fin.readline()
output_file_name, review_output_file = "", None
fileno, file_array, new_file_flag = 0,  [], False 

while line:
	try:
		line = line.split(":")
		if line[0].split("/")[1] == "productId":
			if output_file_name != line[1].strip():
				new_file_flag = True
				if review_output_file:
					review_output_file.close()
				output_file_name = line[1].strip()
				review_output_file = open("list of products/"+output_file_name+".txt", "a")

				if output_file_name not in file_array:				# mentaining a progress report of how much processing of the raw data has been completed
					progress_report_file_object = open("Progress report.txt", "w") # opening a file that keeps a track of the progress
					progress_report_file_object.write("File "+str(fileno)+" complete!") 		
					fileno += 1
					file_array.append(output_file_name)
					progress_report_file_object.close()								# closing the progress report file

		elif new_file_flag and line[0].split('/')[1] == "title":
			new_file_flag = False
			f_map.write(output_file_name + ":" + line[1].strip() + "\n")

		elif line[0].split('/')[1] == "text":
			review_output_file.write(line[1].strip())
			review_output_file.write("\n")		
			fin.readline()
		line = fin.readline()
	except IndexError:
		print "The raw review data is not specified in the given format. Please make sure it is present in the required format."
		print "For more details about the format of the raw review data, refer to the demo_review_data.txt"
		raw_input("Press any key to end the execution of the current script")
		exit() 
fin.close()
raw_input("Script run successful. \nThe raw data has been processed for further analysis. Press any key to continue...")

