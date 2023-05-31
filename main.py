# SAM Fileref: https://samtools.github.io/hts-specs/SAMv1.pdf
# Resource: DeBrujin: 
# https://eaton-lab.org/slides/genomics/answers/nb-10.2-de-Bruijn.html
import toyplot.browser

from DeBruijn import *
from Alignment import Alignment

# Helper function to determine if it is a header entry
def is_header(entry):
    if '@' in entry[0]:  # All varities of SAM headers begin with a @ followed by 2 char
        return True


def main():
    file = 'Data/PB644_EB817.hifi_reads.sam'

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

                        if alignment.IS_MAPPED:  # Prints mapped entries
                            print(alignment)

                            
                            #Find overlapping sequences
                            sequences = get_counts_from_seq(alignment.SEQ, k=50)
                            edges = get_edges(sequences)
                            
                            toyplot.browser.show(plot_debruijn_graph(edges)[0])

            lineCount += 1


if __name__ == "__main__":
    main()
