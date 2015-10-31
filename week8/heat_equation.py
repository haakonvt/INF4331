import matplotlib.pyplot as plt
import sys,time,copy


def SourceTermF_LIST(n,m,constant=1.0):
    """
    Initiate the nested list with a constant = 1 or as specified (if specified)
    """
    f = []
    for i in range(n):
        f.append([])
    for i in range(n):
        for j in range(m):
            f[i].append(constant)
    return f


def SolverPurePython(f, nu=1, dt=0.1, n=50, m=100, t0 = 0, t_end=1000, u0=None,
                        show_animation=False, print_progress=False):
    """
    Solver for heat equation. ONLY pure python objects used.
    Dirichlet boundary conditions: ( u_edge = 0 )
    Warning: Slow (not an understatement)
    """
    t = t0; t_end = t_end + 1E-8
    n = int(n); m = int(m)

    # Initiate the nested list with only zeros
    if u0 == None:
        u  = []
        for i in range(n):
            u.append([])
        for i in range(n):
            for j in range(m):
                u[i].append(float(0))
    else: # Or use some other distribution if given
        u = u0

    u_new = [vec[:] for vec in u] # Make a copy for the solution (to use at the next timestep)

    if show_animation:
        plt.ion()
        im = plt.imshow(zip(*u), cmap='gray')  # Initiate plotting / animation
        plt.colorbar(im)
        plt.title('2D Temp. dist. t=%f' %t)
        plot_every_n_frame = 10        # Plot every n frames
        plot_counter = 0               # Make sure to plot first frame

    # Loop over all timesteps
    while t < t_end:
        for i in range(1,n-1): # Not including first and last element
            for j in range(1,m-1):
                u_new[i][j] = u[i][j] \
                            + dt*(nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] \
                            +     nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])

        t += dt                         # Jump to next timestep
        u = [vec[:] for vec in u_new]   # Update u for next iteration (much faster than "deep copy")

        if show_animation:
            if plot_counter == plot_every_n_frame or t >= t_end: #Also plot the very last solution:
                im.set_array(zip(*u_new))     # Set new values for u in plot
                plt.title('2D Temp. dist. t=%f' %(t-dt)) # Update title with current time
                im.autoscale()          # Fix colorbar and color map to map from min-max
                plt.draw()              # Update the figure with latest solution
                plot_every_n_frame += 1 # Plot less frames the further in time we go
                plot_counter = 0        # Reset the counter
            plot_counter += 1

        if print_progress:
            percent = t/float(t_end)*100.0 if t<t_end else 100
            sys.stdout.write("\rRunning calculations... %d%% " % percent) # Print out a simple "progress bar" showing percent
            sys.stdout.flush()
    return u_new


if __name__ == '__main__':
    n = 50  # Mesh-length in x-direction
    m = 100 # Mesh-length in y-direction

    f = SourceTermF_LIST(n,m)
    dt = 0.1; t0 = 0; t_end = 200; nu = 1.0
    cpu_t0   = time.clock()
    u = SolverPurePython(f,nu,dt,n,m,t0,t_end,show_animation=False,print_progress=True)
    cpu_time = time.clock() - cpu_t0
    print "\nMax. temp.:", max(max(u)), "time taken:", cpu_time

    # Show the solution at the last timesteps (i.e. not close the plot..)
    raw_input('\nPress enter to quit...')
