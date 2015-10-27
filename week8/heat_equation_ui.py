from heat_equation_numpy import SolverNumpy
from heat_equation_weave import SolverWeave
from heat_equation import SolverPurePython
import argparse, sys

parser = argparse.ArgumentParser()
group  = parser.add_mutually_exclusive_group() # Pick only one solver-method
parser.add_argument("-n",  default=50,   help="The mesh points in X-direction",       type=int)
parser.add_argument("-m",  default=100,  help="The mesh points in Y-direction",       type=int)
parser.add_argument("-t0", default=0,    help="The start time of computations [sec]", type=int)
parser.add_argument("-t1", default=1000, help="The end time of computations [sec]",   type=int)
parser.add_argument("-dt", default=0.1,  help="The time step (temporal resolution)",  type=float)
#parser.add_argument("-", help="", type=)

group.add_argument("-python", help="Solve problem with pure python objects", action="store_true")
group.add_argument("-numpy",  help="Solve problem with NumPy", action="store_true")
group.add_argument("-weave",  help="Solve problem with Weave", action="store_true")

#parser.add_argument("test")
parser.add_argument("-v", "-verbose", help="Increase output verbosity", action="store_true")

args = parser.parse_args()
n  = args.n;  m  = args.m; t0 = args.t0; t1 = args.t1; dt = args.dt
#print n,m,t0,t1,dt # FOR DEBUGGING ONLY

# Set method for solver
method = 'python' if args.python else 'numpy' if args.numpy else 'weave' if args.weave else None
if not method:
    print "\nNo method specified. Choosing 'weave' for speed!"
    method = 'weave'

# Give the user options if dt is unstable
if dt > 0.25:
    print "\nTimestep too high, solution might be unstable! Choose what to do:"
    print "- Press enter to use maximum timestep (0.25) and continue"
    print "- Enter 'cont' to continue anyway, or"
    user_choice = raw_input("- Enter 'exit' to quit\n")
    if not user_choice:
        dt = 0.25
    elif user_choice == 'cont':
        pass
    elif user_choice == 'exit':
        sys.exit(1)

# Check that time parameters makes sense
if t0 >= t1 or t0 < 0:
    print "\nStart time must be larger then end time. Also, start time can't be negative"
    sys.exit(1)

print dt,method
