from classes import *

########################
# EDIT BELOW THIS LINE #
########################

program_name = "Amazing Mirror Randomizer"
rom_name = "Kirby & The Amazing Mirror (USA)"
rom_file_format = "gba"
about_page_text = ""

attributes = {
	"Sword Knight" : Attribute(
		name="Sword Knight",
		description="The ability given by Sword Knight",
		addresses=0x3518BE,
		min_value=0,
		max_value=26,
	),
	"Cupie" : Attribute(
		name="Cupie",
		description="The ability given by Cupie",
		addresses=0x35176E,
		min_value=0,
		max_value=26,
	),
}

required_rules = [
	Rule(
		name="Sword Knight and Cupie give the same ability",
		left_side=[attributes["Sword Knight"], attributes["Cupie"]],
		rule_type="==",
		right_side=None
	),
	# Rule(
	# 	name="Sword Knight is one more than Cupie",
	# 	left_side=attributes["Sword Knight"],
	# 	rule_type="==",
	# 	right_side=attributes["Cupie"]*2+1,
	# ),
	# Rule(
	# 	name="Sword Knight gives ability 5",
	# 	left_side=attributes["Sword Knight"],
	# 	rule_type="==",
	# 	right_side=10,
	# ),
]

optional_rulesets = [
	Ruleset(
		name="My Rules 1",
		description="Description of My Rules 1",
		rules=[
			Rule(
				name="Sword Knight < 10",
				left_side=attributes["Sword Knight"],
				rule_type="<",
				right_side=10
			),
			Rule(
				name="Cupie >= 3",
				left_side=attributes["Cupie"],
				rule_type=">=",
				right_side=3
			),
		],
	),
	Ruleset(
		name="My Rules 2",
		description="Description of My Rules 2",
		rules=[
			Rule(
				name="Sword Knight > 12",
				left_side=attributes["Sword Knight"],
				rule_type=">",
				right_side=12
			),
			Rule(
				name="Cupie > 18",
				left_side=attributes["Cupie"],
				rule_type=">",
				right_side=18
			),
		],
	),
	Ruleset(
		name="My Rules 3",
		description="Description of My Rules 3",
		must_be_enabled=["My Rules 1"],
	),
	Ruleset(
		name="Pretty Log Name for Ruleset",
		description="Description of My Rules 4",
		must_be_disabled=["My Rules 2"],
	),
	Ruleset(
		name="My Rules 5",
		description="Description of My Rules 5",
	),
	Ruleset(
		name="My Rules 6",
		description="Description of My Rules 6",
	),
	Ruleset(
		name="My Rules 7",
		description="Description of My Rules 7",
	),
	Ruleset(
		name="My Rules 8",
		description="Description of My Rules 8",
	),
	Ruleset(
		name="My Rules 9",
		description="Description of My Rules 9",
	),
	Ruleset(
		name="My Rules 10",
		description="Description of My Rules 10",
	),
	Ruleset(
		name="My Rules 11",
		description="Description of My Rules 11",
	),
	Ruleset(
		name="My Rules 12",
		description="Description of My Rules 12",
	),
	Ruleset(
		name="My Rules 13",
		description="Description of My Rules 13",
	),
	Ruleset(
		name="My Rules 14",
		description="Description of My Rules 14",
	),
	Ruleset(
		name="My Rules 15",
		description="Description of My Rules 15",
	),
]