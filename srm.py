import sys
from os import path, remove, mkdir
import shutil
from time import time
from gatelib import *

# the same folder where this program is stored
if getattr(sys, 'frozen', False):
	mainFolder = path.dirname(sys.executable) # EXE (executable) file
else:
	mainFolder = path.dirname(path.realpath(__file__)) # PY (source) file
sys.path.append(mainFolder)
outputFolder = path.join(mainFolder, "output")

# GUI imports
try:
	import Tkinter as tk
	from Tkinter.filedialog import askopenfilename
	from Tkinter import font as tkFont
	from Tkinter.messagebox import showinfo, showerror
except ImportError:
	import tkinter as tk
	from tkinter.filedialog import askopenfilename
	from tkinter import font as tkFont
	from tkinter.messagebox import showinfo, showerror
try:
	import ttk
	py3 = False
except ImportError:
	import tkinter.ttk as ttk
	py3 = True

import classes
try:
	from randomizer import *
except:
	tk.Tk().withdraw()
	showerror("Randomizer Not Found", "Valid randomizer file not found. Make sure it is named \"randomizer.py\" and does not contain any errors.")
	sys.exit()

stringLen = 5+ceil(len(Optional_Rulesets)/5.0)

timedOut = False
numAllCombinations = 1
currNumCombinations = 0
currRomIndex = 0

def main():
	global Rom_Name, Rom_File_Format
	if not isinstance(Rom_Name, list):
		Rom_Name = [Rom_Name]
	if not isinstance(Rom_File_Format, list):
		Rom_File_Format = [Rom_File_Format]
	setDefaultRuleNum()
	vp_start_gui()

# The main randomize function.
def randomize():
	global sourceRoms
	global currSeed, seedString
	global endTime
	global numAllCombinations, currNumCombinations
	global Attributes, originalAttributes

	for sr in sourceRoms:
		if not path.isfile(sr.get()):
			return (False, "Invalid ROM input.")

	numOfSeeds = int(numSeeds.get())
	numSeedsGenerated = 0
	for seedNum in range(numOfSeeds):
		originalAttributes = copy.copy(Attributes)
		if useSeed.get() == "1":
			seedString = seedInput.get()
			try:
				assert len(seedString) == stringLen
				assert verifySeed(seedString[:-5], [1]*len(optionalRulesetsList), 36)
			except:
				print("Invalid seed.")
				return (False, "Invalid seed.")
			decodedSeedVals = decodeSeed(seedString[:-5], [1]*len(optionalRulesetsList), 36)
			for i in range(len(optionalRulesetsList)):
				optionalRulesetsList[i] = (optionalRulesetsList[i][0], decodedSeedVals[i])
			currSeed = int(seedString, 36)
		else:
			varArray = []
			maxValueArray = []
			for ruleset in optionalRulesetsList:
				varArray.append(ruleset[1])
				maxValueArray.append(1)
			settingsSeed = encodeSeed(varArray, maxValueArray, 36)[0]
			maxVal = int("ZZZZZ", 36)
			genSeed = random.randint(0, maxVal)
			currSeed = (settingsSeed*(maxVal+1)) + genSeed
			seedString = str(dec_to_base(currSeed, 36)).upper().zfill(stringLen)
		myRules = copy.copy(Required_Rules)
		for ruleset in optionalRulesetsList:
			if ruleset[1] == 1:
				for rule in getFromListByName(Optional_Rulesets, ruleset[0]).rules:
					myRules.append(rule)
		startTime = time()
		endTime = startTime + Timeout
		random.seed(currSeed)
		random.shuffle(Attributes)
		simplifiedRules = []
		for rule in myRules:
			rule.simplifyRule(simplifiedRules)
		myRules = simplifiedRules
		myRules.sort(key=getNumCombinations)
		setNumAllCombinations()
		try:
			result = optimizeAttributes(myRules)
		except:
			errorMessage = "At least one of your rules is bad (has no possible solution)."
			print(errorMessage)
			resetAttributesAndSeed()
			return (False, errorMessage)
		if not result:
			errorMessage = "The program timed out (seed generation took longer than "+str(Timeout)+" seconds)."
			# \n\nEstimated time for current combination of rules: unknown."
			print(errorMessage)
			resetAttributesAndSeed()
			return (False, errorMessage)
		# initialize Attributes
		shuffleAllAttributes()
		for rule in myRules:
			rule.relatedAttributes.sort(key=getShuffledAttributeNum)
		print("Generating values...")
		if not (shotgunApproach(myRules)
			or ((not Slow_Mode) and enforceRulesetBacktracking(myRules))
			or (Slow_Mode and enforceRulesetBruteForce(myRules))):
			errorMessage = ""
			if timedOut:
				errorMessage = "The program timed out (seed generation took longer than "+str(Timeout)+" seconds)."
				# The next line only works for brute force, not backtracking
				# \n\nEstimated time for current combination of rules given your computer's speed: up to "+str(round(numAllCombinations*Timeout/currNumCombinations, 1))+" seconds."
			elif useSeed.get() == "1":
				errorMessage = "Invalid seed."
			else:
				errorMessage = "No combination of values satisfies the given combination of rules. Maybe it's just a bad seed?"
			print(errorMessage)
			resetAttributesAndSeed()
			return (False, errorMessage)

		generatedRom = generateRom()
		resetAttributesAndSeed(True)
		if generateLog.get() == "1":
			generateTextLog()
		for att in Attributes:
			att.resetToDefault()
		if generatedRom[0]:
			numSeedsGenerated += 1
		else:
			return generatedRom
	resetAttributesAndSeed()
	return (True, "Successfully generated "+str(numSeedsGenerated)+" seed"+("s." if numSeedsGenerated != 1 else "."))

