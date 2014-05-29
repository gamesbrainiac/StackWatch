from unittest import TestCase

from StackObjects import Question
from websocket import create_connection


class TestQuestion(TestCase):

    def setUp(self):
        """Creating socket data file"""
        with open('Tests/socket_data.json') as f:
            sd = f.read()
            self.sd = sd

        conn = create_connection('wss://qa.sockets.stackexchange.com')
        conn.send('1-questions-newest-python')
        self.conn = conn

    def test_json_loading(self, data=None):
        data = data or self.sd
        q = Question.from_socket_json(data)
        assert q is not None
        assert isinstance(q, Question)

    def test_dupe_questions(self):
        qs = []
        for i in range(10):
            qs.append(Question.from_socket_json(self.sd))
        assert len(Question.__questions__) == 1
        assert len(Question.__questions__) != len(qs)

    def test_init_testing(self):
        try:
            q = Question('this is not supposed to work')
        except TypeError as e:
            pass

    # def test_random_data_json_loading(self):
    #     for x in range(3):
    #         data = self.conn.recv()
    #         self.test_json_loading(data)
