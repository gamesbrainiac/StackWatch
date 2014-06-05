# encoding=utf-8
import sys
import time
import os

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
    default_tags = 'python regex nodejs javascript php java c scala csharp algorithm while-loop list dict'.split()

    tags = sys.argv[1:] or default_tags

    for t in tags:
        print(t, 'started')
        StackTagWatcher(t).start()

    for v in questions():
        if v:
            os.system('clear')
            for q in reversed(sorted(v, key=lambda x: x.weight)):
                if q.weight > 0:
                    print '\a'
                print(q)
        else:
            time.sleep(0.5)