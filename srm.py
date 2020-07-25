import copy
import math
import shutil
from gatelib import *

from my_randomizer import *

try:
	from my_randomizer import *
except:
	print("Randomizer file not found. Make sure it is named \"my_randomizer.py\"")
	import sys
	sys.exit()

"""
TODO:
- It's way too freaking slow, don't brute force all possible values
"""

# the same folder where this program is stored
if getattr(sys, 'frozen', False):
	mainFolder = path.dirname(sys.executable) # EXE (executable) file
else:
	mainFolder = path.dirname(path.realpath(__file__)) # PY (source) file
sys.path.append(mainFolder)
outputFolder = path.join(mainFolder, "output")
stringLen = 5+math.ceil(len(optional_rulesets)/5.0)

def main():
	vp_start_gui()

def randomize():
	global sourceRom
	global currSeed
	global seedString

	if not path.isfile(sourceRom.get()):
		return (False, "Invalid ROM input.")

	numOfSeeds = int(numSeeds.get())
	numSeedsGenerated = 0
	for seedNum in range(numOfSeeds):
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
		myRules = copy.copy(required_rules)
		for ruleset in optionalRulesetsList:
			if ruleset[1] == 1:
				for rule in getFromListByName(optional_rulesets, ruleset[0]).rules:
					myRules.append(rule)
		random.seed(currSeed)
		# initialize attributes
		for att in attributes:
			att.prepare()
		if not enforceRuleset(myRules):
			if useSeed.get() == "1":
				print("Invalid seed")
				return (False, "Invalid seed.")
			else:
				print("No combination of values satisfies the given combination of rules.")
				return (False, "No combination of values satisfies the given combination of rules.")

		for att in attributes:
			print(att.name+": "+str(att.value))

		generatedRom = generateRom()
		if generateLog.get() == "1":
			generateTextLog()
		for att in attributes:
			att.resetToDefault()
		if generatedRom[0]:
			numSeedsGenerated += 1
		else:
			return generatedRom
	return (True, "Successfully generated "+str(numSeedsGenerated)+" seed"+("s." if numSeedsGenerated != 1 else "."))

def getFromListByName(arr, name):
	for a in arr:
		if a.name == name:
			return a

def enforceRuleset(ruleset):
	ruleNum = 0
	while ruleNum < len(ruleset):
		if not ruleset[ruleNum].rulePasses():
			nextValueSet = False
			for att in attributes:
				if att.setToNextValue():
					nextValueSet = True
					break
			if not nextValueSet:
				return False
			ruleNum = 0
		else:
			ruleNum += 1
	return True

def generateRom():
	global sourceRom
	global seedString

	romName, romExt = path.splitext(path.basename(sourceRom.get()))
	newRom = path.join(outputFolder, romName+"-"+seedString+romExt)
	if not path.isdir(outputFolder):
		mkdir(outputFolder)
	shutil.copyfile(sourceRom.get(), newRom)
	try:
		file = open(newRom, "r+b")
		for att in attributes:
			for address in att.addresses:
				writeToAddress(file, address, att.value, att.number_of_bytes)
		file.close()
		print("Succesfully generated ROM with seed "+seedString)
		return (True, "")
	except:
		print("Something went wrong. Deleting generated ROM.")
		file.close()
		remove(newRom)
		return (False, "Failed to generate ROM.")

def generateTextLog():
	global sourceRom
	global seedString

	newLog = path.join(outputFolder, path.splitext(path.basename(sourceRom.get()))[0]+"-"+seedString+".txt")
	file = open(newLog, "w")
	file.writelines(program_name+"\nSeed: "+seedString+"\n\nValues:\n")
	for att in attributes:
		file.writelines(att.name+": "+str(att.value)+"\n")
	file.close()

#######
# GUI #
#######

#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module initially created by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#	platform: Windows NT

import sys

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

