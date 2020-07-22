from my_randomizer import *
import copy
import math
import shutil
from gatelib import *
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename
from gui import *

# the same folder where this program is stored
if getattr(sys, 'frozen', False):
    mainFolder = path.dirname(sys.executable) # EXE (executable) file
else:
	mainFolder = path.dirname(path.realpath(__file__)) # PY (source) file
sys.path.append(mainFolder)
outputFolder = path.join(mainFolder, "output")

def main():
	vp_start_gui()

def randomize():
	global sourceRom
	global currSeed
	global seedString

	# sourceRom = ""
	# while sourceRom == "":
	# 	Tk().withdraw()
	# 	sourceRom = askopenfilename(filetypes=[("ROM files", "*."+rom_file_format)])

	# initialize attributes
	for att in attributes:
		attributes[att].prepare()

	myRules = copy.copy(required_rules)

	varArray = []
	maxValueArray = []
	for ruleset in optionalRulesets:
		varArray.append(ruleset[1])
		maxValueArray.append(1)
	settingsSeed = encodeSeed(varArray, maxValueArray, 36)[0]
	maxVal = int("ZZZZZ", 36)
	genSeed = random.randint(0, maxVal)
	currSeed = (settingsSeed*(maxVal+1)) + genSeed
	numOptionalRulesets = len(optional_rulesets.keys())
	seedString = str(dec_to_base(currSeed, 36)).upper().zfill(5+math.ceil(numOptionalRulesets/5.0))

	for ruleset in optional_rulesets:
		if optionalRulesets[ruleset] == True:
			for rule in optional_rulesets[ruleset]:
				myRules.append(rule)
	enforceRuleset(myRules)

	for att in attributes:
		print(attributes[att].name+": "+str(attributes[att].value))

	generateRom()

def enforceRuleset(ruleset):
	ruleNum = 0
	while ruleNum < len(ruleset):
		if not ruleset[ruleNum].rulePasses():
			nextValueSet = False
			for att in attributes:
				if attributes[att].setToNextValue():
					nextValueSet = True
					break
			if not nextValueSet:
				print("No combination satisfies the given attributes and rules. Quitting.")
				sys.exit()
			ruleNum = 0
		else:
			ruleNum += 1

def generateRom():
	global sourceRom
	global currSeed
	global seedString

	random.seed(currSeed)
	newRom = path.join(outputFolder, path.splitext(path.basename(sourceRom))[0]+"-"+seedString+"."+rom_file_format)
	if not path.isdir(outputFolder):
		mkdir(outputFolder)
	shutil.copyfile(sourceRom, newRom)
	try:
		file = open(newRom, "r+b")
		for att in attributes:
			for address in attributes[att].addresses:
				file.seek(address)
				file.write(bytes([attributes[att].value]))
		file.close()
		print("Succesfully generated ROM with seed "+seedString)
		return True
	except:
		print("Something went wrong. Deleting generated ROM.")
		file.close()
		remove(newRom)
		return False

if __name__ == '__main__':
	main()