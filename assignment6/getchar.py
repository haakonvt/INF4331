#!/usr/bin/env python
# encoding: utf-8

"""Small script for controlling charactor input in more detail.

To explore what key results in what output, use it interactively.
For example:

    $ ./getchar.py
    prompt:å
    repr:"\xc3\xa5"

Can also be evoced through python import.
For example, for the same special character:

    >>> import getchar
    >>> getchar.getchar()
    <<< '\xc3'
    >>>

Note that the characters that spans multiple bytes, only first character is
returned.  The rest has to be retrieve the manually. For example for 'å':

    >>> import sys
    >>> print sys.stdout.read(1)
    '\xa5'
"""


import sys

# windows implementation
try:

    import msvcrt

    def getchar():
        return msvcrt.getch()

# unix/mac implementation
except:

    import tty, termios

    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if __name__ == "__main__":

    sys.stdout.write("prompt:")

    line = ""
    while True:

        char = getchar()

        # print character to screen
        sys.stdout.write(char)

        # stop cycle
        if char in "\r\n":

            # write repr of character for testing purposes
            if not line:
                sys.stdout.write("repr newline:" + repr(char) + "\n")
            else:
                sys.stdout.write("\nrepr:" + repr(line) + "\n")

            sys.exit(0)

        # add char to line
        line += char
