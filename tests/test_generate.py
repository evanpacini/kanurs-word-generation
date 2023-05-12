import unittest
from uncle_markov import generate
from parameterized import parameterized


class TestGenerate(unittest.TestCase):
    @parameterized.expand([
        # Test case 1: Test that the function returns a random item generated from the given Markov chain,
        # and that the returned item is not in the names set.
        ({"initial": {"h": 1}, "names": {"hello"}}, "h.", True),
        ({"initial": {"h": 1}, "names": {"hello"}}, "h!", False),
        # Test case 2: Test that the function returns an empty string when an empty Markov chain is provided.
        ({}, "", False),
        # Test case 3: Test that it does not enter an infinite loop when all possible items are in the names set.
        ({"initial": {"h": 1}, "names": {"hello"}}, "", True),
        # Test case 4: Test that the generated string does not contain any items from the names set,
        # and that the string starts with a valid initial item and ends with ".".
        ({"initial": {"h": 1}, "names": {"hello"}}, "h.", True),
    ])
    def test_generate(self, chain, expected_output, not_in_names_set):
        result = generate(chain)
        self.assertEqual(not_in_names_set, result not in chain["names"])
        self.assertEqual(expected_output, result)


if __name__ == "__main__":
    unittest.main()
