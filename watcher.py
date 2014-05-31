from __future__ import print_function

import sys

from StackObjects import Question, StackTagWatcher


def questions():
    size = 0
    while True:
        new_size = len(Question.__questions__)
        if new_size > size:
            size = new_size
            yield Question.__questions__
        else:
            yield None


if __name__ == '__main__':
    default_tags = 'python django scala javascript'.split()

    tags = sys.argv[1:] or default_tags

    for t in tags:
        print(t, 'started')
        StackTagWatcher(t).start()

    for v in questions():
        if v:
            for q in reversed(sorted(v, key=lambda x: x.weight)):
                print(q)
        else:
            pass