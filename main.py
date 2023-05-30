#SAM Fileref: https://samtools.github.io/hts-specs/SAMv1.pdf

from Alignment import Alignment

# Helper function to determine if it is a header entry
def is_header(entry):
	if '@' in entry[0]: #All varities of SAM headers begin with a @ followed by 2 char
		return True
		
def main():
	file = 'Data/PB644_EB817.hifi_reads.sam'

	with open(file, 'r') as infile:
		lineCount  = 0
		
		for line in infile:
			
			match lineCount:
				case 10000:
					break # Avoid reading the whole file, for now
				
				case _:
					entry = line.split("\t")
					if not is_header(entry):
						alignment = Alignment(entry)
						#print(alignment)
						
						if alignment.IS_MAPPED: #Prints mapped entries
							print(alignment)
			lineCount += 1
		
if __name__ == "__main__":
	main()
	
	
