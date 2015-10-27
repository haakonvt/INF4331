from heat_equation_numpy import SolverNumpy
from heat_equation_weave import SolverWeave
from heat_equation import SolverPurePython
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

parser.add_argument("-s", "-save",    help="Save plot of last solution as last_u.png", action="store_true")
parser.add_argument("-v", "-verbose", help="Increase output verbosity",                action="store_true")
parser.add_argument("-time", help="Turn on timeit-module and report CPU-time at end",  action="store_true")

group  = parser.add_mutually_exclusive_group() # Pick only one solver-method
group.add_argument("-python", help="Solve problem with pure python objects", action="store_true")
group.add_argument("-numpy",  help="Solve problem with NumPy", action="store_true")
group.add_argument("-weave",  help="Solve problem with Weave", action="store_true")

args = parser.parse_args()
n  = args.n;  m  = args.m
t0 = args.t0; t1 = args.t1
f  = args.f;  nu = args.nu
dt = args.dt

# Store user options with readable names [true or false]
verbose       = args.v
save_last_fig = args.s
use_timeit    = args.time

# File handling switches
output_last_u_to_file = False if not args.o else True
change_initial_u      = False if not args.i else True

# Set method for solver
method = 'python' if args.python else 'numpy' if args.numpy else 'weave' if args.weave else None
if not method:
    if verbose:
        print "\nNo method specified. Choosing 'weave' for speed!"
    method = 'weave'

# Give the user options if dt is unstable
if dt >= 0.25:
    print "\nTimestep (dt) too large, solution might be unstable! Choose what to do:"
    print "- Press enter to use maximum timestep (0.25) and continue"
    print "- Enter 'c' or 'cont' to continue anyway, or"
    user_choice = raw_input("- Enter 'exit' (or anything else than nothing) to quit\n")
    if not user_choice:
        dt = 0.25
    elif user_choice in ['c','cont']:
        pass
    else:
        sys.exit(1)

# Check that time parameters makes sense
if t0 >= t1 or t0 < 0:
    print "\nStart time must be larger then end time. Also, start time can't be negative"
    sys.exit(1)

print dt,method
