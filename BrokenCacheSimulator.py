import sys
import numpy
import re

from math import log

# Count the arguments
argCount = len(sys.argv) - 1

totalCycles = 0

# CACHE SIMULATION RESULT variables
cacheAccesses = 0
cacheHits = 0
cacheMisses = 0
compMisses = 0
confMisses = 0

# CACHE HIT & MISS RATE variables
hitRate = 0
missRate = 0
CPI = 0
unusedCacheSpace = 0
unusedCacheBlocks = 0

rr = []

def blk(tagbits, a):
	s = ''
	t = '0'
	u = ''
	for y in range(tagbits):
		s = s+'X'
	t = t + s
	for y in range(a):
		u = u + t
	u = u + 'R'
	return u

def send(cache, tag, index, offset):
	print(cache[0])
	temp = cache[int(index, 16)]#the current set
	nxt = len(tag) #length of a block
	ttl = len(temp) # length of the set

	n = 1
	k = 0
	r = ''
	j = len(tag)

	while(n):
		rt = '1' + tag
		lt = 0

		if temp[k] == '0':#if the valid bit is 0, add tag into cache
			#cache[int(index, 16)] = '1' + tag + temp[(nxt+1):]
			r = temp[0:k] + rt + temp[(j+1):]
			rt = len(r)-1
			r = r[0:rt] + str(int(((j+1)/(len(tag)+1))))
			rr.append(r[-1:])
			cache[int(index, 16)] = r
			print('comp miss on block '+ str((j/4)))
			compMisses = compMisses + 1
			n=0
		elif (temp[k] == '1') and (temp[(k+1):(j+1)] == tag):#if valid bit is 1 and tag matches, hit
			print('hit on block '+ str((j/4)))
			cacheHits = cacheHits + 1
			n=0
		elif (temp[k] == '1') and (temp[(k+1):(j+1)] != tag):#move to check next block
			k = k + len(tag) + 1
			j = j + len(tag) + 1
		else:
			rep = int(rr[0])
			rr.pop(0)
			k = (rep * 1)-1
			j = (rep * 5)-1
			r = temp[0:k] + rt + temp[(j+1):]
			rt = len(r)-1
			r = r[0:rt] + str(int(((j+1)/(len(tag)+1))))
			rr.append(r[-1:])
			cache[int(index, 16)] = r
			print('conflict miss on block '+ str((j/4)))
			confMisses = confMisses + 1
			n=0



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

	tbits = tagSize
	ibits = indexSize
	rang = numOfRows

	cache = {}#the cache array

	for i in range(rang):#make empty cache
		cache[i] = blk(tbits, associativity)
		#print(cache[i])
		#print(i)

	print("***** Memory Addresses *****\n")
	try:
		f = open(f"{traceFileName}", "r")
	except FileNotFoundError:
		print(f"File {traceFileName} not found.")
		sys.exit(2)

	##################################################################################################
	##################################################################################################
	##################################################################################################



	#############################			Assignment 2			##############################

	totalCycles = 0

	rows = int(cacheSize/associativity)
	cache = dict()
	for row in range(0, rows):
		fullCache = []
		for blocks in range (0, associativity):
			rowContent = ['0', '00000000']
			fullCache.append(rowContent)
		cache[row] = fullCache

	# print(cache)

	#print(f"\t\t\t\t\t\t\t\t\t\tCache is a {rows}x{associativity}")


	count = 0
	for line in f:
		count += 1
	f.close()

	numOfinstructions = count // 3


	EIP = re.compile(r'EIP\s\((\d{2})\):\s(\w{8})')
	dstSrc = re.compile(r'dstM:\s(\w{8})\s.{8}\s\s\s\ssrcM:\s(\w{8})')

	count = 0

	try:
		f = open(traceFileName, "r")
	except FileNotFoundError:
		print(f"File {traceFileName} not found.")
		sys.exit(2)

	lst = []
	for line in f:
		isEIP = EIP.search(line.rstrip())
		isDstSrc = dstSrc.search(line.rstrip())

		if isEIP:
			instructionLength = int(isEIP.group(1))
			instructionAddress = hex(int(isEIP.group(2), 16))

			# converts address to binary and adds zeroes in beginning to have full 32 bits
			binary = (bin(int(isEIP.group(2), 16)))[2:].zfill(32)
			# print(binary)

			# print(f"\nTagsize: {tagSize}\nIndex: {indexSize}\nOffset: {offsetSize}")
			# assigns tag, index, and offset bits
			tagBits = binary[:tagSize+1]
			indexBits = binary[tagSize+1:-offsetSize+1]
			offsetBits = binary[-offsetSize:]

			# store address in list 
			lst.append({'tag':tagBits, 'index': indexBits, 'offset': offsetBits})
			#lst.append({hex(int(tagBits, 2)), hex(int(indexBits, 2)), hex(int(offsetBits, 2))})

			# print(f"\ntagBits: {tagBits}\nindexBits: {indexBits}\noffsetBits: {offsetBits}")

		elif isDstSrc:
			dst = isDstSrc.group(1)
			src = isDstSrc.group(2)

			# add number of cycles for this instruction
			if dst != "00000000" and src != "00000000":
				totalCycles += 2
			elif dst != "00000000" or src != "00000000":
				totalCycles += 1
		else:
			# line is empty... thus perform actual cache calculations with the addresses in the lst
			pass


		# if "EIP" in line:
		# 	count += 1
		# elif "dstM" in line:
		# 	if line[6:14] != "00000000":
		# 		count += 1
		# 	if line[33:41] != "00000000":
		# 		count += 1
	f.close()

	lont = 0

	#print('CATCH ME :' + str(cache[0]))

	for val in lst:
		sol = repr(val)
		fst = str(sol[9:26])
		nrt = str(sol[39:51])
		brt = str(sol[65:69])

		m = '{:0{}X}'.format(int(fst, 2), len(fst) // 4)
		l = '{:0{}X}'.format(int(nrt, 2), len(nrt) // 4)
		p = '{:0{}X}'.format(int(brt, 2), len(brt) // 4)
		#print('lont ' + str(lont))
		send(cache, m, l, p)
		lont = lont + 1

		#print((fst))
		#print(m)
		#print((nrt))
		#print(l)
		#print((brt))
		#print(p)
		
		#send(cache, 'val', 
		#print(f"{val}\n")


	# addresses are: tag | index | offset

	print("\n***** CACHE SIMULATION RESULTS *****\n")

	print(f"Total Cache Accesses:\t{cacheAccesses}\n" +
		f"Cache Hits:\t\t{cacheHits}\n" +
		f"Cache Misses:\t\t{cacheMisses}\n" +
		f"--- Compulsory Misses:\t{compMisses}\n" +
		f"--- Conflict Misses:\t{confMisses}\n")




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

