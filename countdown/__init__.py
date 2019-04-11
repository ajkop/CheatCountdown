import os
import time
from itertools import permutations

from countdown.api_wrapper import Wrapper


class Letters:
    def __init__(self, word_file=None):
        self.word_file = os.path.join(os.getcwd(), "countdown", "words/words_alpha.txt")
        self.api = Wrapper()
        self.word_list = self.init_words(word_file)

    def init_words(self, word_file=None):
        word_input = word_file or self.word_file
        with open(word_input) as input_file:
            word_list = set([word.strip() for word in input_file.readlines()])
        return word_list

    def word_find(self, letter_list, with_definition=False, limit=5):
        """
        Given a list of letters find all real english words that can be found and return a dict of the largest $limit
        amount. Will also return the dictionary definition of the word if it can find it and the argument is enabled.

        :param letter_list: List of letters to try to make words out of.
        :type letter_list: `list`
        :param with_definition: Turn on returning definitions with the word list.
        :type with_definition: `bool`
        :param limit: The limit of words to return, defaults to 10
        :type limit: `int`
        :return: A dictionary of matched words ordered by their length.
        :rtype: `dict`
        """

        start_time = time.time()

        attempt_list = []
        outcomes = []

        # Iterate over each letter and put them in a list.
        for letter in letter_list:
            attempt_list.append(letter)
            # For every amount of combinations of letters within range check permutations
            for i in range(1, len(attempt_list)):
                for item in permutations(attempt_list, i):
                    outcomes.append(item)

        # Join the outcomes together into a new list.
        choices = [''.join(out) for out in set(outcomes)]

        # Iterate over permutations and check if any of them are in our list of words. If so append to matches.
        matches = [choice for choice in choices if choice in self.word_list]

        # Strip duplicates from matches, then Grab the last $limit number of matches after sorting for length
        limited_matches = sorted(set(list(matches)), key=len, reverse=True)[:limit]

        # If the method is invoked with the with_definition argument do the following dict comprehension.
        if with_definition:
            # This comprehension just creates a dictionary of the matched words with word as the key and the len of the
            # word + definition as the value if a definition is found.
            result = {match: [{'Length': len(match)}, {'Definition': self.api.get_def(match) or 'No definition found'}]
                      for match in limited_matches}
        else:
            result = {match: [{'Length': len(match)}] for match in limited_matches}

        result.update({'Runtime': time.time() - start_time})

        return result

    def anagram(self, word, with_definition=False):
        """
        Given a word or combination word with no spaces, check for anagrams that match.

        :param word: Word to check anagrams for.
        :type word: `str`
        :param with_definition: Optional argument to also return the definition of the word.
        :type with_definition: `bool`
        :return: `list' or `dict`
        """

        letter_list = [letter for letter in word]
        outcomes = permutations(letter_list)
        choices = [''.join(out) for out in outcomes]
        possible_matches = [stored_word for stored_word in self.word_list if len(stored_word) == len(word)]
        matches = [choice for choice in set(choices) if choice in possible_matches]

        if with_definition:
            return {match: self.api.get_def(match) for match in matches}
        else:
            return matches
