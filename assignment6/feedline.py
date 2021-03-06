namespace = vars().copy()
namespace['line_number'] = 0
namespace['cmd_history'] = []
namespace['_all_output'] = 'in [0]'

import sys, subprocess
from StringIO import StringIO


def feedline(string_command,return_all_history=False):
    """
    Evaluates a single string argument as python code.

    Args:
        string_command (str):      Python code to be evaluated
        return_all_history (bool): Return all history if specified to True
    Returns:
        IPython-style string to be printed with sys.stdout.write()
    Raises:
        SyntaxError: Non-python characters is used as input
        NameError:   If some variable isn't already defined

    Example usage:
    >>> from feedline import feedline
    >>> feedline('x=2')
    'in [1]:'
    >>> feedline('x**2')
    'out[2]:4\nin [2]:'
    >>> print feedline('x**2')
    out[3]:4
    in [3]:
    """
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
        # Pass the command to the operating system
        string_command = string_command[1:] # Remove the exclamation mark
        output = subprocess.Popen(string_command, shell=True,
                           stdout=subprocess.PIPE).communicate()[0]
        magic  = True
    if last_char == '?':
        # Display the docstring of the object
        string_command = string_command[0:-1] # Remove question mark
        help(string_command)
        magic = True
    if magic_save:
        # Save the command history to file
        save_file = open(magic_save_filename, "w")
        for command in namespace['cmd_history']:
            save_file.write(command + "\n")
        save_file.close()
        magic = True
    if not magic: # Only evaluate if string_command is python code
        try:
            # Evaluate string as python code
            output = eval(string_command,namespace)
        except SyntaxError:
            try:
                oldio, sys.stdout = sys.stdout, StringIO() # Swap stdout with StringIO Instance
                exec(string_command, namespace) # Execute string as python code
                output = sys.stdout.getvalue() # Get stdout buffer
                sys.stdout = oldio # Reset stdout
                eval_used = False
            except Exception as err:
                sys.stdout = oldio # Reset stdout
                if return_all_history:
                    string_out = string_command +'\n' + "Error: %s" %err + "\n" + "in [%d]:" %l_n
                    namespace['_all_output'] += string_out
                    return namespace['_all_output']
                else:
                    return "Error: %s" %err + "\n" + "in [%d]:" %l_n
        except Exception as err:
            if return_all_history:
                string_out = string_command + '\n' + "Error: %s" %err + "\n" + "in [%d]:" %l_n
                namespace['_all_output'] += string_out
                return namespace['_all_output']
            else:
                return "Error: %s" %err + "\n" + "in [%d]:" %l_n

    # Mainly for webapp, where a single string containing the whole history is returned
    if return_all_history:
        if eval_used and not magic:
            string_out = string_command +'\n' + "out[%d]:" %l_n + str(output) + "\n" + "in [%d]:" %l_n
            namespace['_all_output'] += string_out
            return namespace['_all_output']
        else:
            if not output:
                string_out = string_command + '\n' + 'in [%d]:' %l_n
                namespace['_all_output'] += string_out
                return namespace['_all_output']
            else:
                string_out = string_command + '\n' + str(output) + 'in [%d]:' %l_n
                namespace['_all_output'] += string_out
                return namespace['_all_output']
    else:
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
