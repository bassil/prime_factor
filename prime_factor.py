"""refactor of prime_factor_processor:

reads input from the command line, 
verifies that the input is an integer, and
writes back a list of prime factors for the input

Usage instructions:
	- Execute the python file: 
		$ python ./prime_factor.py
	- when prompted, imput an integer:
		$ Please enter an integer: <insert integer here>

Uses unittest test suite -- Testing functionality of:
	- get_prime_factors - are the returned factors prime?
	- is_prime - is the integer actually prime?
	- previously_found_factors - if factors have been persisted, do they get returned?
	- persist_factors - are factors being persisted?


FIXME - Continuous integeration on new commits -- e.g.,
	$ python -m unittest tests/test_prime_factor.py -v

Refactoring philosophy for the first pass --
	write a naive version
	the functionality is decoupled - to find the prime factors, we find the factors, 
		and if it is prime, then we add it to the prime factors list
	Note: this version implements a naive prime factorization algorithm, and
	 	is really inefficient - e.g., 
		Trying to find the prime factors of 6546541851651256156 took too long :()

Future refactoring passes:
	- implement a more efficient is_prime algorithm 
		(e.g., currently, linear with the size of the input int)
	- implement a more efficient get_prime_factors
		(e.g., currently, quadratic with the size of the input int)
	- is there a more efficient way to persist/load previously computed prime factors?
"""

import os
import pickle

from pathlib import Path

def persist_factors(input_int, factors, factors_file):
	"""if input_int not in factors_file, persist input factors to factors_file
	
	In this implementation, we're persisting by pickling, e.g., 
		serializing a dict {input_int: [factors]} Python object
		We're assuming that the O(1) lookup for a given input_int 
		offsets the pickling/depickling overhead for a large enough factors_file
		Some alternatives include adding a line to a csv w/ columns:
		[input_int, factors], or a database table indexed on input_int for fast lookups

	Args:

	input_int - int
		an integer for which we want to persist computed prime factors
	factors - list[int]
		list of prime factors of input_int
	factors_file - string
		path to file storing serialized dictionary of {integers: [prime factors]}
	"""

	try:
		with open(factors_file, 'rb') as file:
			factors_dict = pickle.load(file)
	except:
		if not os.path.exists(factors_file):
			Path(factors_file).touch()
			factors_dict = {}

	# add the factors to the dict
	factors_dict[input_int] = factors
	
	# serialize the dict factors_file
	with open(factors_file, 'wb') as file:
		pickle.dump(factors_dict, file, pickle.HIGHEST_PROTOCOL)

def previously_found_factors(input_int, factors_file):
	"""checks for input_int in factors_file, returns factors if found, otherwise false
	
	In this implementation, we're unpickling, e.g.,
		de-serializing the byte stream into a dict {input_int: [factors]} Python object

	Args:

	input_int - int
		an integer we want to determine if previously computed prime factors
	factors_file - string
		path to file storing serialized dictionary of {integers: [prime factors]}
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

	>>> get_prime_factors(27, "data/prime_factors.pkl")
	[3]
	>>> get_prime_factors(42, "data/prime_factors.pkl")
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
	print(get_prime_factors(user_input, os.path.join("data", "prime_factors.pkl")))