# Optimize attributes by checking each rule and attempting to remove any values that are guaranteed to fail.
# For example, if the rule "value("A")>=5" is enabled, this will remove any value of "A"<5.
def optimizeAttributes(ruleset):
	global endTime, timedOut

	setNumAllCombinations()
	for rule in ruleset:
		numRuleCombinations = getNumCombinations(rule)
		# only optimize an attribute if it would take a negligible amount of time
		if numRuleCombinations < 150000: # 150,000 combinations is what my 3.5 year old laptop checks in about half a second
			newPossibleValues = []
			for i in range(len(rule.relatedAttributes)):
				rule.relatedAttributes[i].resetToFirstValue()
				newPossibleValues.append([False] * len(rule.relatedAttributes[i].possible_values))
			nextValueSet = True
			while nextValueSet:
				if Timeout > 0 and time() > endTime:
					timedOut = True
					return False
				if rule.rulePasses(): # you could also check if all current values are True, then skip the rule check (but I think this would be less efficient)
					for i in range(len(rule.relatedAttributes)):
						newPossibleValues[i][rule.relatedAttributes[i].index] = True
				nextValueSet = False
				for i in range(len(rule.relatedAttributes)):
					if rule.relatedAttributes[i].setToNextValue():
						nextValueSet = True
						break
			for i in range(len(rule.relatedAttributes)):
				newVals = []
				for j in range(len(rule.relatedAttributes[i].possible_values)):
					if newPossibleValues[i][j] == True:
						newVals.append(rule.relatedAttributes[i].possible_values[j])
				rule.relatedAttributes[i].possible_values = newVals
				rule.relatedAttributes[i].resetToFirstValue()
	numAllCombinationsNew = 1
	for att in Attributes:
		numAllCombinationsNew *= len(att.possible_values)
	print(str(round((1-(numAllCombinationsNew/numAllCombinations))*100, 3))+"% reduction in seed generation time.")
	return True

# Attempt 50 completely random combinations before attempting a normal approach.
# This is useful for overcoming unlucky RNG without negatively affecting anything else.
def shotgunApproach(ruleset):
	ruleNum = 0
	numAttempts = 0

	while ruleNum < len(ruleset):
		if not ruleset[ruleNum].rulePasses():
			shuffleAllAttributes()
			numAttempts += 1
			if numAttempts >= 50:
				return False
			ruleNum = 0
		else:
			ruleNum += 1
	return True

