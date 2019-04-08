import requests

from exceptions import APIError, APIAuthenticationError
import config


class Wrapper:

    def __init__(self):
        self.api_url = config.api_url
        self.api_key = config.api_key

    def word_lookup(self, word):
        """
        Runs the oxford dictionary API to lookup the word.

        :param word: The word to lookup.
        :type word: `str`
        :return: dict of all the attributes oxford dictionary returns for the word. Or False
        :rtype: `dict`
        """

        url_call = f'{self.api_url}/{word}?key={self.api_key}'
        r = requests.get(url_call)
        if r.status_code == 200:
            result = r.json()[0]
            if not isinstance(result, dict):
                return False
            else:
                return r.json()
        elif r.status_code == 404:
            return False
        elif r.status_code == 500:
            raise APIError
        elif r.status_code == 403:
            raise APIAuthenticationError('Authentication Failed')
        else:
            return

    def get_def(self, word):
        """
        Get a words definition by connecting to the oxford dictionaries API. Limit 60 per hour.

        :param word: The word to lookup.
        :type word: `str`
        :return: A string containing the definition of the word, or False
        :rtype: `str`
        """

        lookup_result = self.word_lookup(word)
        if lookup_result:
            try:
                return lookup_result[0]['shortdef']
            except KeyError:
                return False
        else:
            return False
