import matplotlib.pyplot as plt
import numpy as np
import sys,time


def SourceTermF_ARRAY(n,m,constant=1):
    """
    Initiate the array (source term f(x,y)) with constant:
    f = 1 or f = constant if specified by user.
    """
    f = constant*np.ones((n,m))
    return f


def SolverNumpy(f, nu=1, dt=0.1, n=50, m=100, t0 = 0, t_end=1000, u0=None,
                    show_animation=False, print_progress=False):
    """
    Solver for heat equation. Solved with numpy arrays (slices for speed)
    Dirichlet boundary conditions: ( u_edge = 0 )
    """

    t = t0; t_end = t_end + 1E-8
    #n = int(n); m = int(m)

    # Initiate the solution array for u_n
    u = np.zeros((n,m)) if u0 == None else u0

    if show_animation:
        plt.ion()
        im = plt.imshow(u.transpose(), cmap='gray')  # Initiate plotting / animation
        plt.colorbar(im)
        plt.title('u(x,y,t=%.1f)' %(t))  # Update title time
        plt.xlabel('X'); plt.ylabel('Y') # Add axis labels
        plot_every_n_frame = 10        # Plot every n frames
        plot_counter = 0               # Make sure to plot first frame

    # Loop over all timesteps
    while t < t_end:
        u[1:-1,1:-1] = u[1:-1,1:-1] \
                     + dt*nu*(u[:-2,1:-1] + u[1:-1,:-2] - 4*u[1:-1,1:-1] \
                     +        u[1:-1,2:]  + u[2:,1:-1]) +nu*f[1:-1,1:-1]*dt
        t += dt # Jump to next timestep

        if show_animation:
            if plot_counter == plot_every_n_frame or t >= t_end: #Also plot the very last solution
                im.set_array(u.transpose())         # Set new values for u in plot
                plt.title('u(x,y,t=%.1f)' %(t-dt))  # Update title time
                im.autoscale()                      # Fix colorbar and color map to map from min-max
                plt.draw()                          # Update the figure with latest solution
                plot_every_n_frame += 1             # Plot less frames the further in time we go
                plot_counter = 0                    # Reset the counter
            plot_counter += 1

        if print_progress:
            percent = t/float(t_end)*100.0 if t<t_end else 100
            sys.stdout.write("\rRunning calculations... %d%% " % percent) # Print out a simple "progress bar" showing percent
            sys.stdout.flush()
    return u


if __name__ == '__main__':
    n = 50  # Mesh-length in x-direction
    m = 100 # Mesh-length in y-direction

    f = SourceTermF_ARRAY(n,m)
    dt = 0.1; t0 = 0; t_end = 1000; nu = 1.0; show_animation = True
    cpu_t0   = time.clock()
    u = SolverNumpy(f,nu,dt,n,m,t0,t_end,show_animation=show_animation)
    cpu_time = time.clock() - cpu_t0

    print "\nMax. temp.:", u.max(), "time taken:", cpu_time
    # Show the solution at the last timesteps (i.e. not close the plot..)
    raw_input('\nPress enter to quit...')