# Backtracking constraint satisfaction across related Attributes only.
def enforceRulesetBacktracking(ruleset):
	global endTime, timedOut
	global currNumCombinations

	ruleNum = 0
	currNumCombinations = 0

	while ruleNum < len(ruleset):
		if not ruleset[ruleNum].rulePasses():
			if Timeout > 0 and time() > endTime:
				timedOut = True
				return False
			onePassed = False
			for att in ruleset[ruleNum].relatedAttributes:
				nestedRuleNum = 0
				nestedPass = True
				att.setToNextValue()
				while nestedRuleNum < ruleNum:
					if not ruleset[nestedRuleNum].rulePasses():
						nestedPass = False
						break
					nestedRuleNum += 1
				if not nestedPass:
					att.setToPreviousValue()
				else:
					onePassed = True
					break
			if not onePassed:
				nextValueSet = False
				for att in ruleset[ruleNum].relatedAttributes:
					if att.setToNextValue():
						nextValueSet = True
						break
				if not nextValueSet:
					return False
			currNumCombinations += 1
		else:
			ruleNum += 1
	return True

# Brute force constraint satisfaction across all Attributes.
# May work marginally better than backtracking in rare situations (at best),
# but is significantly slower to the point of sometimes being impractical.
def enforceRulesetBruteForce(ruleset):
	global endTime
	global timedOut
	global currNumCombinations

	ruleNum = 0
	currNumCombinations = 0

	while ruleNum < len(ruleset):
		if not ruleset[ruleNum].rulePasses():
			if Timeout > 0 and time() > endTime:
				timedOut = True
				return False
			nextValueSet = False
			for att in Attributes:
				if att.setToNextValue():
					nextValueSet = True
					break
			if not nextValueSet:
				return False
			ruleNum = 0
			currNumCombinations += 1
		else:
			ruleNum += 1
	return True

# Generate a ROM using the determined Attribute values.
def generateRom():
	global sourceRoms
	global seedString

	allNewRoms = []
	success = True
	for sr in sourceRoms:
		romName, romExt = path.splitext(path.basename(sr.get()))
		newRom = path.join(outputFolder, romName+"-"+seedString+romExt)
		allNewRoms.append(newRom)
		if not path.isdir(outputFolder):
			mkdir(outputFolder)
		shutil.copyfile(sr.get(), newRom)
		try:
			file = open(newRom, "r+b")
			for att in Attributes:
				for address in att.addresses:
					writeToAddress(file, address, att.value, att.number_of_bytes)
			file.close()
			print("Succesfully generated ROM with seed "+seedString)
			# return (True, "")
		except:
			file.close()
			success = False
			break
	if not success:
		print("Something went wrong. Deleting generated ROMs.")
		for newRom in allNewRoms:
			remove(newRom)
		return (False, "At least one ROM failed to generate.")
	return (True, "")

# Generate a text log containing the Attribute values.
def generateTextLog():
	global sourceRoms
	global seedString

	newLog = path.join(outputFolder, path.splitext(path.basename(sourceRoms[0].get()))[0]+"-"+seedString+".txt")
	file = open(newLog, "w")
	file.writelines(Program_Name+"\nSeed: "+seedString+"\n\nValues:\n")
	for att in Attributes:
		file.writelines(att.name+": "+str(att.value)+"\n")
	file.close()

def shuffleAllAttributes():
	for att in Attributes:
		att.prepare()

def resetAttributesAndSeed(printAttributes=False):
	global Attributes
	global originalAttributes

	Attributes.sort(key=getAttributeNum)
	if printAttributes:
		for att in Attributes:
			print(att.name+": "+str(att.value))
	Attributes = copy.copy(originalAttributes)
	random.seed(time())
	resetRuleCounter()

def getNumCombinations(rule):
	num = 1
	for att in rule.relatedAttributes:
		num *= len(att.possible_values)
	return num

def setNumAllCombinations():
	global numAllCombinations

	numAllCombinations = 1
	for att in Attributes:
		numAllCombinations *= len(att.possible_values)
	return numAllCombinations

def getFromListByName(arr, name):
	for a in arr:
		if a.name == name:
			return a

def getAttributeNum(att):
	return att.attributeNum

def getShuffledAttributeNum(att):
	for i in range(len(Attributes)):
		if att is Attributes[i]:
			return i

#######
# GUI #
#######

#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module initially created by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#	platform: Windows NT

