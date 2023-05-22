import random
import unittest

from parameterized import parameterized

import uncle_markov


class TestSelectRandomItem(unittest.TestCase):

    @parameterized.expand([
        ({
            "item1": 1
        }, "item1"),
        ({
            "item1": 0,
            "item2": 1
        }, "item2"),
        ({}, None),
        ({
            "item1": 0,
            "item2": 0
        }, None),
        ({
            "item1": "a",
            "item2": "b"
        }, TypeError),
        ({
            "item1": 1,
            "item2": 1,
            "item3": 2
        }, "item3"),
        ({
            "item1": 1.1,
            "item2": 2.2
        }, "item2"),
    ])
    def test_select_random_item(self, items, expected):
        random.seed(42)  # Ensure consistent results for certain test cases.
        if expected is None:
            self.assertIsNone(uncle_markov.select_random_item(items))
        elif isinstance(expected, type) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                uncle_markov.select_random_item(items)
        else:
            self.assertIn(expected, uncle_markov.select_random_item(items))
