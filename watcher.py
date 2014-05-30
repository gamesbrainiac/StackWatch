from __future__ import print_function

import logging
from threading import Thread

from websocket import create_connection

from StackObjects import Question, WrongDataFormatException


def questions():
    size = 0
    while True:
        new_size = len(Question.__questions__)
        if new_size > size:
            size = new_size
            yield Question.__questions__
        else:
            yield None


class StackTagWatcher(Thread):

    def __init__(self, tag, *args, **kwargs):
        super(StackTagWatcher, self).__init__()
        self._socket_message = '1-questions-newest-tag-{}'
        self.tag = tag
        self.daemon = True

    def run(self):
        conn = create_connection('wss://qa.sockets.stackexchange.com')
        conn.send(self._socket_message.format(self.tag))
        while True:
            logging.log(logging.INFO, "{} started".format(self.tag))
            data = conn.recv()
            try:
                Question.from_socket_json(data)
            except WrongDataFormatException as e:
                logging.log(logging.ERROR, e)


if __name__ == '__main__':
    tags = 'python ruby django c c++ java php scala javascript'.split()

    for t in tags:
        print(t, 'started')
        StackTagWatcher(t).start()

    for v in questions():
        if v:
            print('\n\a')
            for q in v:
                print(q)
        else:
            pass