def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root
	root = tk.Tk()
	# 1.7 seems to be default scaling
	# size = root.winfo_screenheight()
	# sizeRatio = 1080/1440
	# root.tk.call('tk', 'scaling', 2.0*sizeRatio)
	set_Tk_var()
	top = TopLevel(root)
	init(root, top)
	root.mainloop()

w = None
def create_TopLevel(rt, *args, **kwargs):
	'''Starting point when module is imported by another module.
	   Correct form of call: 'create_TopLevel(root, *args, **kwargs)' .'''
	global w, w_win, root
	#rt = root
	root = rt
	w = tk.Toplevel (root)
	set_Tk_var()
	top = TopLevel (w)
	init(w, top, *args, **kwargs)
	return (w, top)

def destroy_TopLevel():
	global w
	w.destroy()
	w = None

class TopLevel:
	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use('winnative')
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])
		self.font = tkFont.Font(family='TkDefaultFont')

		top.geometry(str(750)+"x"+str(450))
		top.minsize(750, 450)
		# top.maxsize(2000, 600)
		top.resizable(1, 1)
		top.title(Program_Name)
		top.configure(background="#d9d9d9")
		top.configure(highlightbackground="#d9d9d9")
		top.configure(highlightcolor="black")

		## Menu Bar
		menubar = tk.Menu(top, bg=_bgcolor, fg=_fgcolor, tearoff=0)
		fileMenu = tk.Menu(menubar, tearoff=0)
		fileMenu.add_command(label="Load ROM...", command=self.setSourceRom)
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=root.quit)
		menubar.add_cascade(label="File", menu=fileMenu)
		top.config(menu=menubar)
		helpMenu = tk.Menu(menubar, tearoff=0)
		helpMenu.add_command(label="View Help...", command=self.showHelpPopup)
		helpMenu.add_separator()
		if About_Page_Text is not None and About_Page_Text != "":
			helpMenu.add_command(label="About...", command=self.showAboutPopup)
		helpMenu.add_command(label="Simple Randomizer Maker", command=self.showSRMPopup)
		menubar.add_cascade(label="Help", menu=helpMenu)
		top.config(menu=menubar)

		self.style.map('TCheckbutton',background=
			[('selected', _bgcolor), ('active', _ana2color)])
		self.style.map('TRadiobutton',background=
			[('selected', _bgcolor), ('active', _ana2color)])

		vMult = 700.0/600

		# Rom Input Label
		self.Label_RomInput = ttk.Label(top)
		self.Label_RomInput.configure(background="#d9d9d9")
		self.Label_RomInput.configure(foreground="#000000")
		self.Label_RomInput.configure(font="TkDefaultFont")
		self.Label_RomInput.configure(relief="flat")
		self.Label_RomInput.configure(anchor='w')
		self.Label_RomInput.configure(justify='left')

		# Rom Input Entry
		self.Entry_RomInput = ttk.Entry(top)
		self.Entry_RomInput.configure(state='readonly')
		self.Entry_RomInput.configure(background="#000000")
		self.Entry_RomInput.configure(cursor="ibeam")

		# Rom Input Label and Entry
		self.setRomInput(vMult)

		# Rom Input Button
		self.Button_RomInput = ttk.Button(top)
		self.Button_RomInput.place(relx=.845, rely=.0365*vMult, relheight=.057*vMult, relwidth=.12)
		self.Button_RomInput.configure(command=self.setSourceRom)
		self.Button_RomInput.configure(takefocus="")
		self.Button_RomInput.configure(text='Load ROM')

		# Use Settings Radio Button
		self.RadioButton_UseSettings = ttk.Radiobutton(top)
		self.RadioButton_UseSettings.place(relx=.035, rely=.11*vMult, relheight=.05*vMult, relwidth=self.getTextLength('Use Settings'))
		self.RadioButton_UseSettings.configure(variable=useSeed)
		self.RadioButton_UseSettings.configure(value="0")
		self.RadioButton_UseSettings.configure(text='Use Settings')
		self.RadioButton_UseSettings.configure(compound='none')
		self.tooltip_font = "TkDefaultFont"
		self.RadioButton_UseSettings_tooltip = ToolTip(self.RadioButton_UseSettings, self.tooltip_font, 'Use the settings defined below to create a random seed.')

		# Use Seed Radio Button
		self.RadioButton_UseSeed = ttk.Radiobutton(top)
		self.RadioButton_UseSeed.place(relx=.035-.01+.81-self.getTextLength("W"*(stringLen+1))-self.getTextLength('Use Seed'), rely=.11*vMult, relheight=.057*vMult, relwidth=self.getTextLength('Use Seed'))
		self.RadioButton_UseSeed.configure(variable=useSeed)
		self.RadioButton_UseSeed.configure(text='''Use Seed''')
		self.tooltip_font = "TkDefaultFont"
		self.RadioButton_UseSeed_tooltip = ToolTip(self.RadioButton_UseSeed, self.tooltip_font, 'Recreate a specific set of changes according to a seed.')

		# Seed Input Entry
		self.Entry_SeedInput = ttk.Entry(top)
		# old relx=.37+self.getTextLength('Use Seed')
		self.Entry_SeedInput.place(relx=.035-.01+.81-self.getTextLength("W"*(stringLen+1)), rely=.11*vMult, relheight=.05*vMult, relwidth=self.getTextLength("W"*(stringLen+1)))
		self.Entry_SeedInput.configure(state='normal')
		self.Entry_SeedInput.configure(textvariable=seedInput)
		self.Entry_SeedInput.configure(takefocus="")
		self.Entry_SeedInput.configure(cursor="ibeam")
		self.Entry_SeedInput.bind('<Key>',self.keepUpperCharsSeed)
		self.Entry_SeedInput.bind('<KeyRelease>',self.keepUpperCharsSeed)

		# Frame
		self.TFrame1 = ttk.Frame(top)
		self.TFrame1.place(relx=.035, rely=.18*vMult, relheight=.55*vMult, relwidth=.93)
		self.TFrame1.configure(relief='groove')
		self.TFrame1.configure(borderwidth="2")
		self.TFrame1.configure(relief="groove")

		# Ruleset Check Buttons
		self.CheckButtons = []
		self.CheckButtons_tooltips = []
		numOptRulesets = len(Optional_Rulesets)
		if numOptRulesets == 0:
			yShiftArray = [0]
		elif numOptRulesets == 1:
			yShiftArray = [-.045, .045]
		elif numOptRulesets == 2:
			yShiftArray = [-.09, 0, .09]
		elif numOptRulesets == 3:
			yShiftArray = [-.135, -.045, .045, .135]
		else:
			yShiftArray = [-.18, -.09, 0, .09, .18]
		if numOptRulesets < 5:
			xShiftArray = [0]
		elif numOptRulesets < 10:
			xShiftArray = [-.15, .15]
		else:
			xShiftArray = [-.30, 0, .30]
		optRulesetNum = 0
		global optRulesetValues
		for ruleset in Optional_Rulesets:
			if optRulesetNum >= 14:
				print("Warning: You can only have up to 14 optional rulesets. Ignoring the rest.")
				break
			self.CheckButtons.append(ttk.Checkbutton(top)) # self.TFrame1 to put in frame
			# self.CheckButtons[optRulesetNum].place(relx=.07+.30*(optRulesetNum//5), rely=(.22+.09*(optRulesetNum%5))*vMult, relheight=.05*vMult, relwidth=self.getTextLength(ruleset.name))
			self.CheckButtons[optRulesetNum].place(relx=.475-self.getMaxColumnWidth(optRulesetNum)/2+xShiftArray[optRulesetNum//5], rely=(.40+yShiftArray[optRulesetNum%5])*vMult, relheight=.05*vMult, relwidth=self.getTextLength(ruleset.name)+.03)
			self.CheckButtons[optRulesetNum].configure(variable=optRulesetValues[optRulesetNum])
			self.CheckButtons[optRulesetNum].configure(offvalue="0")
			self.CheckButtons[optRulesetNum].configure(onvalue="1")
			self.CheckButtons[optRulesetNum].configure(takefocus="")
			self.CheckButtons[optRulesetNum].configure(text=ruleset.name)
			self.tooltip_font = "TkDefaultFont"
			self.CheckButtons_tooltips.append(ToolTip(self.CheckButtons[optRulesetNum], self.tooltip_font, ruleset.description))
			optRulesetNum += 1

		# Number of Seeds Label
		seedX = .475-self.getMaxColumnWidth(optRulesetNum)/2+xShiftArray[optRulesetNum//5]
		self.Label_NumSeeds = ttk.Label(top)
		self.Label_NumSeeds.place(relx=seedX, rely=(.40+yShiftArray[optRulesetNum%5])*vMult, relheight=.05*vMult, relwidth=.11)
		self.Label_NumSeeds.configure(background="#d9d9d9")
		self.Label_NumSeeds.configure(foreground="#000000")
		self.Label_NumSeeds.configure(font="TkDefaultFont")
		self.Label_NumSeeds.configure(relief="flat")
		self.Label_NumSeeds.configure(anchor='w')
		self.Label_NumSeeds.configure(justify='left')
		self.Label_NumSeeds.configure(text='# of Seeds')
		self.tooltip_font = "TkDefaultFont"
		self.Label_NumSeeds_tooltip = ToolTip(self.Label_NumSeeds, self.tooltip_font, 'How many seeds would you like to generate?')

		# Number of Seeds Dropdown
		self.ComboBox_NumSeeds = ttk.Combobox(top)
		self.ComboBox_NumSeeds.place(relx=seedX, rely=(.45+yShiftArray[optRulesetNum%5])*vMult, relheight=.05*vMult, relwidth=.088)
		self.value_list = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',]
		self.ComboBox_NumSeeds.configure(values=self.value_list)
		self.ComboBox_NumSeeds.configure(state='readonly')
		self.ComboBox_NumSeeds.configure(textvariable=numSeeds)

		# Text Log Check Button
		self.CheckButton_GenerateTextLog = ttk.Checkbutton(top)
		self.CheckButton_GenerateTextLog.place(relx=.25, rely=.895, relheight=.05*vMult, relwidth=.20)
		self.CheckButton_GenerateTextLog.configure(variable=generateLog)
		self.CheckButton_GenerateTextLog.configure(takefocus="")
		self.CheckButton_GenerateTextLog.configure(text='Generate Text Log')
		self.tooltip_font = "TkDefaultFont"
		self.CheckButton_GenerateTextLog_tooltip = ToolTip(self.CheckButton_GenerateTextLog, self.tooltip_font, 'Would you like to generate a text file that details what abilities are tied to each enemy/object in the created seed?')

		# Create Rom Button
		self.Button_CreateRom = ttk.Button(top)
		self.Button_CreateRom.place(relx=.55, rely=.8915, relheight=.057*vMult, relwidth=.144)
		self.Button_CreateRom.configure(takefocus="")
		self.Label_NumSeeds.configure(anchor='w')
		self.Button_CreateRom.configure(text='''Randomize!''')

		# Message (unused)
		# self.Label_Message = ttk.Label(top)
		# self.Label_Message.place(relx=.05, rely=.75, relheight=.05, relwidth=.90)
		# self.Label_Message.configure(background="#d9d9d9")
		# self.Label_Message.configure(foreground="#000000")
		# self.Label_Message.configure(font="TkDefaultFont")
		# self.Label_Message.configure(relief="flat")
		# self.Label_Message.configure(anchor='center')
		# self.Label_Message.configure(justify='left')
		# self.Label_Message.configure(textvariable=message)

		# Other
		self.RadioButton_UseSettings.configure(command=self.prepareSettingsAndSeed)
		self.RadioButton_UseSeed.configure(command=self.prepareSettingsAndSeed)
		self.Button_CreateRom.configure(command=self.attemptRandomize)
		for i in range(min(len(Optional_Rulesets), 13)):
			self.CheckButtons[i].configure(command=self.prepareSettingsFromDependencies)
		self.prepareSettingsFromDependencies()

	def getTextLength(self, text):
		return .03+self.font.measure(text)/1000.0

	def getMaxColumnWidth(self, num):
		lower = 5 * (num//5)
		upper = lower + 5
		sizeArr = []
		for i in range(lower, min(upper, len(Optional_Rulesets))):
			sizeArr.append(self.getTextLength(Optional_Rulesets[i].name)-.03)
		if len(sizeArr) == 0:
			return self.getTextLength("# of Seeds")-.03
		return max(sizeArr)

	def prepareSettingsAndSeed(self, unused=None):
		if useSeed.get()=="1":
			self.Label_NumSeeds.configure(state="disabled")
			self.ComboBox_NumSeeds.configure(state="disabled")
			for button in self.CheckButtons:
				button.configure(state="disabled")
		else:
			self.Label_NumSeeds.configure(state="normal")
			self.ComboBox_NumSeeds.configure(state="readonly")
			for button in self.CheckButtons:
				button.configure(state="normal")
			self.prepareSettingsFromDependencies()

	def prepareSettingsFromDependencies(self):
		for i in range(len(self.CheckButtons)):
			currCheckButton = self.CheckButtons[i]
			currCheckButton.configure(state="normal")
			for j in range(len(self.CheckButtons)):
				currRulesetVal = optRulesetValues[j].get()
				currRulesetName = Optional_Rulesets[j].name
				if ((currRulesetVal == "1") and (currRulesetName in Optional_Rulesets[i].must_be_disabled)
					) or ((currRulesetVal == "0") and (currRulesetName in Optional_Rulesets[i].must_be_enabled)):
					optRulesetValues[i].set("0")
					currCheckButton.configure(state="disabled")
					break

	def setRomInput(self, vMult):
		romTextLength = self.getTextLength(Rom_Name[currRomIndex])
		self.Label_RomInput.place(relx=.035, rely=.04*vMult, relheight=.05*vMult, relwidth=romTextLength)
		self.Label_RomInput.configure(text=Rom_Name[currRomIndex])
		self.Entry_RomInput.place(relx=.035+romTextLength-.01, rely=.04*vMult, relheight=.05*vMult, relwidth=.81-romTextLength)
		self.Entry_RomInput.configure(textvariable=sourceRoms[currRomIndex])

	def setSourceRom(self):
		global sourceRoms
		currRFF = Rom_File_Format[currRomIndex % len(Rom_File_Format)]
		if currRFF is None or currRFF == "":
			sourceRoms[currRomIndex].set(askopenfilename())
		else:
			sourceRoms[currRomIndex].set(askopenfilename(filetypes=[("Files", "*."+currRFF)]))

	def keepUpperCharsSeed(self, unused):
		global seedInput
		seedInput.set(''.join(ch.upper() for ch in seedInput.get() if ch.isalpha() or ch.isdigit()))
		seedInput.set(seedInput.get()[:stringLen])
		useSeed.set("1")
		self.prepareSettingsAndSeed()

	def attemptRandomize(self):
		global optionalRulesetsList
		global optRulesetValues

		optionalRulesetsList = [("", 0)] * len(optRulesetValues)
		for i in range(len(optRulesetValues)):
			optionalRulesetsList[i] = (Optional_Rulesets[i].name, int(optRulesetValues[i].get()))
		results = randomize()
		print("\n")
		# message.set(results[1])
		# self.Label_Message.configure(foreground="#0000FF" if results[0] else "#FF0000")
		if results[0]:
			showinfo("Success!", results[1])
		else:
			showerror("Error", results[1])

	def showHelpPopup(self):
		showinfo("Help",
			"To learn more about an option, move your mouse over it."
			+"\n"+limitedString("You can generate multiple unique ROMs at once by changing the # of seeds.", 55, "- ")
			+"\n"+limitedString("You can also generate a text log that gives information about a created seed.", 55, "- ")
			+"\n"+limitedString("Generated ROMs will be placed in an \"output\" folder, which will be in the same folder as this program.", 55, "- "))

	def showAboutPopup(self):
		showinfo("About", About_Page_Text)

	def showSRMPopup(self):
		showinfo("Simple Randomizer Maker v1.1", "This was made using\nGateGuy's Simple Randomizer Maker.\n\nhttps://github.com/GateGuy/SimpleRandomizerMaker")

# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================

from time import localtime, strftime

class ToolTip(tk.Toplevel):
	"""
	Provides a ToolTip widget for Tkinter.
	To apply a ToolTip to any Tkinter widget, simply pass the widget to the
	ToolTip constructor
	"""
	def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
				 delay=0.5, follow=True):
		"""
		Initialize the ToolTip

		Arguments:
		  wdgt: The widget this ToolTip is assigned to
		  tooltip_font: Font to be used
		  msg:  A static string message assigned to the ToolTip
		  msgFunc: A function that retrieves a string to use as the ToolTip text
		  delay:   The delay in seconds before the ToolTip appears(may be float)
		  follow:  If True, the ToolTip follows motion, otherwise hides
		"""
		self.wdgt = wdgt
		# The parent of the ToolTip is the parent of the ToolTips widget
		self.parent = self.wdgt.master
		# Initalise the Toplevel
		tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
		# Hide initially
		self.withdraw()
		# The ToolTip Toplevel should have no frame or title bar
		self.overrideredirect(True)

		# The msgVar will contain the text displayed by the ToolTip
		self.msgVar = tk.StringVar()
		if msg is None:
			self.msgVar.set('No message provided')
		else:
			self.msgVar.set(msg)
		self.msgFunc = msgFunc
		self.delay = delay
		self.follow = follow
		self.visible = 0
		self.lastMotion = 0
		# The text of the ToolTip is displayed in a Message widget
		tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
				font=tooltip_font,
				aspect=1000).grid()

		# Add bindings to the widget.  This will NOT override
		# bindings that the widget already has
		self.wdgt.bind('<Enter>', self.spawn, '+')
		self.wdgt.bind('<Leave>', self.hide, '+')
		self.wdgt.bind('<Motion>', self.move, '+')

	def spawn(self, event=None):
		"""
		Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
		Usually this is caused by entering the widget

		Arguments:
		  event: The event that called this funciton
		"""
		self.visible = 1
		# The after function takes a time argument in milliseconds
		self.after(int(self.delay * 1000), self.show)

	def show(self):
		"""
		Displays the ToolTip if the time delay has been long enough
		"""
		if self.visible == 1 and time() - self.lastMotion > self.delay:
			self.visible = 2
		if self.visible == 2:
			self.deiconify()

	def move(self, event):
		"""
		Processes motion within the widget.
		Arguments:
		  event: The event that called this function
		"""
		self.lastMotion = time()
		# If the follow flag is not set, motion within the
		# widget will make the ToolTip disappear
		#
		if self.follow is False:
			self.withdraw()
			self.visible = 1

		# Offset the ToolTip 10x10 pixes southwest of the pointer
		self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
		try:
			# Try to call the message function.  Will not change
			# the message if the message function is None or
			# the message function fails
			self.msgVar.set(self.msgFunc())
		except:
			pass
		self.after(int(self.delay * 1000), self.show)

	def hide(self, event=None):
		"""
		Hides the ToolTip.  Usually this is caused by leaving the widget
		Arguments:
		  event: The event that called this function
		"""
		self.visible = 0
		self.withdraw()

	def update(self, msg):
		"""
		Updates the Tooltip with a new message. Added by Rozen
		"""
		self.msgVar.set(msg)

# ===========================================================
#				   End of Class ToolTip
# ===========================================================

def set_Tk_var():
	global sourceRoms
	sourceRoms = [tk.StringVar()] * len(Rom_Name)
	global optRulesetValues
	optRulesetValues = []
	for i in range(len(Optional_Rulesets)):
		optRulesetValues.append(tk.StringVar())
	global numSeeds
	numSeeds = tk.StringVar()
	global useSeed
	useSeed = tk.StringVar()
	global seedInput
	seedInput = tk.StringVar()
	global generateLog
	generateLog = tk.StringVar()
	global message
	message = tk.StringVar()
	message.set('')
	initVars()

def initVars():
	useSeed.set("0")
	numSeeds.set("1")
	generateLog.set("1")
	for val in optRulesetValues:
		val.set("0")
	message.set("Move your mouse over a label to learn more about it.")

def init(top, gui, *args, **kwargs):
	global w, top_level, root
	w = gui
	top_level = top
	root = top

def destroy_window(endProg=False):
	# Function which closes the window.
	global top_level
	top_level.destroy()
	top_level = None
	if endProg:
		sys.exit()

if __name__ == '__main__':
	main()