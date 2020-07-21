from classes import *

########################
# EDIT BELOW THIS LINE #
########################

my_attributes = {
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

my_rules = [
	# Rule(
	# 	name="Sword Knight and Cupie give the same ability",
	# 	left_side=my_attributes["Sword Knight"],
	# 	rule_type="==",
	# 	right_side=my_attributes["Cupie"],
	# ),
	Rule(
		name="Sword Knight is one more than Cupie",
		left_side=my_attributes["Sword Knight"],
		rule_type="==",
		right_side=my_attributes["Cupie"]*2+1,
	),
	# Rule(
	# 	name="Sword Knight gives ability 5",
	# 	left_side=my_attributes["Sword Knight"],
	# 	rule_type="==",
	# 	right_side=10,
	# ),
]