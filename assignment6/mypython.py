from feedline import feedline
from getchar  import getchar
import sys
import time

def prompt():
    sys.stdout.write("Welcome to mypython!\nin [0]:")
    sys.stdout.write("")
    line = ""
    cmd_history = []  #List of all used commands
    save_line_on_first_arrow_key = True
    up_counter = 0 # Will be index of cmd_history when multplied with -1
    while True:
        arrow_key      = None
        char_to_screen = True
        char_to_line   = True
        char = getchar() # Catch user input (one character at the time)

        if char == "\x1b":
            arrow_key = sys.stdin.read(2)
        if arrow_key in ["[A", "[B"]: # Up or down
            char_to_screen = False
            char_to_line   = False
            if save_line_on_first_arrow_key:
                stored_current_line = line
                save_line_on_first_arrow_key = False
        if arrow_key == "[A": # UP is pressed
            up_counter += 1 if len(cmd_history) > up_counter else 0
            if not cmd_history:
                # Basicly do nothing, nothing to grab
                pass
            else:
                if up_counter == 1:
                    prev_cmd = cmd_history[-1*up_counter]
                    chars_to_remove = "\b"*len(line) + " "*len(line) + "\b"*len(line)
                    sys.stdout.write(chars_to_remove + prev_cmd)
                    line = prev_cmd
                else:
                    prev_cmd = cmd_history[-1*up_counter]
                    number   = len(prev_cmd)
                    chars_to_remove = "\b"*number + " "*number + "\b"*number
                    sys.stdout.write(chars_to_remove + prev_cmd)
                    line = prev_cmd
        if arrow_key == "[B": # DOWN is pressed
            if up_counter == 0:
                pass
            elif up_counter == 1:
                next_cmd = stored_current_line
                number   = len(cmd_history[-1*up_counter])
                chars_to_remove = "\b"*number + " "*number + "\b"*number
                sys.stdout.write(chars_to_remove + next_cmd)
                line = next_cmd
            else:
                next_cmd = cmd_history[-1*up_counter+1]
                number   = len(next_cmd)
                chars_to_remove = "\b"*number + " "*number + "\b"*number
                sys.stdout.write(chars_to_remove + next_cmd)
                line = next_cmd
            up_counter -= 1 if up_counter > 0 else 0


        if char == "\x04": # Ctrl + D = quit
            char_to_line   = False
            char_to_screen = False
            if line == "":
                sys.stdout.write("\n")
                sys.exit(0)
            else:
                sys.stdout.write("\nKeyboardInterupt\n")
                sys.stdout.write(feedline(""))
                line = ""

        if char == "\x7f":
                if line: # not empty
                    sys.stdout.write("\b \b")
                    line = line[:-1]
                char_to_line   = False
                char_to_screen = False

        if char_to_screen:
            sys.stdout.write(char) # ... and print that character to screen

        if char in "\r\n":
            # When enter is pressed (i.e. char is 'newline') send all
            # buffered input to feedline
            sys.stdout.write('\n' + feedline(line))
            if line != '': # Dont append empty commands
                cmd_history.append(line)
            # Reset variables:
            line = ""
            up_counter = 0
            save_line_on_first_arrow_key = True

        elif char_to_line:
            line += char # add char to line/buffer

if __name__ == '__main__':
    prompt()
