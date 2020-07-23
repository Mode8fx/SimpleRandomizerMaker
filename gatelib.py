def makeChoice(question, choices, allowMultiple=False):
	numChoices = len(choices)
	if numChoices == 0:
		print("Warning: A question was asked with no valid answers. Returning None.")
		return None
	if numChoices == 1:
		print("A question was asked with only one valid answer. Returning this answer.")
		return choices[0]
	print("\n"+question)
	for i in range(numChoices):
		print(str(i+1)+": "+choices[i])
	cInput = input().split(" ")
	if not allowMultiple:
		try:
			assert len(cInput) == 1
			choice = int(cInput[0])
			assert choice > 0 and choice <= numChoices
			return choice
		except:
			print("Invalid input.")
			return makeChoice(question, choices, allowMultiple)
	else:
		try:
			choices = [int(c) for c in cInput]
			for choice in choices:
				assert choice > 0 and choice <= numChoices
			return choices
		except:
			print("Invalid input.")
			return makeChoice(question, choices, allowMultiple)

def makeChoiceNumInput(question, minVal, maxVal):
	while True:
		print("\n"+question)
		try:
			var = float(input())
			assert minVal <= var <= maxVal
			return var
		except:
			print("Invalid input.")

def encodeSeed(varArray, maxValueArray, base=10):
	if base > 36:
		print("Base must be between 2 and 36. Lowering to 36.")
		base = 36
	seed = 0
	baseShift = 0
	for i in range(len(varArray)):
		seed += varArray[i]<<baseShift
		baseShift += maxValueArray[i].bit_length()
	return seed, dec_to_base(seed, base)

def decodeSeed(seed, maxValueArray, base=10):
	if base > 36:
		print("Base must be between 2 and 36. Lowering to 36.")
		base = 36
	if type(seed) is str:
		seed = int(seed, base)
	baseShift = 0
	varArray = []
	for i in range(len(maxValueArray)):
		bitLength = maxValueArray[i].bit_length()
		varArray.append((seed>>baseShift) & ((2**bitLength)-1))
		baseShift += bitLength
	return varArray

# values in maxValueArray start from 0
def verifySeed(seed, maxValueArray, base=10):
	if base > 36:
		print("Base must be between 2 and 36. Lowering to 36.")
		base = 36
	if type(seed) is int:
		base = 10
		seed = dec_to_base(seed,base)
	seed = seed.upper().strip()

	try:
		maxSeed = 0
		baseShift = 0
		for i in range(len(maxValueArray)):
			maxSeed += maxValueArray[i]<<baseShift
			baseShift += maxValueArray[i].bit_length()
		assert int(seed, 36) <= maxSeed
		varsInSeed = decodeSeed(seed, maxValueArray, base)
		for i in range(len(varsInSeed)):
			assert 0 <= varsInSeed[i] <= maxValueArray[i]
		return True
	except:
		return False

# taken from https://www.codespeedy.com/inter-convert-decimal-and-any-base-using-python/
def dec_to_base(num,base):  #Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  #Using uppercase letters
        num //= base
    base_num = base_num[::-1]  #To reverse the string
    return base_num

# Writes a value to a file address. Supports multi-byte addresses.
def writeToAddress(file, address, val, numBytes=1):
	if val.bit_length() > numBytes*8:
		print("Given value is greater than "+str(numBytes)+" bytes.")
		return False
	address += (numBytes-1)
	for i in range(numBytes):
		file.seek(address)
		currByte = val & 0xFF
		file.write(bytes([currByte]))
		address -= 1
		val = val>>8
	return True