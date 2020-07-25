# This is a randomizer file for the Simple Randomizer Maker.
# This file must be named my_randomizer.py in order to work.

from classes import *

########################
# EDIT BELOW THIS LINE #
########################

program_name = "Amazing Mirror Randomizer"
rom_name = "Kirby & The Amazing Mirror (USA)"
rom_file_format = "gba"
about_page_text = "PLACEHOLDER TEXT"

attributes = {
	"Sword Knight" : Attribute(
		name="Sword Knight",
		addresses=0x3518BE,
		min_value=0,
		max_value=26,
	),
	"Cupie" : Attribute(
		name="Cupie",
		addresses=0x35176E,
		min_value=0,
		max_value=26,
	),
}

required_rules = [
	# Rule(
	# 	description="Sword Knight and Cupie give the same ability",
	# 	left_side=[attributes["Sword Knight"], attributes["Cupie"]],
	# 	rule_type="==",
	# 	right_side=None
	# ),
	Rule(
		description="Sword Knight is at most one more than Cupie*2",
		left_side=attributes["Sword Knight"],
		rule_type="<=",
		right_side=attributes["Cupie"]*2+1,
	),
	# Rule(
	# 	description="Sword Knight gives ability 5",
	# 	left_side=attributes["Sword Knight"],
	# 	rule_type="==",
	# 	right_side=10,
	# ),
]

optional_rulesets = [
	Ruleset(
		name="Low Values",
		description="Description of My Rules 1",
		rules=[
			Rule(
				description="Sword Knight < 10",
				left_side=attributes["Sword Knight"],
				rule_type="<",
				right_side=10
			),
			Rule(
				description="Cupie >= 3",
				left_side=attributes["Cupie"],
				rule_type=">=",
				right_side=3
			),
		],
		must_be_disabled="High Values",
	),
	Ruleset(
		name="High Values",
		description="Description of My Rules 2",
		rules=[
			Rule(
				description="Sword Knight > 18",
				left_side=attributes["Sword Knight"],
				rule_type=">",
				right_side=18
			),
			Rule(
				description="Cupie > 9",
				left_side=attributes["Cupie"],
				rule_type=">",
				right_side=9
			),
		],
		must_be_disabled="Low Values",
	),
]