# This is a randomizer file for the Simple Randomizer Maker.
# This file must be named randomizer.py in order to work.
# For more information on what each variable means, see "Readme (Tutorial).md"

from classes import *

def value(name):
	for att in Attributes:
		if att.name == name:
			return att
	print("This attribute does not exist: "+name)
	return None

########################
# EDIT BELOW THIS LINE #
########################

Program_Name = "My Randomizer"
Rom_Name = "Rom Name"
Rom_File_Format = "gba" # File format (nes, gba, etc.)
About_Page_Text = "This is the text that will show on the About page."
Timeout = 10
Slow_Mode = False

Attributes = [

]

Required_Rules = [

]

Optional_Rulesets = [

]