import os
import glob


def get_files(path):
	os.chdir(path)
	files = glob.glob("*.sam")
	os.chdir("..")

	full_path = []
	for file in files:
		full_path.append(path + "/" + file)
	return full_path


def generate_output_path(sam_name, alignment):
	path = (sam_name.split('.')[0]).split("/")
	path.remove("Data")
	path = "/".join(path)
	file_name = "Output/" + path + "_" + alignment.NAME.replace("/", "__") + "_" + alignment.MAP_QUALITY + ".png"

	return file_name

#TODO Log file generation