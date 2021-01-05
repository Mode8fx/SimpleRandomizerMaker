# Welcome to the Simple Randomizer Maker tutorial!

I recommend you read this file using [GitHub's reader](https://github.com/GateGuy/SimpleRandomizerMaker/blob/master/Readme%20%28Tutorial%29.md).

This will explain what you can create for your randomizer and how to do it, through both written documentation and code snippets. Or if you'd rather learn by example, there are two templates included that feature everything explained here.

If you want to edit one of the templates, keep in mind that you need to rename it to `randomizer.py`.

## Settings
First, the settings for the randomizer itself:

##### Program Name
- The name of the randomizer.

##### Rom Name
- The name of the rom/game that's compatible with the randomizer. The rom doesn't have to have this exact name, it's just there to guide the user.
`"Kirby & The Amazing Mirror"`
- If your game uses multiple files (such as some PC or PS1 games), this should be an array containing the names of each file.
`["Metal Gear Solid (Disc 1)", "Metal Gear Solid (Disc 2)"]`

##### ROM File Format
- (optional) The file format of the ROM ("nes", "gba", etc).
- If you want to allow any file type, leave it as ""
- If your game uses multiple files of different types (such as some games), this should be an array containing the types of each file, in order.
`["exe", "bin"]`

##### About Page Text
- Any text you want to put on the "About..." page on the menu bar.
- If you don't want an About page, leave it as ""

##### Timeout
- The number of seconds you want to wait per seed before the randomizer times out. If you don't want a timeout, leave it as 0.
- It is recommended that you at least set a timeout during testing so you can know how long it takes to create a seed.

##### Slow Mode
- Setting this to True changes the seed generation to a much slower method. This is a debug setting, so it's recommended that you leave this as False unless you're having trouble getting your randomizer to work.

## Attribute

Now, there are three main components that make up your randomizer. The first of these is an Attribute.

An Attribute is anything you want to change the value for, such as item price, enemy health, base stats, and so on. Attributes are created in an array called attributes.

An Attribute has the following components:

##### Name
- The name of the Attribute.

##### Addresses
- The memory address(es) of the Attribute. These addresses must be in an array, meaning you separate them with commas and put them all between brackets.
`[0x01234, 0x56789, 0xABCDE]`
- These are hex addresses, so remember to put 0x in front of each one.
- If your game uses multiple files, each address should instead be a tuple (parentheses) containing both the address and the index of which file this address belongs to (1 for the first file, 2 for the second, etc). If unspecified, the first file is modified.
`[(0x01234, 2), (0x56789, 2), (0xABCDE, 2)]`

##### Number of Bytes
- (optional) The number of bytes taken up by each of these addresses. If you don't know what this means, leave it as None (the program will attempt to guess).

##### Is Little Endian
- (optional) If True, the game uses a little-endian system, meaning bytes are read - and should be written - in reverse order. If you don't know what this means, leave it as False.
- If your created randomizer produces unexpected results (the correct attributes are changed to the wrong values), it could be because the system uses little-endian.

##### Possible Values
- (semi-optional) An array of possible values for this Attribute. The addresses will be set to one of these values.
`[1, 4, 21, 83, 106]`
- An Attribute must use either Possible Values or both Min Value and Max Value (see below).

##### Min Value
- (semi-optional) The smallest possible value.

##### Max Value
- (semi-optional) The largest possible value. EXAMPLE: setting min_value to 5 and max_value to 10 will make the possible values [5,6,7,8,9,10].

##### Min-Max Interval
- (semi-optional) If using Min Value and Max Value, this is the interval. EXAMPLE: setting min_value=20, max_value=65, and min_max_interval=10 will make the possible values [20,30,40,50,60].

If you choose not to use one of the optional variables, set its value to None

#### Attribute Examples
A code example can be found below. If you're using this file as a template, MAKE SURE YOU DELETE THESE ATTRIBUTES!
```
Attributes = [
	Attribute(
		name="My Attribute 1",
		addresses=[0x0123],
		number_of_bytes=1,
		is_little_endian=False,
		possible_values=None,
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
		min_value=None,
		max_value=None,
		min_max_interval=None
	),
	Attribute(
		name="My Attribute 3",
		addresses=[0x147, 0x258, 0x369],
		number_of_bytes=2,
		is_little_endian=False,
		possible_values=[0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300],
		min_value=None,
		max_value=None,
		min_max_interval=None
	),
]
```
## Rule

This is the second component.

A Rule is a requirement (a constraint) that the randomized values must follow. This is useful if you want certain Attributes to depend on others. For example, if you want to randomize the prices of two healing items (we'll call them Potion and Super Potion), you can guarantee that the Super Potion will always cost at least twice as much as a regular Potion. You can also take an array of Attributes and guarantee that they will all have the same or different values. You can have as many or as few Rules as you'd like.

Rules that you want to always apply are stored in an array called required_rules. If you don't want any required rules (or any rules at all), keep the array as:
`Required_Rules = []`

A Rule has the following components:

##### Description
- (optional) A description of the Rule. This isn't actually used for anything, but it can be useful for organizing your Rules.

##### Left Side
- The first part of the rule. If you think of a rule as an equation like "a + b > c", then Left Side is "a + b", Rule Type (see below) is ">", and Right Side (also see below) is "c".

##### Rule Type
- The type of comparison. Possible comparisons are:
  `"=" (or "=="), "!=", ">", ">=", "<", "<=", and "count"`
- Most of these are self-explanatory, but the "count" comparison lets you count how many attributes fulfill a certain requirement (see EXAMPLE 3 below).

##### Right Side
- The right side of the comparison (may be unused, depending on the rule).

If you choose not to use one of the optional variables, set its value to None

#### Rule Examples
- EXAMPLE 1: If you want to set a requirement that a Super Potion must cost at least as much as (two Potions + 100), then you would set the following:
```
Rule(
	left_side=value("Super Poiton"),
	rule_type=">=",
	right_side=value("Potion")*2+100,
)
```
- EXAMPLE 2: If you want to guarantee that a Potion, Elixir, and Revive all cost the same amount, then you would set the following:
```
Rule(
	left_side=[value("Potion"), value("Elixir"), value("Revive")],
	rule_type="=",
	right_side=None,
)
```
- EXAMPLE 3: If you have four stats and you want to guarantee that at most (<=) two of them are greater than (>) 100 each, then you would set the following:
```
Rule(
	left_side=[value("Attack"), value("Defense"), value("Speed"), value("Magic")],
	rule_type = "count",
	right_side = (">", 100, "<=", 2),
)
```
The Right Side represents: (value rule type, value, count rule type, count), and it must be in parentheses.

A code example can be found below. If you're using this file as a template, MAKE SURE YOU DELETE THESE RULES!
```
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
```
## Ruleset

The third and final component is simpler than the other two because it's basically a set of rules, fittingly named a Ruleset.

A Ruleset is a collection of optional Rules that may be enabled or disabled by the user. This is useful if you want to add optional user settings without having to create multiple randomizers. You can create up to 14 Rulesets, not counting the required Rules above.

Rulesets are stored in an array called optional_rulesets. If you don't want any optional rulesets, keep the array as:
`Optional_Rulesets = []`

A Ruleset has the following variables:

##### Name
- The name of the Ruleset.

##### Description
(optional) A description of the ruleset. This is what appears when you move your mouse over the ruleset.

##### Rules
- An array of Rules that are applied if the Ruleset is enabled.

##### Must Be Enabled
- (optional) An array of Ruleset names. This Ruleset can only be enabled if all of the optional Rulesets in this array are also enabled.

##### Must Be Disabled
- (optional) An array of Ruleset names. This Ruleset can only be enabled if all of the optional Rulesets in this array are disabled.

If you choose not to use one of the optional variables, set its value to None

#### Ruleset Examples (+ More Rule Examples)
A code example can be found below. If you're using this file as a template, MAKE SURE YOU DELETE THESE RULESETS!
```
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
	),
	Ruleset(
		name="Special Ruleset",
		description="This can only be enabled if My Ruleset 1 is enabled and My Ruleset 2 is disabled.",
		rules=[],
		must_be_enabled=["My Ruleset 1"],
		must_be_disabled=["My Ruleset 2"],
	),
]
```
## Tips

That's everything you need to know to make your own randomizer! But here are a few more tips if you want them:

##### Advanced Rules
- Look back at Ruleset #2 in the Rulesets section. If you're creative (and have a little bit of coding experience), you can push the boundaries and come up with some interesting rules. You can add OR (or XOR) statements, check if values are divisible by certain numbers, perform bitwise operations on them, and more.
- See the Amazing Mirror Template for an example of an XOR statement. If you want to make something like an OR or XOR statement, remember that a statement returns 1 or 0 if it's True or False respectively. For example, this statement:
`(value("Attribute 1"), ">", 5)`
... will be equivalent to 1 if Attribute 1 is greater than 5, or 0 if Attribute 1 is not greater than 5.

##### No Unnecessary Arrays
- When inputting addresses, left_side, right_side, must_be_enabled, or must_be_disabled, you don't have to use an array if you are only using one value.

For example, either of these will work the same:
```
addresses = [0x12345]
addresses = 0x12345
```

... or these:
```
left_side = [value("A")]
left_side = value("A")
```

##### Rule Compression
- For most Rule types (everything except "==" and "count"), you can set the Left Side and Right Side as arrays of multiple values each, and comparisons will be performed on every combination of Left Side and Right Side value. For example, this rule:
```
Rule(
	description="Several comparisons",
	left_side=[value("A"), value("B")],
	rule_type=">",
	right_side=[value("C"), value("D")],
)
```
... will check all of (A > C), (A > D), (B > C), and (B > D). Nested rules like this are automatically broken down into smaller rules, so in most situations, you won't have to worry about breaking them down yourself.

##### Speed/Timeout
- Optimization algorithms are used to speed up seed generation. But if your randomizer is going too slow, see if you have any "count" rules and consider reworking them into something else; "count" doesn't work as well with optimization. If it's still too slow, see if increasing your Timeout by a few seconds solves it.

##### Turning Your Randomizer Into An Executable
- When distributing your newly-created randomizer, all you need to do is package your `randomizer.py` file with a copy of the Simple Randomizer Maker executable. But if you want to combine them into one file instead, you can use a program like PyInstaller to package `srm.py` (the main Simple Randomizer Maker script that the EXE runs) with your randomizer file to make a single executable. If you use PyInstaller, just make sure `srm.py`, `gatelib.py`, `classes.py`, and your `randomizer.py` are all in the same directory, make sure you have SRM's dependencies (and PyInstaller) installed, then open a command window in that directory and run `pyinstaller srm.py --onefile --windowed --name "NAME"`, where NAME is the name of your randomizer. Your executable will be saved as `YOUR DIRECTORY/dist/NAME.exe`.

##### No Solution?
- In case you run into a situation where your randomizer gives an error that no possible combination of values was found: Look through your Attributes and Rules again and make sure they can actually generate a solution. That includes making sure two enabled optional rulesets don't conflict with each other. You can also try running the randomizer a few more times; maybe you just got a bad seed. Otherwise, read on.
- Backtracking constraint satisfaction is used to heavily speed up seed generation. By "heavily", I mean "a rule that used to take ~10 hours to apply now takes less than a second". If your randomizer gives an error that no solution was found, you can try setting Slow_Mode to True; this will make the randomizer use brute force calculation instead, which has a *very slight* chance of fixing your problem. But again, make sure your Rules/Attributes can actually generate a solution before attempting this.