import json
from itertools import permutations
import requests
import secret as oxc


class WordScramble:
    def __init__(self):
        org_dict_file = oxc.dictionary_file
        with open(org_dict_file, 'r') as dict_file:
            self.word_dict = json.loads(dict_file.read())
        self.word_dict = {key.lower().strip(): value for key, value in self.word_dict.items()}
        self.word_list = set(list([word for word in set(list(self.word_dict.keys())) if '_' not in word
                                   and ' ' not in word]))

        self.api_url = oxc.api_url
        self.api_id = oxc.api_id
        self.api_key = oxc.api_key

    def word_lookup(self, word, language='en'):
        """
        Runs the oxford dictionary API to lookup the word.

        :param word: The word to lookup.
        :type word: `str`
        :param language: The language the word is in. Defaults to English ('en')
        :type language: `str`
        :return: dict of all the attributes oxford dictionary returns for the word. Or False
        :rtype: `dict`
        """
        url_call = self.api_url + f'{language}/' + word.lower()
        headers = {'app_id': self.api_id, 'app_key': self.api_key}
        r = requests.get(url_call, headers=headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 400:
            return False
        elif r.status_code == 500:
            return False
        else:
            return

    def get_def(self, word, language='en'):
        """
        Get a words definition by connecting to the oxford dictionaries API. Limit 60 per hour.

        :param word: The word to lookup.
        :type word: `str`
        :param language: The language the word is in. Defaults to English ('en')
        :type language: `str`
        :return: A string containing the definition of the word, or False
        :rtype: `str`
        """

        lookup_result = self.word_lookup(word, language=language)
        if lookup_result:
            try:
                lookup_key_map = ['results', 'lexicalEntries', 'entries', 'senses', 'definitions']
                for key in lookup_key_map:
                    lookup_result = lookup_result[key][0]
                    continue
                return lookup_result
            except KeyError:
                return False
        else:
            return False

    def word_find(self, letter_list, with_definition=False, limit=10):
        """
        Given a list of letters find all real english words that can be found and return a dict of the largest $limit
        amount. Will also return the dictionary definition of the word if it can find it and the argument is enabled.

        :param letter_list: List of letters to try to make words out of.
        :type letter_list: `str`
        :param with_definition: Turn on returning definitions with the word list.
        :type with_definition: `bool`
        :param limit: The limit of words to return, defaults to 10
        :type limit: `int`
        :return: A dictionary of matched words ordered by their length.
        :rtype: `dict`
        """

        attempt_list = []
        outcomes = []
        matches = []

        # Iterate over each letter and put them in a list.
        for letter in letter_list:
            attempt_list.append(letter)
            # For every amount of combinations of letters within range check permutations
            for i in range(1, len(attempt_list)):
                for item in permutations(attempt_list, i):
                    outcomes.append(item)

        # Join the outcomes together into a new list.
        choices = [''.join(out) for out in outcomes]

        # Iterate over permutations and check if any of them are in our list of words. If so append to matches.
        for choice in choices:
            if str(choice) in self.word_list:
                matches.append(choice)

        # Strip duplicates from matches, then Grab the last $limit number of matches after sorting for length
        limited_matches = sorted(set(list(matches)), key=len, reverse=True)[:limit]

        # If the method is invoked with the with_definition argument do the following dict comprehension.
        if with_definition:
            # This comprehension just creates a dictionary of the matched words with word as the key and the len of the
            # word + definition as the value if a definition is found.
            return {match: [len(match), self.get_def(match) or 'No definition found'] for match in limited_matches}
        else:
            return {match: len(match) for match in limited_matches}

    def anagram(self, word, with_definition=False):
        """
        Given a word or combination word with no spaces, check for anagrams that match.

        :param word: Word to check anagrams for.
        :type word: `str`
        :param with_definition: Optional argument to also return the definition of the word.
        :type with_definition: `bool`
        :return: `list' or `dict`
        """

        matches = []
        letter_list = [letter for letter in word]
        outcomes = permutations(letter_list)
        choices = [''.join(out) for out in outcomes]
        new_word_list = set([dict_word for dict_word in self.word_list if len(dict_word) == len(word)])
        for choice in choices:
            if choice in new_word_list:
                matches.append(choice)

        # Sanitize match list.
        if with_definition:
            return {match: self.get_def(match) for match in matches}
        else:
            return matches
