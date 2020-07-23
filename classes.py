import sys
import random
import shutil
import copy
from math import ceil, floor
from os import path, remove, mkdir
from time import sleep
import operator

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

class Attribute:
	def __init__(self, name, addresses, description=None, number_of_bytes=1, possible_values=[], min_value=None, max_value=None):
		self.name = name
		self.description = description
		self.number_of_bytes = number_of_bytes
		if isinstance(addresses, list):
			self.addresses = addresses
		else:
			self.addresses = [addresses]
		self.possible_values = possible_values
		if len(possible_values) == 0:
			self.possible_values = list(range(min_value, max_value+1))
			self.default_possible_values = copy.copy(self.possible_values)
		else:
			self.possible_values = [v for v in possible_values if min_value <= v <= max_value]
			self.default_possible_values = copy.copy(self.possible_values)
		self.specialOperators = []
		self.specialVal = []
	def resetToFirstValue(self):
		self.index = 0
		self.value = self.possible_values[0]
	def resetToDefault(self):
		self.possible_values = copy.copy(self.default_possible_values)
		self.resetToFirstValue()
	def prepare(self):
		random.shuffle(self.possible_values)
		self.resetToFirstValue()
	def setToNextValue(self):
		self.index += 1
		try:
			self.value = self.possible_values[self.index]
			return True
		except:
			# print("Resetting value to start of array.")
			self.resetToFirstValue()
			return False
	# allows rules to perform dynamic operations on attribute value; no pointers necessary!
	def performSpecialOperation(self):
		if len(self.specialOperators) == 0:
			return self.value
		comparedVal = self.value
		for i in range(len(self.specialOperators)):
			func = operator.methodcaller(self.specialOperators[i], comparedVal, self.specialVal[i])
			comparedVal = func(operator)
		return comparedVal
	def __add__(self, val):
		self.specialOperators.append("add")
		self.specialVal.append(val)
		return self
	def __sub__(self, val):
		self.specialOperators.append("sub")
		self.specialVal.append(val)
		return self
	def __mul__(self, val):
		self.specialOperators.append("mul")
		self.specialVal.append(val)
		return self
	def __floordiv__(self, val):
		self.specialOperators.append("floordiv")
		self.specialVal.append(val)
		return self
	def __truediv__(self, val):
		self.specialOperators.append("truediv")
		self.specialVal.append(val)
		return self
	def __mod__(self, val):
		self.specialOperators.append("mod")
		self.specialVal.append(val)
		return self
	def __pow__(self, val):
		self.specialOperators.append("pow")
		self.specialVal.append(val)
		return self
	def __lshift__(self, val):
		self.specialOperators.append("lshift")
		self.specialVal.append(val)
		return self
	def __rshift__(self, val):
		self.specialOperators.append("rshift")
		self.specialVal.append(val)
		return self
	def __and__(self, val):
		self.specialOperators.append("and")
		self.specialVal.append(val)
		return self
	def __xor__(self, val):
		self.specialOperators.append("xor")
		self.specialVal.append(val)
		return self
	def __or__(self, val):
		self.specialOperators.append("or")
		self.specialVal.append(val)
		return self
	def __neg__(self, val):
		self.specialOperators.append("neg")
		self.specialVal.append(val)
		return self
	def __pos__(self, val):
		self.specialOperators.append("pos")
		self.specialVal.append(val)
		return self
	def __abs__(self, val):
		self.specialOperators.append("abs")
		self.specialVal.append(val)
		return self
	def __invert__(self, val):
		self.specialOperators.append("invert")
		self.specialVal.append(val)
		return self

ruleTypesDict = {
	"=" : "eq",
	"==" : "eq",
	"all equal" : "eq",
	"all same" : "eq",
	"!=" : "ne",
	"all not equal" : "ne",
	"all different" : "ne",
	">" : "gt",
	">=" : "ge",
	"=>" : "ge",
	"<" : "lt",
	"<=" : "le",
	"=<" : "le",
}

class Rule:
	def __init__(self, name, left_side, rule_type, right_side=None, description=None):
		self.name = name
		self.description = description
		self.left_side = left_side
		self.rule_type = ruleTypesDict.get(rule_type.lower())
		if self.rule_type is None:
			self.rule_type = rule_type.lower()
		self.right_side = right_side
	def rulePasses(self):
		try:
			if self.rule_type == "eq" and self.right_side is None:
				if not isinstance(self.left_side, list):
					return True
				for i in range(len(self.left_side)-1):
					for j in range(i+1, len(self.left_side)):
						left = self.setSide(self.left_side[i])
						right = self.setSide(self.left_side[j])
						if left != right:
							return False
				return True
			if self.rule_type == "ne" and self.right_side is None:
				if not isinstance(self.left_side, list):
					return True
				for i in range(len(self.left_side)-1):
					for j in range(i+1, len(self.left_side)):
						left = self.setSide(self.left_side[i])
						right = self.setSide(self.left_side[j])
						if left == right:
							return False
				return True
			left = self.setSide(self.left_side)
			right = self.setSide(self.right_side)
			func = operator.methodcaller(self.rule_type, left, right)
			return func(operator)
		except:
			print("Something went wrong. Failed to verify rule.")
			return False
	def setSide(self, side):
		if isinstance(side, Attribute):
			return side.performSpecialOperation()
		else:
			return side