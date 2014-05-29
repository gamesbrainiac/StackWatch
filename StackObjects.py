# encoding=utf-8
import json

import re

from utils import CachedProperty
from bs4 import BeautifulSoup


class StackObject(object):

    __base_url = 'http://stackoverflow.com'


class User(StackObject):
    """
    Object that represents a stackoverflow user
    """
    def __init__(self, name, uid):
        self.name = name
        self._id = uid

    @CachedProperty
    def url(self):
        return "{}/users/{}".format(self.__class__.__base_url, self._id)

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
    __questions__ = set()
    _slash_remover_regex = re.compile(r'\+[nr]?')
    _weights = {
        "python": 15,
        "python-2.7": 15,
        "python-3.x": 15,
        "decorator": 15,
        "pycharm": 15,
        "webstorm": 15,
        "list": 15,
        "beautifulsoup": 12,
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
        wts = self.__class__._weights
        return sum(wts[t] for t in self.tags)

    @CachedProperty
    def url(self):
        return "{}/{}".format(self.__class__.__base_url, self.id)

    @classmethod
    def from_socket_json(cls, ws_json_string):
        # Turning retrieved information into dictionary
        info = json.loads(
            json.loads(
                # data contains all the information we need,
                # there are two keys, ``action`` and ``data``
                # the regex removes all the ``\\`` and ``\n`` or ``\r``
                # inside the string
                cls._slash_remover_regex.sub('', ws_json_string))['data']
        )

        id_num = int(info['id'])
        tags = set(info['tags'])

        # Getting data from info['body']
        body_soup = BeautifulSoup(info['body'])
        question_name = body_soup.find(
            attrs={'class': 'question-summary'}).text
        cr_name = body_soup.find(
            attrs={'class': 'user-details'}).find('a').text
        cr_id = int(body_soup.find(
            attrs={'class': 'user-details'}).find('a')['href'].split(r'/')[2])

        # Finally creating class
        return cls(id_num=id_num, name=question_name, tags=tags, creator=(cr_name, cr_id))

    def __eq__(self, other):
        return self.id == other.id