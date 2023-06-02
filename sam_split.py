import glob, os
from Alignment import Alignment
from file_tools import is_header

def split_sam():
    files = glob.glob("*.sam")
    char_count = 0
    file_count = 0
    out = []
    header = ""
    for file in files:
        with open(file, 'r') as infile:
            for line in infile:
                entry_list = line.split("\t")
                
                if is_header(entry_list):
                    header = line
                    out.append(line)
                    char_count += len(line)
                    print("Header written to stream")
                else:
                    alignment = Alignment(entry_list)
                    if (alignment.IS_MAPPED and int(alignment.MAP_QUALITY) <= 15):  # Prints mapped entries
                        del alignment
                        out.append(line)
                        char_count += len(line)
                        #print("Entry written to stream")

                if file_split(char_count, out):
                    #Removes sam ext
                    f = open("pre-processed/" + "".join((file.split('.')[0:-1])) + "_pp_" + str(file_count) + ".sam", 'w')
                    for line in out:
                        f.write("%s" % line)

                    f.close()
                    print("File saved")

                    char_count = 0
                    out = []
                    file_count += 1

                    #Store header in every entry
                    out.append(header)
                    char_count += len(line)
                    print("Header written to stream")

        f = open("pre-processed/" + "".join((file.split('.')[0:-1])) + "_pp_" + str(file_count) + ".sam", 'w')
        for line in out:
            f.write("%s" % line)

        f.close()
        print("File saved")

        # Reset counters for new read in file
        char_count = 0
        out = []
        file_count = 0
                    

def file_split(char_count, out):
    CHAR_TO_GB = 1000000000 # 100,000,000 char = 100 MB
    if char_count >= CHAR_TO_GB:
        return True
    else:
        return False

def setup():
    path = "pre-processed"

    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        print("Created directory: " + path)

def main():
    setup()
    split_sam()


if __name__ == "__main__":
    main()