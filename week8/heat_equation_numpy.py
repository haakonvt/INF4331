import matplotlib.pyplot as plt
import numpy as np
import sys,time


def SourceTermF_ARRAY(Nx,Ny):
    # Initiate the array with constant f = 1
    f = np.ones((Nx,Ny))
    return f


def SolverNumpy(f, nu=1, dt=0.1, Nx=50, Ny=100, t0 = 0, t_end=1000,
                    show_animation=False, print_progress=False):
    """
    Solver for heat equation. Solved with numpy arrays (slices for speed)
    Dirichlet boundary conditions: ( u_edge = 0 )
    """
    t = t0
    #Nx = int(Nx); Ny = int(Ny)

    # Initiate the solution array for u_n
    u     = np.zeros((Nx,Ny))

    if show_animation:
        plt.ion()
        im = plt.imshow(u, cmap='gray')  # Initiate plotting / animation
        plt.colorbar(im)
        plot_every_n_frame = 10        # Plot every n frames
        plot_counter = 0               # Make sure to plot first frame

    # Loop over all timesteps
    while t < t_end:
        u[1:-1,1:-1] = u[1:-1,1:-1] \
                     + dt*(nu*u[:-2,1:-1] + nu*u[1:-1,:-2] - 4*nu*u[1:-1,1:-1] \
                     +     nu*u[1:-1,2:]  + nu*u[2:,1:-1] + f[1:-1,1:-1])
        t += dt # Jump to next timestep

        if show_animation:
            if plot_counter == plot_every_n_frame:
                im.set_array(u)     # Set new values for u in plot
                im.autoscale()          # Fix colorbar and color map to map from min-max
                plt.draw()              # Update the figure with latest solution
                plot_every_n_frame += 1 # Plot less frames the further in time we go
                plot_counter = 0        # Reset the counter
            plot_counter += 1

        if print_progress:
            percent = t/float(t_end)*100.0 if t<t_end else 100
            sys.stdout.write("\rRunning calculations... %d%% " % percent) # Print out a simple "progress bar" showing percent
            sys.stdout.flush()
    return u


if __name__ == '__main__':
    Nx = 50  # Mesh-length in x-direction
    Ny = 100 # Mesh-length in y-direction

    f = SourceTermF_ARRAY(Nx,Ny)
    dt = 0.1; t0 = 0; t_end = 200; nu = 1.0
    cpu_t0   = time.clock()
    u = SolverNumpy(f,nu,dt,Nx,Ny,t0,t_end,show_animation=False)
    cpu_time = time.clock() - cpu_t0

    print "\nMax. temp.:", u.max(), "time taken:", cpu_time
    # Show the solution at the last timesteps (i.e. not close the plot..)
    raw_input('\nPress enter to quit...')