def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root, sizeRatio
	root = tk.Tk()
	# 1.7 seems to be default scaling
	size = root.winfo_screenheight()
	sizeRatio = size/1440
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

		top.geometry(str(int(1000*sizeRatio))+"x"+str(int(600*sizeRatio)))
		top.minsize(int(1000*sizeRatio), int(600*sizeRatio))
		# top.maxsize(2000, 600)
		top.resizable(1, 1)
		top.title(program_name)
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
		if about_page_text is not None and about_page_text != "":
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
		romTextLength = self.getTextLength(rom_name)
		self.Label_RomInput.place(relx=.035, rely=.04*vMult, relheight=.05*vMult, relwidth=romTextLength)
		self.Label_RomInput.configure(background="#d9d9d9")
		self.Label_RomInput.configure(foreground="#000000")
		self.Label_RomInput.configure(font="TkDefaultFont")
		self.Label_RomInput.configure(relief="flat")
		self.Label_RomInput.configure(anchor='w')
		self.Label_RomInput.configure(justify='left')
		self.Label_RomInput.configure(text=rom_name)

		# Rom Input Entry
		self.Entry_RomInput = ttk.Entry(top)
		# old relx=.035+self.getTextLength(rom_name+' ROM')-.02
		# old relwidth=.40
		self.Entry_RomInput.place(relx=.035+romTextLength-.01, rely=.04*vMult, relheight=.05*vMult, relwidth=.81-romTextLength)
		self.Entry_RomInput.configure(state='readonly')
		self.Entry_RomInput.configure(textvariable=sourceRom)
		self.Entry_RomInput.configure(background="#000000")
		self.Entry_RomInput.configure(cursor="ibeam")

		# Rom Input Button
		self.Button_RomInput = ttk.Button(top)
		# old relx=.035+self.getTextLength(rom_name+' ROM')-.02+.40+.01
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
		self.RadioButton_UseSeed_tooltip = ToolTip(self.RadioButton_UseSeed, self.tooltip_font, 'Recreate a specific set of changes according to a 10-character seed.')

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
		numOptRulesets = len(optional_rulesets)
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
		for ruleset in optional_rulesets:
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
		for i in range(min(len(optional_rulesets), 13)):
			self.CheckButtons[i].configure(command=self.prepareSettingsFromDependencies)
		self.prepareSettingsFromDependencies()

	def getTextLength(self, text):
		return .03+self.font.measure(text)/1000.0

	def getMaxColumnWidth(self, num):
		lower = 5 * (num//5)
		upper = lower + 5
		sizeArr = []
		for i in range(lower, min(upper, len(optional_rulesets))):
			sizeArr.append(self.getTextLength(optional_rulesets[i].name)-.03)
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
				currRulesetName = optional_rulesets[j].name
				if ((currRulesetVal == "1") and (currRulesetName in optional_rulesets[i].must_be_disabled)
					) or ((currRulesetVal == "0") and (currRulesetName in optional_rulesets[i].must_be_enabled)):
					optRulesetValues[i].set("0")
					currCheckButton.configure(state="disabled")
					break

	def setSourceRom(self):
		global sourceRom
		if rom_file_format is None or rom_file_format == "":
			sourceRom.set(askopenfilename())
		else:
			sourceRom.set(askopenfilename(filetypes=[("ROM files", "*."+rom_file_format)]))

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
			optionalRulesetsList[i] = (optional_rulesets[i].name, int(optRulesetValues[i].get()))
		results = randomize()
		# message.set(results[1])
		# self.Label_Message.configure(foreground="#0000FF" if results[0] else "#FF0000")
		if results[0]:
			showinfo("Success!", results[1])
		else:
			showerror("Error", results[1])

	def showHelpPopup(self):
		showinfo("Help",
			"To learn more about an option, move your mouse over it.\
			\nYou can generate multiple unique ROMs at once by changing the # of seeds.\
			\nYou can also generate a text log that gives information about a created seed.\
			\nGenerated ROMs will be placed in an \"output\" folder, which will be in the same folder as this program.")

	def showAboutPopup(self):
		showinfo("About", about_page_text)

	def showSRMPopup(self):
		showinfo("Simple Randomizer Maker v1.0", "This was made using\nGateGuy's Simple Randomizer Maker.\n\nhttps://github.com/GateGuy/SimpleRandomizerMaker")

# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================

from time import time, localtime, strftime

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
	global sourceRom
	sourceRom = tk.StringVar()
	global optRulesetValues
	optRulesetValues = []
	for i in range(len(optional_rulesets)):
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