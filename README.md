# Simple Randomizer Maker
This is a program that allows you to easily create your own game randomizer with little to no coding.

## How It Works
All you need are the ROM addresses of whatever you want to change, along with possible values for those addresses, and the maker will do everything else for you, from the actual randomization to the GUI. You can make address values completely random, or you can set rules that they must follow (like if you want certain values to change according to other values).

## Features
- Create a randomizer with (basically) no coding
- Add optional rulesets to make your randomizer more complex (while keeping it easy to develop)
- Dynamic GUI that changes according to settings and number of options
- Built-in seed support with verification to check for invalid seeds
- Generate up to 20 unique seeds at once
- Supports multi-byte addresses
- Optionally generate a text log of all randomized values
- Includes detailed tutorial+template plus a sample randomizer

## Example Functions
I recommend you look at the included tutorial, but the short version is that this maker works through three types of objects: Attributes (the things you want to randomize), Rules (requirements that the randomized values must follow), and Rulesets (sets of Rules that are grouped together). Here are some samples:

`Attribute(
	name="My Attribute",
	addresses=[0x456, 0xABC],
	number_of_bytes=1,
	possible_values=[1,4,21,83,106],
	min_value=None,
	max_value=None,
),
Rule(
	description="My Attribute 2 + My Attribute 3 is at least 20",
	left_side=value("My Attribute 2") + value("My Attribute 3"),
	rule_type=">=",
	right_side=20,
),`
