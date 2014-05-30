import json
from unittest import TestCase

from StackObjects import Question, WrongDataFormatException
from websocket import create_connection


class TestQuestion(TestCase):
    """
    A set of regression tests for StackObjects.Question.
    """

    def setUp(self):
        """
        - Creating socket data file
        - Creating connection for use
        - Test is carried out using new python tags only
        """
        with open('Tests/socket_data.json') as f:
            sd = f.read()
            self.sd = sd

        conn = create_connection('wss://qa.sockets.stackexchange.com')
        conn.send('1-questions-newest-python')
        self.conn = conn

    def test_json_loading(self, data=None):
        """
        Testing from_socket_json classmethod.
        """
        data = data or self.sd
        assert isinstance(data, str) or isinstance(data, unicode)
        q = Question.from_socket_json(data)
        assert q is not None
        assert isinstance(q, Question)

        assert q.name is not None
        assert int(q.id)

    def test_dupe_questions(self):
        """
        Testing to see whether multiple questions with the same ID
        is being added. Essentially, testing __hash__
        """
        qs = []
        for i in range(10):
            qs.append(Question.from_socket_json(self.sd))
        assert len(Question.__questions__) == 1
        assert len(Question.__questions__) != len(qs)

    def test_init_testing(self):
        """
        Testing __init__ function
        """
        try:
            q = Question('this is not supposed to work')
        except TypeError as e:
            pass

    def test_repr(self):
        q = Question.from_socket_json(self.sd)
        print q

    def test_url(self):
        q = Question.from_socket_json(self.sd)
        assert q.url is not None

    def test_wrong_json_data(self):
        test_dict = {
            "something": 1,
            "data": "cakes",
            "happy": "noodles",
            "action": "Nothing here"
        }

        info = json.dumps(test_dict)
        try:
            self.test_json_loading(info)
        except WrongDataFormatException as e:
            pass

    def tearDown(self):
        self.conn.close()