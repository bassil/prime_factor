import unittest

import os
import pickle
import sys

sys.path.append(os.path.join(os.getcwd(), ".."))

import prime_factor


class TestIsPrime(unittest.TestCase):

	def test_is_prime_1(self):
		self.assertEqual(prime_factor.is_prime(27), False)

	def test_is_prime_2(self):
		self.assertEqual(prime_factor.is_prime(43), True)


class TestGetPrimeFactors(unittest.TestCase):
	
	def setUp(self):
		self.factors_file = os.path.join("data", "test_prime_factors.pkl")

	def tearDown(self):
		os.remove(self.factors_file)

	def test_get_prime_factors_1(self):
		self.assertEqual(prime_factor.get_prime_factors(27, self.factors_file), [3])

	def test_get_prime_factors_2(self):
		self.assertEqual(prime_factor.get_prime_factors(42, self.factors_file), [2, 3, 7])


class TestPreviouslyFoundFactors1(unittest.TestCase):

	def setUp(self):
		self.factors_file = os.path.join("data", "test_previously_found_factors_1.pkl")
		prime_factor.get_prime_factors(27, self.factors_file)
		prime_factor.get_prime_factors(42, self.factors_file)

	def tearDown(self):
		os.remove(self.factors_file)

	def test_previously_found_factors_1(self):
		self.assertEqual(prime_factor.previously_found_factors(27, self.factors_file),
						 [3])

	def test_previously_found_factors_2(self):
		self.assertEqual(prime_factor.previously_found_factors(42, self.factors_file),
						 [2, 3, 7])

	def test_previously_found_factors_not_found(self):
		self.assertEqual(prime_factor.previously_found_factors(43, self.factors_file),
						 False)


class TestPreviouslyFoundFactors2(unittest.TestCase):

	def setUp(self):
		self.factors_file = os.path.join("data", "test_previously_found_factors_2.pkl")

	def test_previously_found_factors_file_not_exists(self):
		self.assertEqual(prime_factor.previously_found_factors(27, self.factors_file),
						 False)

	def test_previously_found_factors_file_empty(self):
		open(self.factors_file, 'a').close()
		self.assertEqual(prime_factor.previously_found_factors(27, self.factors_file),
						 False)
		os.remove(self.factors_file)
		

class TestPersistFactors(unittest.TestCase):

	def setUp(self):
		self.factors_file = os.path.join("data", "test_persist_factors.pkl")

	def tearDown(self):
		os.remove(self.factors_file)

	def test_persist_factors_file_not_exists_1(self):
		prime_factor.persist_factors(27, [3], self.factors_file)
		self.assertEqual(prime_factor.previously_found_factors(27, self.factors_file),
						 [3])

	def test_persist_factors_file_not_exists_2(self):
		prime_factor.persist_factors(42, [2, 3, 7], self.factors_file)
		self.assertEqual(prime_factor.previously_found_factors(42, self.factors_file),
						 [2, 3, 7])

	def test_persist_factors_file_empty(self):
		with open(self.factors_file, 'wb') as file:
			pickle.dump({}, file, pickle.HIGHEST_PROTOCOL)

		prime_factor.persist_factors(27, [3], self.factors_file)
		self.assertEqual(prime_factor.previously_found_factors(27, self.factors_file),
						 [3])


if __name__ == "__main__":
	unittest.main()