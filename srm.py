from my_randomizer import *
import copy

# the same folder where this program is stored
if getattr(sys, 'frozen', False):
    mainFolder = path.dirname(sys.executable) # EXE (executable) file
else:
	mainFolder = path.dirname(path.realpath(__file__)) # PY (source) file
sys.path.append(mainFolder)
outputFolder = path.join(mainFolder, "output")

def main():
	# initialize attributes
	for att in attributes:
		attributes[att].prepare()

	myRules = copy.copy(required_rules)
	optionalRulesToFollow = {
		"My Rules 1" : False,
		"My Rules 2" : False,
	}
	for ruleset in optional_rulesets:
		if optionalRulesToFollow[ruleset] == True:
			for rule in optional_rulesets[ruleset]:
				myRules.append(rule)
	enforceRuleset(myRules)

	print("Complete.\n")
	for att in attributes:
		print(attributes[att].name+": "+str(attributes[att].value))

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

if __name__ == '__main__':
	main()