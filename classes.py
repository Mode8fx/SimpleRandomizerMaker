import sys
import random
import shutil
import copy
from math import ceil, floor
from os import path, remove, mkdir
from time import sleep
import operator

currRule = 0
ruleCounter = 0

def increaseRuleCounter():
	global ruleCounter
	ruleCounter += 1

def setCurrRule(val):
	global currRule
	currRule = val

class Attribute:
	def __init__(self, name, addresses, number_of_bytes=None, possible_values=None, min_value=None, max_value=None):
		self.name = name
		if isinstance(addresses, list):
			self.addresses = addresses
		else:
			self.addresses = [addresses]
		self.possible_values = possible_values
		if possible_values is None or len(possible_values) == 0:
			self.possible_values = list(range(min_value, max_value+1))
			self.default_possible_values = copy.copy(self.possible_values)
		else:
			self.possible_values = [v for v in possible_values if (min_value is None or v >= min_value) and (max_value is None or v <= max_value)]
			self.default_possible_values = copy.copy(self.possible_values)
		if number_of_bytes is None:
			self.number_of_bytes = ceil(max(self.possible_values).bit_length() / 8.0)
		else:
			self.number_of_bytes = number_of_bytes
		self.specialOperators = []
		self.specialVal = []
		self.ruleOnSpecialOp = []
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
			self.resetToFirstValue()
			return False
	# allows rules to perform dynamic operations on attribute value; no pointers necessary!
	def performSpecialOperation(self):
		if len(self.specialOperators) == 0:
			return self.value
		comparedVal = self.value
		global currRule
		for i in range(len(self.specialOperators)):
			if self.ruleOnSpecialOp[i] is currRule:
				if self.specialVal[i] is not None:
					if not isinstance(self.specialVal[i], Attribute):
						func = operator.methodcaller(self.specialOperators[i], comparedVal, self.specialVal[i])
					else:
						# if self.value == 4:
						# 	print("shift")
						# 	print(currRule)
						func = operator.methodcaller(self.specialOperators[i], comparedVal, self.specialVal[i].performSpecialOperation())
				else:
					func = operator.methodcaller(self.specialOperators[i], comparedVal)
				comparedVal = func(operator)
				# if self.value == 4:
				# 	print("here")
				# 	print(currRule)
				# 	print(comparedVal)
				# 	print(self.specialOperators[i])
				# 	print(self.specialVal[i])
		return comparedVal
	def __add__(self, val):
		global currRule
		self.specialOperators.append("add")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __sub__(self, val):
		global currRule
		self.specialOperators.append("sub")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __mul__(self, val):
		global currRule
		self.specialOperators.append("mul")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __floordiv__(self, val):
		global currRule
		self.specialOperators.append("floordiv")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __truediv__(self, val):
		global currRule
		self.specialOperators.append("truediv")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __mod__(self, val):
		global currRule
		self.specialOperators.append("mod")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __pow__(self, val):
		global currRule
		self.specialOperators.append("pow")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __lshift__(self, val):
		global currRule
		self.specialOperators.append("lshift")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __rshift__(self, val):
		global currRule
		self.specialOperators.append("rshift")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __and__(self, val):
		global currRule
		self.specialOperators.append("and")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __xor__(self, val):
		global currRule
		self.specialOperators.append("xor")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __or__(self, val):
		global currRule
		self.specialOperators.append("or")
		self.specialVal.append(val)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __neg__(self):
		global currRule
		self.specialOperators.append("neg")
		self.specialVal.append(None)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __pos__(self):
		global currRule
		self.specialOperators.append("pos")
		self.specialVal.append(None)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __abs__(self):
		global currRule
		self.specialOperators.append("abs")
		self.specialVal.append(None)
		self.ruleOnSpecialOp.append(currRule)
		return self
	def __invert__(self):
		global currRule
		self.specialOperators.append("invert")
		self.specialVal.append(None)
		self.ruleOnSpecialOp.append(currRule)
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

invertedRuleTypesDict = {
	"eq" : "eq",
	"ne" : "ne",
	"gt" : "lt",
	"ge" : "le",
	"lt" : "gt",
	"le" : "ge",
}

class Rule:
	def __init__(self, left_side, rule_type, right_side=None, description=None):
		self.description = description
		self.left_side = left_side
		self.rule_type = ruleTypesDict.get(rule_type.lower())
		if self.rule_type is None:
			self.rule_type = rule_type.lower()
		self.right_side = right_side
		global ruleCounter
		self.ruleNum = ruleCounter
		increaseRuleCounter()
		currRule = self.ruleNum
	def rulePasses(self):
		# try:
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
		if not isinstance(right, Attribute):
			func = operator.methodcaller(self.rule_type, left, right)
		else:
			func = operator.methodcaller(self.rule_type, left, right)
		return func(operator)
		# except:
		# 	print("Something went wrong. Failed to verify rule.")
		# 	return False
	def setSide(self, side):
		if isinstance(side, Attribute):
			global currRule
			currRule = self.ruleNum
			return side.performSpecialOperation()
		else:
			return side

class Ruleset:
	def __init__(self, name=None, description=None, rules=[], must_be_enabled=[], must_be_disabled=[]):
		self.name = name
		self.description = description
		self.rules = rules
		if must_be_enabled is None:
			self.must_be_enabled = []
		elif isinstance(must_be_enabled, list):
			self.must_be_enabled = must_be_enabled
		else:
			self.must_be_enabled = must_be_enabled
		if must_be_disabled is None:
			self.must_be_disabled = []
		elif isinstance(must_be_disabled, list):
			self.must_be_disabled = must_be_disabled
		else:
			self.must_be_disabled = must_be_disabled
	def addRule(rule):
		self.rules.append(rule)
