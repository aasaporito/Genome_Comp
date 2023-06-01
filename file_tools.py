import os, glob

def get_files(path):
	os.chdir(path)
	files = glob.glob("*.sam")
	os.chdir("..")

	full_path = []
	for file in files:
		full_path.append(path + "/" + file)
	return full_path