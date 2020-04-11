"""refactor of prime_factor_processor:

reads input from the command line, 
verifies that the input is an integer, and
writes back a list of prime factors for the input

Usage instructions:
	- python ./prime_factor.py
	- when prompted, imput an integer

Uses doctest test suite -- Testing functionality of:
	- get_prime_factors - are the returned factors prime
	- is_prime - is the integer actually prime
	- previously_found_factors - 

FIXME - Continuous integeration on new commits -- e.g.,
	python -m doctest -v prime_factor.py

First pass refactoring philosophy --
	write the simplest version
	Note: this version is really inefficient - 
		Trying to find the prime factors of 6546541851651256156 took too long :()
"""

import os
import pickle

from pathlib import Path

def persist_factors(input_int, factors, factors_file):
	"""if input_int not in factors_file, persist input factors to file ./found_factors.txt

	Args:

	input_int - int
		an integer for which we want to persist computed prime factors
	factors - list[int]
		list of prime factors of input_int
	factors_file - string
		path to file storing serialized dictionary of {integers: [prime factors]}

	Example Usage: FIXME - add test cases
	"""

	if not os.path.exists(factors_file):
		Path(factors_file).touch()
	if os.path.getsize(factors_file) > 0:
		with open(factors_file, 'rb') as file:
			factors_dict = pickle.load(file)
	else:
		factors_dict = {}

	factors_dict[input_int] = factors
	
	with open(factors_file, 'wb') as file:
		pickle.dump(factors_dict, file, pickle.HIGHEST_PROTOCOL)

def previously_found_factors(input_int, factors_file):
	"""checks for input_int in factors_file, returns factors if found, otherwise false
	
	Args:

	input_int - int
		an integer we want to determine if previously computed prime factors
	factors_file - string
		path to file storing serialized dictionary of {integers: [prime factors]}
	
	Example Usage: FIXME - add test cases
	"""
	try:
		with open(factors_file, 'rb') as file:
			factors_dict = pickle.load(file)
			if input_int in factors_dict.keys():
				return factors_dict[input_int]
			else:
				return False
	except:
		return False

def is_prime(input_int):
	"""return boolean whether an input_int is prime or not
	time complexity: O(input_int)
	Args:

	input_int - int
		an integer we want to determine is prime or not

	Example Usage:

	>>> is_prime(27)
	False
	>>> is_prime(43)
	True
	"""
	factors = []
	# Again, simplest, most naive implementation
	for possible_factor in range(1, input_int + 1):
		if input_int % possible_factor == 0:
			factors.append(possible_factor)

	return factors == [1, input_int]

def get_prime_factors(input_int, factors_file):
	"""return the prime factors of the input_int
	time complexity: O(input_int)*O(is_prime) = O(input_int^2)

	Args:

	input_int - int
		an integer for which we want the prime factors

	# note: this is a good time to work out a few examples on paper and
	# define our test cases.
	# Working out some examples can help us determine the algorithm we will implement

	Example Usage:

	>>> get_prime_factors(27)
	[3]
	>>> get_prime_factors(42)
	[2, 3, 7]
	"""

	# this is the simplest, most naive implementation 
	prime_factors = []
	# first, check if found factors before
	if previously_found_factors(input_int, factors_file):
		return previously_found_factors(input_int, factors_file)

	# otherwise, determine all factors of the input int
	for possible_factor in range(2, input_int):
		if input_int % possible_factor == 0:
			# wouldn't it be nice if we had a function that told us if a number was prime?
			if is_prime(possible_factor):
				prime_factors.append(possible_factor)
	persist_factors(input_int, prime_factors, factors_file)
	return prime_factors

if __name__ == '__main__':

	# take input -- python has a function input() that prompts a user for input
	user_input = ""

	# we instantiate user_input as a str so that the while loop executes at least once
	while type(user_input) != int:
		try:
			user_input = int(input("Please enter an integer: "))
		except:
			print("You didn't enter an integer, please try again.")

	# now that we have an integer, we need to find its prime factors
	# suppose we had a function that, given an int, returns its prime factors.
	print(get_prime_factors(user_input, "prime_factors.pkl"))
