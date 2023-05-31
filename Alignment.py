class Alignment:
	NAME = ""
	FLAG = ""				# 4 indicates unmapped [no value for name position, cigar or quality]
	
	REF_SEQ_NAME = ""	# * indicates unavailable
	POSITION = 0			# 0 unmapped without coordinates
	MAP_QUALITY = 255 	#255 indicates unavailable
	CIGAR = "" 			# * indicates unavailable
	
	NEXT_SEQ_NAME = "" 	# * indicates unavailable
	NEXT_POS = 0 		#0 indicates unavailable
	
	LENGTH = 0			#Observed template length
	SEQ = "" 			#DNA Sequence
	QUALITY = ""			# * indicates unstored quality. ASCII of quality + 33
	
	IS_MAPPED = True
	
	def __init__(self, entry):
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
		
		if self.FLAG == '4':
			self.IS_MAPPED = False
	
	def __repr__(self):
		return "Alignment()"
		
	def __str__(self):
		out = " Name: {} \n Flag: {} \n REF_SEQ: {} \n POS: {} \n Quality: {} \n CIGAR: {} \n NEXT_SEQ_NAME: {} \n NEXT_POS: {} \n LENGTH: {} \n QUALITY: {} \n" \
		.format(self.NAME, self.FLAG, self.REF_SEQ_NAME, self.POSITION, self.MAP_QUALITY, self.CIGAR, \
		self.NEXT_SEQ_NAME, self.NEXT_POS, self.LENGTH, self.QUALITY) #Does not print DNA Sequence
		return out
	
	