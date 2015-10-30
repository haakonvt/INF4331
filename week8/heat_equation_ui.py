from heat_equation       import SolverPurePython, SourceTermF_LIST
from heat_equation_numpy import SolverNumpy,      SourceTermF_ARRAY
from heat_equation_weave import SolverWeave
import matplotlib.pyplot as plt
import numpy             as np
import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("-n",  default=50,   help="The mesh points in X-direction",       type=int)
parser.add_argument("-m",  default=100,  help="The mesh points in Y-direction",       type=int)
parser.add_argument("-t0", default=0,    help="The start time of computations [sec]", type=int)
parser.add_argument("-t1", default=1000, help="The end time of computations [sec]",   type=int)
parser.add_argument("-dt", default=0.1,  help="The time step (temporal resolution)",  type=float)
parser.add_argument("-nu", default=1.0,  help="The thermal diffusivity",              type=float)
parser.add_argument("-f",  default=1.0,  help="The constant heat source term",        type=float)

parser.add_argument("-o", "-output", help="Filename (save to disk) of final solution u", type=str)
parser.add_argument("-i", "-input",  help="Filename (read from disk) of initial u"     , type=str)

parser.add_argument("-s", "-save",    help='Save plot of last solution: "last_u.png"', action="store_true")
parser.add_argument("-v", "-verbose", help="Increase output verbosity",                action="store_true")
parser.add_argument("-a", "-anim",    help="Animate solution while computation runs",  action="store_true")
parser.add_argument("-time", help="Turn on timeit-module and report used CPU-time",    action="store_true")

group  = parser.add_mutually_exclusive_group() # Pick only one solver-method
group.add_argument("-python", help="Solve problem with pure python objects", action="store_true")
group.add_argument("-numpy",  help="Solve problem with NumPy", action="store_true")
group.add_argument("-weave",  help="Solve problem with Weave", action="store_true")

# Store user options with readable names
args = parser.parse_args()
dt = args.dt
n  = args.n;  m  = args.m
t0 = args.t0; t1 = args.t1
nu = args.nu
f_constant       = args.f
verbose          = args.v
save_last_fig    = args.s
use_timeit       = args.time
show_animation   = args.a

# File handling switches
output_last_u_to_file = False if not args.o else True
change_initial_u      = False if not args.i else True
print_progress        = True  if verbose    else False

# Set method for solver
method = SolverPurePython if args.python else SolverNumpy if args.numpy else SolverWeave if args.weave else None
if not method:
    if verbose:
        print "\nNo method specified. Choosing 'weave' for speed!"
    method = SolverWeave

# Give the user options if dt is unstable/too large
if dt >= 1.0/(4*nu): # dt <= dx*dy / (4*nu) (and we have dx=dy=1 for any mesh size, see report)
    print "\nTimestep (dt) too large, solution might be unstable! Choose what to do:"
    print "- Press enter to use maximum timestep and continue"
    print "- Enter 'c' or 'cont' to continue anyway, or"
    user_choice = raw_input("- Enter 'exit' (or anything else than the above options) to quit\n")
    if not user_choice:
        dt = 1.0/(4*nu)
    elif user_choice in ['c','cont']:
        pass
    else:
        sys.exit(1)

# Check that time parameters makes sense
if t0 >= t1 or t0 < 0:
    print "\nStart time must be larger then end time. Also, start time can't be negative"
    sys.exit(1)

# Load initial temp. dist. from file if specified.
# Using a human readable text format (little slower than np.save or pickle)
if change_initial_u:
    if verbose:
        print "\nReading initial temperature distribution u0 from file"
    filename  = args.i
    try:
        initial_u = np.loadtxt(filename)
    except:
        print "File does not exit or is not in txt-format. Exiting..."; sys.exit(1)
    if method == SolverPurePython: # Must convert to nested list
        initial_u = np.tolist(initial_u)
else:
    initial_u = None


"""
Main
"""
# Fill the source term f (as a list or array)
if method == SolverPurePython:
    f = SourceTermF_LIST(n,m,f_constant)
else: # All other methods use arrays
    f = SourceTermF_ARRAY(n,m,f_constant)

# One call to rule them all
u = method(f,nu,dt,n,m,t0,t1,initial_u,show_animation=show_animation,print_progress=verbose)

if verbose: # Need to add some spacing for aesthetical purposes
    print ""

# Save last u
if output_last_u_to_file:
    if verbose:
        print "\nSaving final temperature distribution u to file"
    filename = args.o
    np.savetxt(filename, u)

if save_last_fig:
    if verbose:
        print "\nSaving the final temperature plot of u to 'last_u.png'"
    plt.ion()
    im = plt.imshow(zip(*u), cmap='gray')  # Initiate plotting / animation
    if not show_animation: # Do not add a second colorbar if already added!
        plt.colorbar(im)
    plt.savefig('last_u.png')
