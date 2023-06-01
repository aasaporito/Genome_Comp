# SAM Fileref: https://samtools.github.io/hts-specs/SAMv1.pdf
# Resource: DeBrujin: 
# https://eaton-lab.org/slides/genomics/answers/nb-10.2-de-Bruijn.html
from DeBruijn import *
from Alignment import Alignment
from tests import *
from file_tools import *

import configparser

# Helper function to determine if it is a header entry
def is_header(entry):
    if '@' in entry[0]:  # All varities of SAM headers begin with a @ followed by 2 char
        return True

def process_data():
    config = configparser.ConfigParser()
    config.read('config.ini')

    files = get_files(str(config['DEFAULT']['data_path']))


    for file in files:

        with open(file, 'r') as infile:
            lineCount = 0

            for line in infile:

                match lineCount:
                    case 10000:
                        break  # Avoid reading the whole file, for now

                    case _:
                        entry = line.split("\t")
                        if not is_header(entry):
                            alignment = Alignment(entry)
                            # print(alignment)

                            if alignment.IS_MAPPED and int(alignment.MAP_QUALITY) <= 15:  # Prints mapped entries
                                print(alignment)

                                
                                #Find overlapping sequences
                                sequences = get_counts_from_seq(alignment.SEQ, k=int(config['DEFAULT']['kmer']))
                                #sequences = get_counts_from_seq("ATGGTATGTA", 3)
                                edges = get_edges(sequences)

                                g1 = generate_diGraph(edges)
                                if loop_test(g1):
                                    print("Loop found")
                                    save_graph(g1, alignment, file)
                                    
                                else:
                                    print("No loop found\n\n")

                lineCount += 1

def main():
    process_data()    
    #g1 = test_plot("ACTGAGTACCATGGAC",4)


if __name__ == "__main__":
    main()
