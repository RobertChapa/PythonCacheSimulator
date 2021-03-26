import sys

from math import log

# Count the arguments
argCount = len(sys.argv) - 1


def processCommands():
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

	print(f"Trade File:{traceFileName}\n")
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
	cost = 0




	print("***** Cache Calculated Values *****\n")

	print(f"Total # Blocks:\t\t\t{numOfBlocks}\n" + 
		f"Tag Size:\t\t\t{tagSize} bits\n" +
		f"Index Size:\t\t\t{indexSize} bits\n" +
		f"Total # Rows:\t\t\t{numOfRows}\n" +
		f"Overhead Size:\t\t\t{overheadSize} bytes\n" +
		f"Implementation Memory Size:\t{memorySize / 1024} KB ({memorySize} bytes)\n" + 
		f"Cost:\t\t\t\t${cost}\n")

def main():
	processCommands()

if __name__ == "__main__":
	main()

