import unittest
from uncle_markov import build_markov_chain
from parameterized import parameterized


class TestBuildMarkovChain(unittest.TestCase):

    @parameterized.expand([
        # Empty input
        ([], 2, {'initial': {}, 'names': set()}),

        # Input with only one word and order less than or equal to the length of the word
        (['hello'], 1,
         {'initial': {'h': 1}, 'names': {'hello'}, 'h': {'e': 1}, 'e': {'l': 1}, 'l': {'l': 1, 'o': 1}, 'o': {'.': 1}}),
        (['hello'], 5, {'hello': {'ello.': 1},
         'initial': {'hello': 1}, 'names': {'hello'}}),

        # Input with only one word and order greater than the length of the word
        (['hello'], 6, {'initial': {}, 'names': {'hello'}}),

        # Input with multiple words and order less than or equal to the length of the shortest word
        (['hi', 'bye'], 1, {'b': {'y': 1}, 'e': {'.': 1}, 'h': {'i': 1}, 'i': {'.': 1}, 'initial': {'b': 1, 'h': 1},
                            'names': {'hi', 'bye'}, 'y': {'e': 1}}),
        (['hi', 'bye'], 2,
         {'by': {'ye': 1}, 'hi': {'i.': 1}, 'initial': {'by': 1, 'hi': 1}, 'names': {'hi', 'bye'}, 'ye': {'e.': 1}}),

        # Input with multiple words and order greater than the length of the shortest word
        (['hi', 'bye'], 3, {'bye': {'ye.': 1},
         'initial': {'bye': 1}, 'names': {'hi', 'bye'}}),
        (['hello', 'world'], 5,
         {'hello': {'ello.': 1}, 'initial': {'hello': 1, 'world': 1}, 'names': {'hello', 'world'},
          'world': {'orld.': 1}}),

        # Input with special characters or numbers
        (['hello', '123', 'world'], 2,
         {'12': {'23': 1}, '23': {'3.': 1}, 'el': {'ll': 1}, 'he': {'el': 1}, 'initial': {'12': 1, 'he': 1, 'wo': 1},
          'ld': {'d.': 1}, 'll': {'lo': 1}, 'lo': {'o.': 1}, 'names': {'123', 'world', 'hello'}, 'or': {'rl': 1},
          'rl': {'ld': 1}, 'wo': {'or': 1}}),
        (['hi!', 'bye?'], 1, {'!': {'.': 1}, '?': {'.': 1}, 'b': {'y': 1}, 'e': {'?': 1}, 'h': {'i': 1}, 'i': {'!': 1},
                              'initial': {'b': 1, 'h': 1}, 'names': {'hi!', 'bye?'}, 'y': {'e': 1}})
    ])
    def test_build_markov_chain(self, data, n, expected_output):
        self.assertEqual(expected_output, build_markov_chain(data, n))

    # Boundary tests
    def test_build_markov_chain_min_input(self):
        self.assertEqual({'initial': {}, 'names': {''}},
                         build_markov_chain([''], 1))

    def test_build_markov_chain_max_input(self):
        max_input = ['a' * 100] * 100
        self.assertEqual({'initial': {'a': 100}, 'names': {
                         'a' * 100}, 'a': {'.': 100, 'a': 9900}}, build_markov_chain(max_input, 1))


if __name__ == '__main__':
    unittest.main()
