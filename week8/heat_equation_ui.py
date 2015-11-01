from heat_equation       import SolverPurePython, SourceTermF_LIST
from heat_equation_numpy import SolverNumpy,      SourceTermF_ARRAY
from heat_equation_weave import SolverWeave
import matplotlib.pyplot as plt
import numpy             as np
import argparse, sys, timeit


def heat_eq_ui():
    """
    Solve heat equation with arguments (all are optional) from the commands
    line; Type of solver, constants, initial dist. from file, animation etc.
    Run with "-h" for a complete description of available commands.

    When using timeit via "-time RUNS ITER" animation and other output
    are ignored. User settings i.e. f, m, t0 etc. are used if acceptable.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-time", nargs=2, help="Turn on timeit-module. "+ \
                                                   "Run ARG1 tests with ARG2 iterations", type=int)
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
    show_animation   = args.a

    # File handling switches
    use_timeit            = False if not args.time else True
    output_last_u_to_file = False if not args.o    else True
    change_initial_u      = False if not args.i    else True
    print_progress        = True  if verbose       else False

    if use_timeit:
        timeit_repeats   = args.time[0]
        timeit_iter      = args.time[1]

    # Set method for solver
    method = SolverPurePython if args.python else SolverNumpy if args.numpy else SolverWeave if args.weave else None
    scheme_name = 'Python'    if args.python else 'Numpy'     if args.numpy else 'Weave'     if args.weave else None
    if not method:
        if verbose:
            print "\nNo method specified. Choosing 'weave' for speed!"
        method = SolverWeave
        scheme_name = 'Weave'

    # Give the user options if dt is unstable/too large
    # dt <= dx*dy / (4*nu) (and we have dx=dy=1 for any mesh size, see report)
    max_stable_dt = 1.0/(4*nu)
    if dt > max_stable_dt:
        print "\nThe chosen dt (%.2e) is  too large, solution might be unstable!" %dt
        print "Choose what to do:"
        print "- Press enter to use the max. stable dt (%.2e) and continue" %max_stable_dt
        print "- Enter 'c' or 'cont' to continue anyway, or"
        user_choice = raw_input("- Enter 'exit' (or anything else than the above options) to quit\n")
        if not user_choice:
            dt = max_stable_dt
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
        n_i = initial_u.shape[0]
        m_i = initial_u.shape[1]
        if n != n_i or m != m_i:
            print "\nMesh dimensions of initial u from file (%d,%d) does NOT match" %(n_i,m_i)
            print "user (or default) specified values: (%d,%d)\nExiting..." %(n,m)
            sys.exit(1)
    else:
        initial_u = None

    # If timeit is used and method = PurePython, give the user a warning
    if method == SolverPurePython and use_timeit:
        timeit_total_iter = timeit_repeats*timeit_iter # Total number of iterations (i.e. runs of solver)
        if timeit_total_iter >= 2 and t1-t0 >= 200:
            estimate_time_used = int((t1-t0)/1000. * 55)
            print "\nWarning: Testing the pure python implementation is really slow. "
            if verbose:
                print "Rough time estimate per iteration (and total time): %d, (%d) seconds" \
                       %(estimate_time_used, timeit_total_iter*estimate_time_used)
                raw_input('Press enter to continue..')


    # Fill the source term f (as a list or array)
    if method == SolverPurePython:
        f = SourceTermF_LIST(n,m,f_constant)
    else: # All other methods use arrays
        f = SourceTermF_ARRAY(n,m,f_constant)

    # One call to rule them all
    if use_timeit:
        if verbose:
            print "\nWhen running timeit, some user specified settings might"
            print "be ignored for consistency and reproducability"

        if method == SolverPurePython: # Sorry for long lines of code, but I get indent error otherwise...
            setup_timeit = "from heat_equation import SolverPurePython, SourceTermF_LIST; method = SolverPurePython; f = SourceTermF_LIST(%d,%d,%f)" %(n,m,f_constant)
        elif method == SolverNumpy:
            setup_timeit = "from heat_equation_numpy import SolverNumpy, SourceTermF_ARRAY; method = SolverNumpy; f = SourceTermF_ARRAY(%d,%d,%f)" %(n,m,f_constant)
        else:
            setup_timeit = "from heat_equation_weave import SolverWeave, SourceTermF_ARRAY; method = SolverWeave; f = SourceTermF_ARRAY(%d,%d,%f)" %(n,m,f_constant)
        solver_call = "u = method(f,%f,%f,%d,%d,%d,%d,None,False,False)" %(nu,dt,n,m,t0,t1)
        timeit_results = timeit.Timer(solver_call, setup=setup_timeit).repeat(timeit_repeats, timeit_iter)
        best_time = min(timeit_results)/float(timeit_iter) # All noise in data is "positive", so minimum time is most accurate
        if verbose:
            print "\nTest repeats: %d, each with %d iterations" %(timeit_repeats, timeit_iter)
            print "Settings: f=1,nu=%.1f,dt=%.1f,n=%d,m=%d,t0=%d,t1=%d" %(nu,dt,n,m,t0,t1)
            print "Minimum CPU-time of scheme '%s': %f seconds" %(scheme_name, best_time)
        else:
            print "Min. CPU-time: %f sec. (%s)" %(best_time, scheme_name)

    else:
        u = method(f,nu,dt,n,m,t0,t1,initial_u, \
               show_animation=show_animation,print_progress=verbose)

        if verbose: # Need to add some spacing for aesthetical purposes
            print ""

        # Save last u
        if output_last_u_to_file:
            if verbose:
                print "\nSaving final temperature distribution u to file"
            filename = args.o
            np.savetxt(filename, u) # Works with both nested list and array

        if save_last_fig:
            if verbose:
                print "\nSaving the final temperature plot of u to 'last_u.png'"
            plt.ion()
            im = plt.imshow(zip(*u), cmap='gray')  # Initiate plotting / animation
            plt.title('u(x,y,t=%d)' %(t1)) # Update title time
            plt.xlabel('X'); plt.ylabel('Y')
            if not show_animation: # Do not add a second colorbar if already added!
                plt.colorbar(im)
            plt.savefig('last_u.png')


if __name__ == '__main__':
    heat_eq_ui()
