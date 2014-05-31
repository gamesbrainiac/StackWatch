# encoding=utf-8
"""
Object Wrapper for StackOverflow Questions and Users. Also houses module's object specific exceptions.
"""
import json

import re

from utils import CachedProperty, LockedSet
from bs4 import BeautifulSoup


class WrongDataFormatException(Exception):
    pass


class StackObject(object):
    _BASE_URL = 'http://stackoverflow.com'


class User(StackObject):
    """
    Object that represents a StackOverflow user

    :param name: Name of the user
    :type name: str|unicode

    :param uid: User ID on StackOverflow
    :type uid: int
    """

    def __init__(self, name, uid):
        self.name = name
        self._id = uid

    @CachedProperty
    def url(self):
        """
        :return: The URL for the user's profile page on StackOverflow
        :rtype: str
        """
        return "{}/users/{}".format(self.__class__._BASE_URL, self._id)

    def __repr__(self):
        return "<{}>{{{}}}".format(self.name, self._id)


class Question(StackObject):
    """
    A Question class for StackOverflow questions. Has a class variable called __questions__ that contains all
    instances of questions asked

    :type creator: str
    :param creator: The username of the person who posted the question

    :type name: str
    :param name: The name of the question

    :type id_num: int
    :param id_num: The ID of the question asked

    :param tags: A set of all the associated tags
    :type tags: set
    """
    __questions__ = LockedSet()
    _slash_remover_regex = re.compile(r'\+[nr]?')
    _action_test_regex = re.compile(r'1-questions-newest-tag-\w+')
    _weights = {
        "python": 20,
        "python-2.7": 15,
        "python-3.x": 15,
        "decorator": 15,
        "pycharm": 15,
        "webstorm": 15,
        "list": 15,
        "beautifulsoup": 12,
        "while-loop": 10,
        "phpstorm": 10,
        "multiprocessing": 10,
        "django": 5,
    }

    def __init__(self, id_num, name, tags, creator=(None, 1)):
        self.id = id_num
        self.tags = tags
        self.name = name
        self.creator = User(*creator)
        self.__class__.__questions__.add(self)

    @CachedProperty
    def weight(self):
        """
        :return: The sum of all the weights of the question's tags
        :rtype: int
        """
        wts = self.__class__._weights
        # Not very good complexity
        return sum(wts[t] for t in self.tags if t in wts)

    def __hash__(self):
        return self.id

    @CachedProperty
    def url(self):
        """
        :return: Returns the StackOverflow url of a question
        :rtype: str
        """
        return "{}/questions/{}".format(self.__class__._BASE_URL, self.id)

    @classmethod
    def from_socket_json(cls, ws_json_string):
        """
        A classmethod which creates a Question object wrapper for
        StackOverflow questions.

        :param ws_json_string: JSON string from web socket
        :type ws_json_string: str|unicode

        :return: A Question Object
        :rtype: Question

        :raise WrongDataFormatException: Websocket returned the wrong JSON string
        """
        info = json.loads(ws_json_string)
        try:
            if cls._action_test_regex.match(info['action']):
                # data contains all the information we need,
                # there are two keys, ``action`` and ``data``
                # the regex removes all the ``\\`` and ``\n`` or ``\r``
                # inside the string
                info = json.loads(cls._slash_remover_regex.sub('', info['data']))
            else:
                raise WrongDataFormatException("Wrong socket data format. Incorrect ``action`` format in JSON object.")
        except KeyError:
            raise

        id_num = int(info['id'])
        tags = set(info['tags'])

        # Getting data from info['body']
        body_soup = BeautifulSoup(info['body'])
        question_name = body_soup.find(
            attrs={'class': 'question-hyperlink'}).text
        cr_name = body_soup.find(
            attrs={'class': 'user-details'}).find('a').text
        cr_id = int(body_soup.find(
            attrs={'class': 'user-details'}).find('a')['href'].split(r'/')[2])

        # Finally creating class
        return cls(id_num=id_num, name=question_name, tags=tags, creator=(cr_name, cr_id))

    def __repr__(self):
        return "<{question_name}> - {tags}|{weight} - {creator} -> {url}".format(
            question_name=self.name,
            creator=self.creator.name,
            url=self.url,
            tags=list(self.tags),
            weight=self.weight
        )

    def __eq__(self, other):
        return self.id == other.id