from feedline import feedline
from getchar  import getchar
import sys
import time

def prompt():
    sys.stdout.write("Welcome to mypython!\nin [0]:")
    sys.stdout.write("")
    line = ""
    while True:
        char = getchar() # Catch user input (one character at the time)
        if char != "\x04":
            sys.stdout.write(char) # ... and print that character to screen

        if char == "\x04":
                if line == "":
                    sys.stdout.write("\n")
                    sys.exit(0)
                else:
                    sys.stdout.write("\nKeyboardInterupt\n")
                    sys.stdout.write(feedline(""))
                    line = ""

        if char in "\r\n":
            # When enter is pressed (i.e. char is 'newline') send all
            # buffered input to feedline
            sys.stdout.write('\n' + feedline(line))
            line = "" # Reset line
        elif char != "\x04":
            line += char # add char to line/buffer

if __name__ == '__main__':
    prompt()
