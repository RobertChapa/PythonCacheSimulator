import sys

from math import log

# Count the arguments
argCount = len(sys.argv) - 1


def processCommands():

	##################################################################################################
	##################################################################################################
	##################################################################################################

	traceFileName = ""
	cacheSize = -1
	blockSize = -1
	associativity = -1
	replacementMethod = ""

	for x in range(1, len(sys.argv)):
		if sys.argv[x] == "-f":
			traceFileName = sys.argv[x+1]
		if sys.argv[x] == "-s":
			cacheSize = int(sys.argv[x+1])
		elif sys.argv[x] == "-b":
			blockSize = int(sys.argv[x+1])
		elif sys.argv[x] == "-a":
			associativity = int(sys.argv[x+1])
		elif sys.argv[x] == "-r":
			replacementMethod = sys.argv[x+1]

	print("\nCache Simulator CS 3853 Spring 2021 - Group #1\n")

	print(f"Trace File: {traceFileName}\n")
	print("***** Cache Input Parameters *****")
	print(f"Cache Size:\t\t\t{cacheSize} KB\n" + 
		f"Block Size:\t\t\t{blockSize} bytes\n" +
		f"Associativity:\t\t\t{associativity}\n" +
		f"Replacement Policy:\t\t{replacementMethod}\n")


	numOfBlocks = int(cacheSize * 1024 / blockSize)
	numOfRows = int(numOfBlocks / associativity)
	indexSize = int(log(numOfRows, 2))
	offsetSize = int(log(blockSize, 2))

	tagSize = 32 - indexSize - offsetSize

	overheadSize = pow(2, tagSize) + pow(2, indexSize)

	# cacheSize + validbytes + tagbytes
	memorySize = cacheSize * 1024 + numOfBlocks * (tagSize + 1) / 8

	cost = round(memorySize / 1024 * 0.09, 2)


	print("***** Cache Calculated Values *****\n")

	print(f"Total # Blocks:\t\t\t{numOfBlocks}\n" + 
		f"Tag Size:\t\t\t{tagSize} bits\n" +
		f"Index Size:\t\t\t{indexSize} bits\n" +
		f"Total # Rows:\t\t\t{numOfRows}\n" +
		f"Overhead Size:\t\t\t{overheadSize} bytes\n" +
		f"Implementation Memory Size:\t{memorySize / 1024} KB ({memorySize} bytes)\n" + 
		f"Cost:\t\t\t\t${cost}\n")


	# print("***** Memory Addresses *****\n")

	# f = open(f"{traceFileName}", "r")

	# count = 0
	# for line in f:
	# 	if "EIP" in line:
	# 		print(f"0x{line[10:18]}: ", end="") # characters 10 through 18 (exclusive) is address
	# 		print(f"(00{line[5:7]})") # character 5 and 6 is the length
	# 		count += 1
	# 	elif "dstM" in line:
	# 		if line[6:14] != "00000000":
	# 			print(f"0x{line[6:14]}: (0004)") # characters 10 through 18 (exclusive) is address
	# 			count += 1
	# 		if line[33:41] != "00000000":
	# 			print(f"0x{line[33:41]}: (0004)") # characters 10 through 18 (exclusive) is address
	# 			count += 1
	# 	if count >= 20: 
	# 		break
	# f.close()

	##################################################################################################
	##################################################################################################
	##################################################################################################



	#############################			Assignment 2			##############################

	cacheAccesses = 0
	cacheHits = 0
	cacheMisses = 0
	compMisses = 0
	confMisses = 0

	print("\n***** CACHE SIMULATION RESULTS *****\n")

	print(f"Total Cache Accesses:\t{cacheAccesses}\n" +
		f"Cache Hits:\t\t{cacheHits}\n" +
		f"Cache Misses:\t\t{cacheMisses}\n" +
		f"--- Compulsory Misses:\t{compMisses}\n" +
		f"--- Conflict Misses:\t{confMisses}\n")





	hitRate = 0
	missRate = 0
	CPI = 0
	unusedCacheSpace = 0
	unusedCacheBlocks = 0

	print("\n***** ***** CACHE HIT & MISS RATE: ***** *****\n")

	print(f"Hit Rate:\t\t{hitRate}%\n" +
		f"Miss Rate:\t\t{missRate}%\n" +
		f"CPI:\t\t\t{CPI} Cycles/Instruction\n" +
		f"Unused Cache Space:\t{unusedCacheSpace}\n" +
		f"Unused Cache Blocks:\t{unusedCacheBlocks}\n")


def main():
	processCommands()

if __name__ == "__main__":
	main()

