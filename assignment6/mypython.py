from feedline import feedline
from getchar  import getchar
import sys

def prompt():
    sys.stdout.write("Welcome to mypython!\nin [0]:")
    sys.stdout.write("")
    line = ""
    while True:
        char = getchar() # Catch user input (one character at the time)
        sys.stdout.write(char) # ... and print that character to screen

        if char in "\r\n":
            # When enter is pressed (i.e. char is 'newline') send all
            # buffered input to feedline
            sys.stdout.write('\n' + feedline(line))
            line = "" # Reset line
        else:
            line += char # add char to line/buffer

if __name__ == '__main__':
    prompt()
