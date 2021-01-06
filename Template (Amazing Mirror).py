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

"""
Ability Values:

00 - Nothing
01 - Fire
02 - Ice
03 - Burning
04 - Wheel
05 - Parasol
06 - Cutter
07 - Beam
08 - Stone
09 - Bomb
0A - Throw
0B - Sleep
0C - Cook
0D - Laser
0E - UFO
0F - Spark
10 - Tornado
11 - Hammer
12 - Sword
13 - Cupid
14 - Fighter
15 - Magic
16 - Smash
17 - Mini
18 - Crash
19 - Missile
1A - Master

The remaining values are either some sort of bug/crash, mix (like when you inhale two abilities at one), or duplicate.
"""

########################
# EDIT BELOW THIS LINE #
########################

Program_Name = "Amazing Mirror Randomizer"
Rom_Name = "Kirby & The Amazing Mirror (USA)"
Rom_File_Format = "gba"
About_Page_Text = "This is a sample randomizer for Kirby & The Amazing Mirror that changes the abilities given by a few enemies (specifically, the ones in the first area of the game)."
Timeout = 10
Slow_Mode = False

Attributes = [
	Attribute(
		name="Waddle Dee",
		addresses=[0x35164E, 0x351B76],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
	Attribute(
		name="Droppy",
		addresses=[0x351AFE, 0x3527D6],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
	Attribute(
		name="Leap",
		addresses=[0x3517B6],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
	Attribute(
		name="Big Waddle Dee",
		addresses=[0x3517E6],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
	Attribute(
		name="Flamer",
		addresses=[0x351816],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
	Attribute(
		name="Sword Knight",
		addresses=[0x3518BE],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
	Attribute(
		name="Cupie",
		addresses=[0x35176E],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None, # unused since min_value and max_value are used
		min_value=0,
		max_value=26,
		min_max_interval=1,
	),
]

Required_Rules = [
]

Optional_Rulesets = [
	Ruleset(
		name="All Unique",
		description="All enemies give different abilities.",
		rules=[
			Rule(
				description="All Unique",
				left_side=[value("Waddle Dee"), value("Droppy"), value("Leap"), value("Big Waddle Dee"), value("Flamer"), value("Sword Knight"), value("Cupie")],
				rule_type="!=",
				right_side=None,
			),
		],
		must_be_enabled=None,
		must_be_disabled=["All Master", "Smashing!"],
	),
	Ruleset(
		name="All Master",
		description="All enemies give the Master ability (ability #26).",
		rules=[
			Rule(
				description="Waddle Dee gives Master",
				left_side=value("Waddle Dee"),
				rule_type="==",
				right_side=26,
			),
			Rule(
				description="All enemies give the same ability (by extension, they all give Master)",
				left_side=[value("Waddle Dee"), value("Droppy"), value("Leap"), value("Big Waddle Dee"), value("Flamer"), value("Sword Knight"), value("Cupie")],
				rule_type="==",
				right_side=None,
			),
		],
		must_be_enabled=None,
		must_be_disabled=["All Unique", "At Least 1 UFO", "Smashing!"],
	),
	Ruleset(
		name="All Enemies Give An Ability",
		description="All enemies are guaranteed to give an ability.",
		rules=[
			Rule(
				description="All Enemies Give An Ability",
				left_side=[value("Waddle Dee"), value("Droppy"), value("Leap"), value("Big Waddle Dee"), value("Flamer"), value("Sword Knight"), value("Cupie")],
				rule_type="count",
				right_side=("==", 0, "==", 0),
			),
		],
		must_be_enabled=None,
		must_be_disabled=None,
	),
	Ruleset(
		name="At Least 1 UFO",
		description="At least one enemy gives the UFO ability (ability #14).",
		rules=[
			Rule(
				description="At Least 1 UFO",
				left_side=[value("Waddle Dee"), value("Droppy"), value("Leap"), value("Big Waddle Dee"), value("Flamer"), value("Sword Knight"), value("Cupie")],
				rule_type="count",
				right_side=("==", 0x0E, ">=", 1),
			),
		],
		must_be_enabled=None,
		must_be_disabled=["All Master", "Smashing!"],
	),
	Ruleset(
		name="All Different From Original",
		description="All enemies are guaranteed to give different abilities from what they usually give.",
		rules=[
			Rule(
				description="Waddle Dee is different",
				left_side=value("Waddle Dee"),
				rule_type="!=",
				right_side=0,
			),
			Rule(
				description="Droppy is different",
				left_side=value("Droppy"),
				rule_type="!=",
				right_side=0,
			),
			Rule(
				description="Leap is different",
				left_side=value("Leap"),
				rule_type="!=",
				right_side=0,
			),
			Rule(
				description="Big Waddle Dee is different",
				left_side=value("Big Waddle Dee"),
				rule_type="!=",
				right_side=0,
			),
			Rule(
				description="Flamer is different",
				left_side=value("Flamer"),
				rule_type="!=",
				right_side=3,
			),
			Rule(
				description="Sword Knight is different",
				left_side=value("Sword Knight"),
				rule_type="!=",
				right_side=0x12,
			),
			Rule(
				description="Cupie is different",
				left_side=value("Cupie"),
				rule_type="!=",
				right_side=0x13,
			),
		],
		must_be_enabled=None,
		must_be_disabled=None,
	),
	Ruleset(
		name="Smashing!",
		description="All enemies give either Smash, Fighting, Stone, Cutter, or Hammer.",
		rules=[
			Rule(
				description="Waddle Dee is smashing",
				left_side=value("Waddle Dee"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
			Rule(
				description="Droppy is smashing",
				left_side=value("Droppy"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
			Rule(
				description="Leap is smashing",
				left_side=value("Leap"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
			Rule(
				description="Big Waddle Dee is smashing",
				left_side=value("Big Waddle Dee"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
			Rule(
				description="Flamer is smashing",
				left_side=value("Flamer"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
			Rule(
				description="Sword Knight is smashing",
				left_side=value("Sword Knight"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
			Rule(
				description="Cupie is smashing",
				left_side=value("Cupie"),
				rule_type="==",
				right_side=[0x16, 0x14, 0x8, 0x6, 0x11],
			),
		],
		must_be_enabled=None,
		must_be_disabled=["All Master", "At Least 1 UFO", "All Unique"],
	),
	Ruleset(
		name="XOR Statement (move mouse over this)",
		description="Either Waddle Dee gives Cutter (ability #6), or Droppy gives Throw (ability #10), but not both/neither.",
		rules=[
			Rule(
				description="XOR Statement",
				left_side=[(value("Waddle Dee"), "==", 6), (value("Droppy"), "==", 10)],
				rule_type="count",
				right_side=("==", True, "==", 1),
			),
		],
		must_be_enabled=None,
		must_be_disabled=["All Master"]
	),
]