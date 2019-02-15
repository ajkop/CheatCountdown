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
        lookup_result = self.word_lookup(word, language=language)
        if lookup_result:
            try:
                lookup_key_map = ['results', 'lexicalEntries', 'entries', 'senses', 'definitions']
                for key in lookup_key_map:
                    lookup_result = lookup_result[key][0]
                return lookup_result
            except KeyError:
                return False
        else:
            return False

    def word_find(self, letter_list, with_definition=False, limit=10):
        attempt_list = []
        outcomes = []
        matches = []

        for letter in letter_list:
            attempt_list.append(letter)
            for i in range(1, len(attempt_list)):
                for item in permutations(attempt_list, i):
                    outcomes.append(item)

        choices = [''.join(out) for out in outcomes]

        for choice in choices:
            if str(choice) in self.word_list:
                matches.append(choice)

        # Strip duplicates from matches.
        matches = set(list(matches))

        if with_definition:
            return {match: [len(match), self.get_def(match)] for match in sorted(matches, key=len,
                                                                                 reverse=True)[:limit]}
        else:
            return {match: len(match) for match in sorted(matches, key=len, reverse=True)[:limit]}

    def anagram(self, word, with_definition=False):
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
