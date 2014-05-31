StackWatch
==========

A simple question watcher for StackOverflow. This is still in alpha. To test:

    python -m unittest -v Tests.test_question

In order to use the program:

    python watcher.py

Before that, make sure you have all the requirements installed:

    pip install -r requirements.txt

Note, that as of now, you need to set your own weights. And this can be done by modifying the `_weights` dict inside
of `StackObjects.Question`.

The tags that are being watched is configured in `watcher.py`. To change tags in `watcher.py` simply
add or remove a tag from the list:

    ...
    tags = 'python ruby django c c++ java php scala javascript'.split()
    ...

Or you can simply pass in your own arguments:

    python watcher.py node javascript python django scala coffeescript

Plans
-----

 - Make a console UI
 - Make a web UI (probably using flask or Pyramid)
 - Add a time stamp to question class