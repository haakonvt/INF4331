namespace = vars().copy()
namespace['line_number'] = 0
namespace['cmd_history'] = []

import sys, subprocess, inspect
from StringIO import StringIO

def feedline(string_command):
    if not isinstance(string_command, basestring):
        "The input argument must be a string! Exiting!"; sys.exit(1)
    output = None; eval_used = True
    if string_command != '' or namespace['line_number'] == 0:
        namespace['line_number'] += 1
    l_n = namespace['line_number']

    # Append all commands
    if string_command:
        namespace['cmd_history'].append(string_command)

    # Catch 'magic commands'
    magic = False; magic_save = False
    if len(string_command) > 0:
        char0     = string_command[0]
        last_char = string_command[-1]
    else:
        char0     = None
        last_char = None
    if len(string_command) > 4:
        if string_command[0:5] == "%save":
            magic_save = True
            if len(string_command) < 7:
                sys.stdout.write('\nNo filename given, saving as "cmd_history.txt"')
                magic_save_filename = "cmd_history.txt"
            else:
                magic_save_filename = string_command[6:]
                sys.stdout.write('\nSaving command history as "%s"' %magic_save_filename)

    if char0 == '!':
        string_command = string_command[1:] # Remove the exclamation mark
        output = subprocess.Popen(string_command, shell=True,
                           stdout=subprocess.PIPE).communicate()[0]
        magic  = True
    if last_char == '?':
        string_command = string_command[0:-1] # Remove question mark
        help(string_command)
        magic = True
    if magic_save:
        save_file = open(magic_save_filename, "w")
        for command in namespace['cmd_history']:
            save_file.write(command + "\n")
        save_file.close()
        magic = True
    if not magic:
        try:
            output = eval(string_command,namespace)
        except SyntaxError:
            try:
                oldio, sys.stdout = sys.stdout, StringIO() # Swap stdout with StringIO Instance
                exec(string_command, namespace)
                output = sys.stdout.getvalue() # Get stdout buffer
                sys.stdout = oldio # Reset stdout
                eval_used = False
            except Exception as err:
                sys.stdout = oldio # Reset stdout
                return "Error: %s" %err + "\n" + "in [%d]:" %l_n
        except Exception as err:
            return "Error: %s" %err + "\n" + "in [%d]:" %l_n

    if eval_used and not magic:
        return "out[%d]:" %l_n + str(output) + "\n" + "in [%d]:" %l_n
    else:
        if not output:
            return 'in [%d]:' %l_n
        else:
            return str(output) + 'in [%d]:' %l_n


if __name__ == '__main__':
    print feedline("print 'hello world'")
    print feedline("")
    print feedline("x=1;x+=1")
    print feedline("x*2-2")
    print repr(feedline("print x"))
    print feedline("from math import sin")
    print feedline("def f(x): return sin(x**2)")
    print feedline("f(x)")
