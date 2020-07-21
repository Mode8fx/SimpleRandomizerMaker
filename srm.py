from my_randomizer import *

# the same folder where this program is stored
if getattr(sys, 'frozen', False):
    mainFolder = path.dirname(sys.executable) # EXE (executable) file
else:
	mainFolder = path.dirname(path.realpath(__file__)) # PY (source) file
sys.path.append(mainFolder)
outputFolder = path.join(mainFolder, "output")

def main():
	# initialize attributes
	for att in my_attributes:
		my_attributes[att].prepare()

	ruleNum = 0
	while ruleNum < len(my_rules):
		if not my_rules[ruleNum].rulePasses():
			nextValueSet = False
			for att in my_attributes:
				if my_attributes[att].setToNextValue():
					nextValueSet = True
					break
			if not nextValueSet:
				print("No combination satisfies the given attributes and rules. Quitting.")
				sys.exit()
			ruleNum = 0
		else:
			ruleNum += 1

	print("Complete.\n")
	for att in my_attributes:
		print(my_attributes[att].name+": "+str(my_attributes[att].value))

if __name__ == '__main__':
	main()