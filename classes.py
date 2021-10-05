import sys
import random
import shutil
import copy
from math import ceil, floor
from time import sleep
import operator

attributeCounter = 0
ruleCounter = 0
defaultRuleNum = 0

def setDefaultRuleNum():
	global defaultRuleNum
	global ruleCounter
	defaultRuleNum = ruleCounter

def resetRuleCounter():
	global ruleCounter
	global defaultRuleNum
	ruleCounter = defaultRuleNum

class Attribute:
	def __init__(self, name, addresses, number_of_bytes=None, is_little_endian=False, possible_values=None, min_value=None, max_value=None, min_max_interval=1, lock_if_enabled=None, lock_unless_enabled=None):
		self.name = name
		if isinstance(addresses, list):
			self.addresses = addresses
		else:
			self.addresses = [addresses]
		for i in range(len(self.addresses)):
			if not isinstance(addresses[i], tuple):
				addresses[i] = (addresses[i], 1)
		self.possible_values = possible_values
		if possible_values is None or len(possible_values) == 0:
			# self.possible_values = list(range(min_value, max_value+1))
			self.possible_values = []
			if min_max_interval is None:
				min_max_interval = 1
			attArraySize = (max_value - min_value) / min_max_interval * sys.getsizeof(int())
			if attArraySize > (1048576*50): # 50 MB
				print("At least one of the provided attributes has a very large number of possible values. This may (or may not) make the program run slow.")
			i = min_value
			while i <= max_value:
				self.possible_values.append(i)
				i += min_max_interval
		else:
			self.possible_values = [v for v in possible_values if (min_value is None or v >= min_value) and (max_value is None or v <= max_value)]
		self.default_possible_values = copy.copy(self.possible_values)
		if number_of_bytes is None:
			self.number_of_bytes = ceil(max(self.possible_values).bit_length() / 8.0)
		else:
			self.number_of_bytes = number_of_bytes
		self.is_little_endian = is_little_endian
		if lock_if_enabled is None:
			self.lock_if_enabled = []
		elif isinstance(lock_if_enabled, list):
			self.lock_if_enabled = lock_if_enabled
		else:
			self.lock_if_enabled = [lock_if_enabled]
		for i in range(len(self.lock_if_enabled)):
			if not isinstance(self.lock_if_enabled[i], tuple):
				self.lock_if_enabled[i] = tuple([self.lock_if_enabled[i]])
		if lock_unless_enabled is None:
			self.lock_unless_enabled = []
		elif isinstance(lock_unless_enabled, list):
			self.lock_unless_enabled = lock_unless_enabled
		else:
			self.lock_unless_enabled = [lock_unless_enabled]
		for i in range(len(self.lock_unless_enabled)):
			if not isinstance(self.lock_unless_enabled[i], tuple):
				self.lock_unless_enabled[i] = tuple([self.lock_unless_enabled[i]])

		self.index = 0
		self.value = self.possible_values[0]
		self.specialOperators = []
		self.specialVals = []
		self.rulesOnSpecialOp = []
		global attributeCounter
		self.attributeNum = attributeCounter
		attributeCounter += 1
	def resetToFirstValue(self):
		self.index = 0
		self.value = self.possible_values[0]
	def resetToDefault(self):
		self.possible_values = copy.copy(self.default_possible_values)
		self.resetToFirstValue()
	def prepare(self):
		random.shuffle(self.possible_values)
		self.resetToFirstValue()
	def setToPreviousValue(self):
		self.index -= 1
		self.value = self.possible_values[self.index]
	def setToNextValue(self):
		self.index += 1
		try:
			self.value = self.possible_values[self.index]
			return True
		except:
			self.resetToFirstValue()
			return False
	# Allows rules to perform dynamic operations on attribute value; no pointers necessary!
	def performSpecialOperation(self, ruleNum):
		if len(self.specialOperators) == 0:
			return self.value
		comparedVal = self.value
		for i in range(len(self.specialOperators)):
			if self.rulesOnSpecialOp[i] == ruleNum:
				if self.specialVals[i] is not None:
					if not isinstance(self.specialVals[i], Attribute):
						func = operator.methodcaller(self.specialOperators[i], comparedVal, self.specialVals[i])
					else:
						func = operator.methodcaller(self.specialOperators[i], comparedVal, self.specialVals[i].performSpecialOperation(ruleNum))
				else:
					func = operator.methodcaller(self.specialOperators[i], comparedVal)
				comparedVal = func(operator)
		return comparedVal
	# Whenever a calculation (arithmetic, comparison, etc) is attempted on an Attribute, store it for use later.
	def addSpecialOperator(self, op, val):
		global ruleCounter

		self.specialOperators.append(op)
		self.specialVals.append(val)
		self.rulesOnSpecialOp.append(ruleCounter)
		return self
	def duplicateOperations(self, oldRuleNum, newRuleNum):
		newSO = copy.copy(self.specialOperators)
		newSV = copy.copy(self.specialVals)
		newROSO = copy.copy(self.rulesOnSpecialOp)
		for i in range(len(self.rulesOnSpecialOp)):
			if self.rulesOnSpecialOp[i] == oldRuleNum:
				newSO.append(self.specialOperators[i])
				newSV.append(self.specialVals[i])
				newROSO.append(newRuleNum)
		self.specialOperators = newSO
		self.specialVals = newSV
		self.rulesOnSpecialOp = newROSO
	def __add__(self, val):
		return self.addSpecialOperator("add", val)
	def __sub__(self, val):
		return self.addSpecialOperator("sub", val)
	def __mul__(self, val):
		return self.addSpecialOperator("mul", val)
	def __floordiv__(self, val):
		return self.addSpecialOperator("floordiv", val)
	def __truediv__(self, val):
		return self.addSpecialOperator("truediv", val)
	def __mod__(self, val):
		return self.addSpecialOperator("mod", val)
	def __pow__(self, val):
		return self.addSpecialOperator("pow", val)
	def __lshift__(self, val):
		return self.addSpecialOperator("lshift", val)
	def __rshift__(self, val):
		return self.addSpecialOperator("rshift", val)
	def __and__(self, val):
		return self.addSpecialOperator("and", val)
	def __xor__(self, val):
		return self.addSpecialOperator("xor", val)
	def __or__(self, val):
		return self.addSpecialOperator("or", val)
	def __neg__(self):
		return self.addSpecialOperator("neg", None)
	def __pos__(self):
		return self.addSpecialOperator("pos", None)
	def __abs__(self):
		return self.addSpecialOperator("abs", None)
	def __invert__(self):
		return self.addSpecialOperator("invert", None)

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
	"in" : "eq",
	"is in" : "eq",
	"is one of" : "eq",
	"not in" : "ne",
	"is not in" : "ne",
	"is not one of" : "ne",
	"count" : "count",
}

