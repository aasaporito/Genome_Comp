class Alignment:

	"""Represents an single SAM file entry. Not all possible attributes are accounted for
	For full attribute classifications, reference SAM File formatting.
	https://samtools.github.io/hts-specs/SAMv1.pdf
	
	Attributes:
	    CIGAR (str): * Indicates no CIGAR available
	    FLAG (str): An unmapped entry map be classified by a 4 for FLAG.
	    IS_MAPPED (bool): Indicates if the alignment contains a DNA sequence
	    LENGTH (int): Observed template length
	    MAP_QUALITY (int): Quality of the mapping. 255 indicates unavailable map quality.
	    NAME (str): Query name
	    NEXT_POS (int): Position of next read. 0 indicates unavailable.
	    NEXT_SEQ_NAME (str): Name of next sequence. * indicates unavailable
	    POSITION (int): Position. 0 indicates unavailable.
	    QUALITY (str): ASCII representation of quality (+33). * indicates unavailable.
	    REF_SEQ_NAME (str): Reference sequence name
	    SEQ (str): Segment sequence
	"""
	
	NAME = ""
	FLAG = ""	
	
	REF_SEQ_NAME = ""	
	POSITION = 0		
	MAP_QUALITY = 255 	
	CIGAR = "" 			
	
	NEXT_SEQ_NAME = "" 
	NEXT_POS = 0 		
	
	LENGTH = 0			
	SEQ = "" 			
	QUALITY = ""		
	
	IS_MAPPED = True
	
	def __init__(self, entry):
		"""Standard constructor
		
		Args:
		    entry String: A complete alignment entry in SAM v1 format
		"""
		self.NAME = entry[0]
		self.FLAG = entry[1]
		self.REF_SEQ_NAME  = entry[2]
		self.POSITION = entry[3]
		self.MAP_QUALITY = entry[4]
		self.CIGAR = entry[5]
		self.NEXT_SEQ_NAME = entry[6]
		self.NEXT_POS = entry[7]
		self.LENGTH = entry[8]
		self.SEQ = entry[9]
		self.QUALITY = entry[10]
		
		if self.FLAG == '4' or self.SEQ == "*":
			self.IS_MAPPED = False
	
	def __repr__(self):
		"""Summary
		
		Returns:
		    TYPE: String
		"""
		return "Alignment()"
		
	def __str__(self):
		""" Displays the contents of an alignment.
		
		Returns:
		    TYPE: String
		"""
		out = " Name: {} \n Flag: {} \n REF_SEQ: {} \n POS: {} \n Quality: {} \n CIGAR: {} \n NEXT_SEQ_NAME: {} \n NEXT_POS: {} \n LENGTH: {} \n QUALITY: {} \n" \
		.format(self.NAME, self.FLAG, self.REF_SEQ_NAME, self.POSITION, self.MAP_QUALITY, self.CIGAR, \
		self.NEXT_SEQ_NAME, self.NEXT_POS, self.LENGTH, self.QUALITY) #Does not print DNA Sequence
		return out
	
	