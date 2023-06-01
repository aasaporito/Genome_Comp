"""Summary
	Supplies various file read/write related helper functions.
"""
import os
import glob


def get_files(path):
	"""Summary
		Finds all .sam files within a directory specified in config.ini
	Args:
	    path (str): The folder within the working directory storing .sam files.
	
	Returns:
	    list: A list of all .sam files within the directory.
	"""
	os.chdir(path)
	files = glob.glob("*.sam")
	os.chdir("..")

	full_path = [] #Full path from working directory.
	for file in files:
		full_path.append(path + "/" + file)
	return full_path


def generate_output_path(sam_name, alignment):
	"""Summary
		Creates an output path for a given SAM entry. 
		Additionally, any "/" in samFileName are replaced with '__'

		Save paths followe the format: Output/samFileName_alignmentName_alignmentMapQuality.png
	Args:
	    sam_name (str): Name of the current .sam file.
	    alignment (Alignment): The Alignment object to create a save path for.
	
	Returns:
	    str: The output path starting at the working directory
	"""
	path = (sam_name.split('.')[0]).split("/")
	path.remove("Data")
	path = "/".join(path)
	file_name = "Output/" + path + "_" + alignment.NAME.replace("/", "__") + "_" + alignment.MAP_QUALITY + ".png"

	return file_name

#TODO Log file generation