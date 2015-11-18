namespace = vars().copy()
namespace['line_number'] = 0

import sys
from StringIO import StringIO

def feedline(string_command):
    if not isinstance(string_command, basestring):
        "The input argument must be a string! Exiting!"; sys.exit(1)
    output = None; eval_used = True
    try:
        output = eval(string_command,namespace)
    except:
        oldio, sys.stdout = sys.stdout, StringIO() # Swap stdout with StringIO Instance
        exec(string_command, namespace)
        output = sys.stdout.getvalue() # Get stdout buffer
        sys.stdout = oldio # Reset stdout
        eval_used = False

    #print "###%s###" %(output[:-1]) # Remove newline character
    if string_command != '' or namespace['line_number'] == 0:
        namespace['line_number'] += 1
    l_n = namespace['line_number']
    if eval_used:
        return "out[%d]:" %l_n + str(output) + "\n" + "in [%d]:" %l_n
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