ruleTypesOtherDict = {
	"eq" : "==",
	"ne" : "!=",
	"gt" : ">",
	"ge" : ">=",
	"lt" : "<",
	"le" : "<=",
	"count" : "count",
}

class Rule:
	def __init__(self, left_side, rule_type, right_side=None, description="", oldRuleNum=None):
		self.description = description
		if self.description is None:
			self.description = ""
		self.left_side = left_side
		self.rule_type = ruleTypesDict.get(rule_type.lower())
		if self.rule_type is None:
			self.rule_type = rule_type.lower()
		self.right_side = right_side
		global ruleCounter
		self.ruleNum = ruleCounter
		if oldRuleNum is not None:
			self.left_side = self.handleMidStatementAssertion(self.left_side, oldRuleNum, self.ruleNum)
			self.right_side = self.handleMidStatementAssertion(self.right_side, oldRuleNum, self.ruleNum)
		ruleCounter += 1
		self.relatedAttributes = []
		self.storeRelatedAttributes(self.left_side)
		self.storeRelatedAttributes(self.right_side)
	def storeRelatedAttributes(self, att):
		if isinstance(att, Attribute):
			if not att in self.relatedAttributes:
				self.relatedAttributes.append(att)
			for val in att.specialVals:
				self.storeRelatedAttributes(val)
		elif isinstance(att, list) or isinstance(att, tuple):
			for a in att:
				self.storeRelatedAttributes(a)
	# Used for OR statements and other mid-statement comparisons/assertions
	def handleMidStatementAssertion(self, att, oldRuleNum, newRuleNum):
		if isinstance(att, tuple) and isinstance(att[0], Attribute):
			att[0].duplicateOperations(oldRuleNum, newRuleNum)
			return att[0].addSpecialOperator(ruleTypesDict.get(att[1]), att[2])
		elif isinstance(att, list):
			for i in range(len(att)):
				att[i] = self.handleMidStatementAssertion(att[i], oldRuleNum, newRuleNum)
		return att
	def rulePasses(self):
		try:
			if self.rule_type == "eq" and self.right_side is not None:
				left = self.setSide(self.left_side)
				right = []
				for att in self.asList(self.right_side):
					right.append(self.setSide(att))
				return left in right
			elif self.rule_type == "count":
				left = self.asList(self.left_side)
				newLeft = []
				for i in range(len(left)):
					newLeft.append(self.setSide(left[i]))
				left = newLeft
				if self.right_side[0] in ["=","=="]:
					count = sum(map(lambda x : x==self.right_side[1], left))
				elif self.right_side[0] == "!=":
					count = sum(map(lambda x : x!=self.right_side[1], left))
				elif self.right_side[0] == ">":
					count = sum(map(lambda x : x>self.right_side[1], left))
				elif self.right_side[0] == ">=":
					count = sum(map(lambda x : x>=self.right_side[1], left))
				elif self.right_side[0] == "<":
					count = sum(map(lambda x : x<self.right_side[1], left))
				elif self.right_side[0] == "<=":
					count = sum(map(lambda x : x<=self.right_side[1], left))
				rule_type = ruleTypesDict.get(self.right_side[2].lower())
				func = operator.methodcaller(rule_type, count, self.right_side[3])
				return func(operator)
			else:
				left = self.setSide(self.left_side)
				right = self.setSide(self.right_side)
				func = operator.methodcaller(self.rule_type, left, right)
				return func(operator)
		except:
			print("Something went wrong. Failed to verify rule.")
			return False
	# Breaks most large rules down into several smaller rules, heavily reducing computation time.
	def simplifyRule(self, rulesArray):
		newDescription = "Generated "+ruleTypesOtherDict.get(self.rule_type)
		if self.rule_type == "eq" and self.right_side is None:
			for i in range(1, len(self.left_side)):
				newRule = Rule(description=newDescription, left_side=self.left_side[0], rule_type="==", right_side=self.left_side[i], oldRuleNum=self.ruleNum)
				rulesArray.append(newRule)
		elif self.rule_type == "ne" and self.right_side is None:
			for i in range(len(self.left_side)-1):
				for j in range(i+1, len(self.left_side)):
					newRule = Rule(description=newDescription, left_side=self.left_side[i], rule_type="!=", right_side=self.left_side[j], oldRuleNum=self.ruleNum)
					rulesArray.append(newRule)
		elif self.rule_type in ["eq","ne","gt","ge","lt","le"]:
			for lVal in self.asList(self.left_side):
				for rVal in self.asList(self.right_side):
					newRule = Rule(description=newDescription, left_side=lVal, rule_type=self.rule_type, right_side=rVal, oldRuleNum=self.ruleNum)
					rulesArray.append(newRule)
		else:
			newRule = Rule(description=self.description, left_side=self.left_side, rule_type=self.rule_type, right_side=self.right_side, oldRuleNum=self.ruleNum)
			rulesArray.append(newRule)
	def asList(self, side):
		if isinstance(side, list):
			return side
		else:
			return [side]
	def setSide(self, side):
		if isinstance(side, Attribute):
			return side.performSpecialOperation(self.ruleNum)
		else:
			return side

class Ruleset:
	def __init__(self, name=None, description=None, rules=[], must_be_enabled=[], must_be_disabled=[]):
		self.originalName = name
		tempFullStr = ""
		tempWordArr = name.split(" ")
		lineLenCounter = 0
		for word in tempWordArr:
		    if (lineLenCounter + len(word) + 1 <= (25 + 1)):
		        tempFullStr += word + " "
		        lineLenCounter += len(word) + 1
		    else:
		        tempFullStr += '\n' + word + " "
		        lineLenCounter = 0
		self.name = tempFullStr.strip()
		self.description = description
		self.rules = rules
		if must_be_enabled is None:
			self.must_be_enabled = []
		elif isinstance(must_be_enabled, list):
			self.must_be_enabled = must_be_enabled
		else:
			self.must_be_enabled = [must_be_enabled]
		if must_be_disabled is None:
			self.must_be_disabled = []
		elif isinstance(must_be_disabled, list):
			self.must_be_disabled = must_be_disabled
		else:
			self.must_be_disabled = [must_be_disabled]
	def addRule(rule):
		self.rules.append(rule)
