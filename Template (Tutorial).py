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
Rom_Name = "My Game (USA, Europe) ROM"
Rom_File_Format = ""
About_Page_Text = ""
Timeout = 10
Slow_Mode = False

"""
If you're using this file as a template, MAKE SURE YOU DELETE THESE ATTRIBUTES!
"""
Attributes = [
	Attribute(
		name="My Attribute 1",
		addresses=[0x0123],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=100,
		min_max_interval=1,
	),
	Attribute(
		name="My Attribute 2",
		addresses=[0x456, 0xABC],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=[1, 4, 21, 56, 83, 106, 119],
		min_value=None, # unused since possible_values is used
		max_value=None, # unused since possible_values is used
		min_max_interval=None, # unused since possible_values is used
	),
	Attribute(
		name="My Attribute 3",
		addresses=[0x147, 0x258, 0x369],
		number_of_bytes=2,
		is_little_endian=False,
		possible_values=[0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300],
		min_value=None, # unused since possible_values is used
		max_value=None, # unused since possible_values is used
		min_max_interval=None, # unused since possible_values is used
	),
]

"""
If you're using this file as a template, MAKE SURE YOU DELETE THESE RULES!
"""
Required_Rules = [
	Rule(
		description="My Attribute 1 + My Attribute 2 is less than 150",
		left_side=value("My Attribute 1") + value("My Attribute 2"),
		rule_type="<",
		right_side=150,
	),
	Rule(
		description="My Attribute 2 + My Attribute 3 is at least 20",
		left_side=value("My Attribute 2") + value("My Attribute 3"),
		rule_type=">=",
		right_side=20,
	),
]

"""
If you're using this file as a template, MAKE SURE YOU DELETE THESE RULESETS!
"""
Optional_Rulesets = [
	Ruleset(
		name="Basic Rules",
		description="A set of basic rules",
		rules=[
			Rule(
				description="My Attribute 1 and My Attribute 2 are not equal",
				left_side=[value("My Attribute 1"), value("My Attribute 2")],
				rule_type="!=",
				right_side=None,
			),
			Rule(
				description="My Attribute 1 has more requirements",
				left_side=value("My Attribute 1"),
				rule_type="<",
				right_side=(value("My Attribute 2")+5) - (value("My Attribute 3")/4),
			),
		],
		must_be_enabled=None,
		must_be_disabled=None,
	),
	Ruleset(
		name="Advanced Rules",
		description="A set of advanced rules",
		rules=[
			Rule(
				description="The first Attribute is an even number, the other two are odd",
				left_side=[(value("My Attribute 1")%2, "==", 0), (value("My Attribute 2")%2, "==", 1), (value("My Attribute 3")%2, "==", 1)],
				rule_type="==",
				right_side=None,
			),
			Rule(
				description="The number of attributes that can be less than 70 is at most 2",
				left_side=[value("My Attribute 1"), value("My Attribute 2"), value("My Attribute 3")],
				rule_type="count",
				right_side=("<", 70, "<=", 2),
			),
		],
		must_be_enabled=None,
		must_be_disabled=None,
	),
	Ruleset(
		name="Special Ruleset",
		description="This can only be enabled if My Ruleset 1 is enabled and My Ruleset 2 is disabled.",
		rules=[],
		must_be_enabled=["My Ruleset 1"],
		must_be_disabled=["My Ruleset 2"],
	),
]