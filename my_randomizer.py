import sys
import random
import shutil
import copy
from math import ceil, floor
from os import path, remove, mkdir
from time import sleep

"""
An attribute that is being randomized. The value at the given ROM address(es) will be changed into one of the given values at random
name: the name of the attribute
description: optional; a description of the attribute
addresses: an array of all ROM addresses for this attribute (note: these addresses will all be changed to the same thing)
possible_values: optional; an array of possible values for this attribute
min_value: optional; the minimum value of this attribute
max_value: optional; the maximum value of this attribute
rules: optional; an array of logical rules that must be followed (explained in more detail below)
NOTE: You must use either (possible_values), (min_value and max_value), or both

EXAMPLE USING VALUES (from Kirby & The Amazing Mirror):
sword_knight_ability = Attribute(
	name="Sword Knight",
	description="The ability given by Sword Knight",
	addresses=[0x3518BE], # if you only use one address, you don't have to put it in an array
	possible_values=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
)
ALTERNATE EXAMPLE
sword_knight_ability = Attribute(
	name="Sword Knight",
	description="The ability given by Sword Knight",
	addresses=0x3518BE,
	min_value=0,
	max_value=26
)

You can also use "rules" make an attribute whose values are determine by another attribute.
In this example, a Golden Mushroom will always cost 1.5x to 2.5x as much as a regular Mushroom.
EXAMPLE (item prices for Mario Party 2; the addresses are made up):
mushroom_price = Attribute(
	name="Mushroom", description="Mushroom Price", addresses=[0x153835], min_value=4, max_value=8
)
golden_mushroom_price = Attribute(
	name="Golden Mushroom",
	description="Golden Mushroom Price",
	addresses=[0x154261],
	min_value=5,
	max_value=20,
	rules = [("Is Greater Than or Equal To", mushroom_price*1.5), ("Is Less Than or Equal To", mushroom_price*2.5)]
)
"""

def applyRule(rule_type, att, right_side):
	newPossibleValues = []
	for val in att.possible_values:
		if not isinstance(right_side, list):
			right_side = [right_side]
		if ((rule_type == "Equals" and any(val == right_val for right_val in right_side))
			or (rule_type == "Does Not Equal" and any(val != right_val for right_val in right_side))
			or (rule_type == "Is Greater Than" and any(val > right_val for right_val in right_side))
			or (rule_type == "Is Greater Than or Equal To" and any(val >= right_val for right_val in right_side))
			or (rule_type == "Is Less Than" and any(val < right_val for right_val in right_side))
			or (rule_type == "Is Less Than or Equal To" and any(val <= right_val for right_val in right_side))):
			newPossibleValues.append(val)
	att.possible_values = newPossibleValues

class Attribute:
	def __init__(self, name, description=None, addresses, possible_values=None, min_value=None, max_value=None, rules=None):
		self.name = name
		self.description = description
		if isinstance(addresses, list):
			self.addresses = addresses
		else:
			self.addresses = [addresses]
		self.possible_values = possible_values
		if (possible_values is None):
			self.possible_values = range(min_value, max_value+1)
		else:
			self.possible_values = [v for v in possible_values if min_value <= v <= max_value]
	def applyRules(self): # this method may need to be reworked into a different type of implementation entirely; see notes below
		for rule in rules:
			rule_type = rule[0]
			if isinstance(args, list):
				args = rule[1]
			else:
				args = [rule[1]]
			applyRule(rule_type, self, args)
	def getValue(self):
		self.value = random.choice(self.possible_values)



"""
NOTES FOR ME

Possible Strategy for Constraint Satisfaction:
get att1 values
get att2 values
apply given rules/constraints on each att2 value, comparing each one to all att1 values
if att2 value fails for all att1 values, remove att2 value
if all att2 values fail for an att1 value, remove the att1 value
if there are no remaining values for an attribute, throw exception (there is no possible combination of attribute values)

Strategy 2 (more feasible) (Constraint Satisfaction with Backtracking)
for each attribute, shuffle all possible values according to seed
set att1 value to first possible_value
apply given rules/constraints to first att2 possible_value, comparing this value to the att1 value
if it passes, move on; if it fails, keep going down the list of possible att2 values until one passes
if no att2 values pass, backtrack to att1 and set its value to the next possible_value, then continue
this will always give a possible solution in a good (enough) amount of time, if one exists
"""