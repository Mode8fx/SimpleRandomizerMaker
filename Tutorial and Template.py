# This is a randomizer file for the Simple Randomizer Maker.
# This file must be named my_randomizer.py in order to work.

from classes import *

def value(name):
	for att in attributes:
		if att.name == name:
			return att
	print("This attribute does not exist: "+name)
	return None

########################
# EDIT BELOW THIS LINE #
########################

# The name of the randomizer.
program_name = "My Randomizer"
# The name of the rom that's compatible with the randomizer.
# The rom doesn't have to have this exact name, it's just to guide the user.
rom_name = "My Game (USA, Europe) ROM"
# The file format of the ROM ("nes", "gba", etc).
# If you want to allow any file type, leave it as ""
rom_file_format = ""
# Any text you want to put on the "About..." page on the menu bar.
# If you don't want an About page, leave it as ""
about_page_text = ""
# The number of seconds you want to wait per seed before the randomizer times
# out. If you don't want a timeout, leave it as 0.
# It is recommended that you at least set a timeout during testing so you can
# know how long it takes to create a seed.
timeout = 10

"""
A list of Attributes.
An Attribute is anything you want to change the value for, such as item price,
enemy health, base stats, and so on. An Attribute has the following variables:

name: The name of the Attribute.
addresses: The memory address(es) of the Attribute. These addresses must
	be in an array (EXAMPLE: addresses=[0x01234, 0x56789, 0xABCDE]).
number_of_bytes: (optional) The number of bytes taken up by each of these
	addresses. If you don't know what this means, leave it as None
	(the program will attempt to guess).
possible_values: (semi-optional) An array of possible values for this
	Attribute. The addresses will be set to one of these values
	(EXAMPLE: possible_values=[1, 4, 21, 83, 106]). An Attribute must use
	either possible_value or both min_value and max_value (see below).
min_value: (semi-optional) The minimum possible value.
max_value: (semi-optional) The maximum possible value
	(EXAMPLE: setting min_value to 5 and max_value to 10
	will make the possible values [5,6,7,8,9,10]).

If you choose not to use one of the optional variables, set its value to None

A more detailed example can be found below. If you're using this file as a
template, MAKE SURE YOU DELETE THESE ATTRIBUTES!
"""
attributes = [
	Attribute(
		name="My Attribute 1",
		addresses=0x0123,
		number_of_bytes=1,
		possible_values=None,
		min_value=0,
		max_value=100,
	),
	Attribute(
		name="My Attribute 2",
		addresses=[0x456, 0xABC],
		number_of_bytes=1,
		possible_values=[1, 4, 21, 56, 83, 106, 119],
		min_value=None,
		max_value=None,
	),
	Attribute(
		name="My Attribute 3",
		addresses=[0x147, 0x258, 0x369],
		number_of_bytes=2,
		possible_values=[0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300],
		min_value=None,
		max_value=None,
	),
]

"""
A list of Rules.
A Rule is a requirement that the randomized values must follow. This is useful
if you want certain Attributes to depend on others. For example, if you want
to randomize the prices of two healing items (we'll call them Potion and Super
Potion), you can guarantee that the Super Potion will always cost at least
twice as much as a regular Potion. You can also take an array of Attributes and
guarantee that they will all have the same or different values. You can have as
many or as few Rules as you'd like. A Rule has the following variables:

description: (optional) A description of the Rule.
left_side: The left side of the comparison (see examples below).
rule_type: The type of comparison. Possible comparisons are
	"=" (or "=="), "!=", ">", ">=", "<", and "<="
	There is also the "count" comparison, which lets you count how many
	attributes fulfill a certain requirement (see EXAMPLE 3 below).
right_side: The right side of the comparison (unused for some rule types).
	EXAMPLE 1: If you want to set a requirement that a Super Potion must cost
	at least as much as (two Potions + 100), then you would set the following:
		left_side=value("Super Poiton"),
		rule_type=">=",
		right_side=value("Potion")*2+100,
	EXAMPLE 2: If you want to guarantee that a Potion, Elixir, and Revive all
	cost the same amount, then you would set the following:
		left_side=[value("Potion"), value("Elixir"), value("Revive")],
		rule_type="=",
		right_side=None,
	EXAMPLE 3: If you have four stats and you want to guarantee that at most
	two of them are greater than 100 each, then you would set the following:
		left_side=[value("Attack"), value("Defense"), value("Speed"), value("Magic")],
		rule_type = "count",
		right_side = ("<=", 2, ">", 100)

If you choose not to use one of the optional variables, set its value to None

A more detailed example can be found below. If you're using this file as a
template, MAKE SURE YOU DELETE THESE RULES!
"""
required_rules = [
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
An array of optional Rulesets.
A Ruleset is an array of Rules. It is optional and may be enabled or disabled
by the user. This is useful if you want to add optional user settings without
having to create multiple randomizers. A Ruleset has the following variables:

name: The name of the Ruleset.
description: (optional) A description of the ruleset.
rules: An array of Rules that are applied if the Ruleset is enabled.
must_be_enabled: (optional) An array of Ruleset names. This Ruleset can only
	be enabled if all of the optional Rulesets in this array are also enabled.
must_be_disabled: (optional) An array of Ruleset names. This Ruleset can only
	be enabled if all of the optional Rulesets in this array are disabled.

If you choose not to use one of the optional variables, set its value to None

A more detailed example can be found below. If you're using this file as a
template, MAKE SURE YOU DELETE THESE RULESETS!
"""
optional_rulesets = [
	Ruleset(
		name="My Ruleset 1",
		description="Description of My Ruleset 1",
		rules=[
			Rule(
				description="My Attribute 1 and My Attribute 2 are not equal",
				left_side=[value("My Attribute 1"), value("My Attribute 2")],
				rule_type="!=",
				right_side=None,
			),
			Rule(
				description="My Attribute 1 has complex requirements",
				left_side=value("My Attribute 1"),
				rule_type="<",
				right_side=(value("My Attribute 2")+5) - (value("My Attribute 3")/4),
			),
		],
		must_be_enabled=None,
		must_be_disabled=None,
	),
	Ruleset(
		name="My Ruleset 2",
		description="Description of My Ruleset 2",
		rules=[
			Rule(
				description="The first Attribute is an even number, the other two are odd",
				left_side=[(value("My Attribute 1")%2 == 0), (value("My Attribute 2")%2 == 1), (value("My Attribute 3")%2 == 1)],
				rule_type="==",
				right_side=None,
			),
			Rule(
				description="At most, only two attributes can be less than 70",
				left_side=[value("My Attribute 1"), value("My Attribute 2"), value("My Attribute 3")],
				rule_type="count",
				right_side=("<=", 2, "<", 70),
			),
		],
	),
	Ruleset(
		name="Special Ruleset",
		description="This can only be enabled if My Ruleset 1 is enabled and My Ruleset 2 is disabled.",
		must_be_enabled=["My Ruleset 1"],
		must_be_disabled=["My Ruleset 2"],
	),
]