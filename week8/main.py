import matplotlib.pyplot as plt
import numpy as np
import sys


def SourceTermF_LIST(Nx,Ny):
    # Initiate the nested list with only constant = 1
    f = []
    for i in range(Nx):
        f.append([])
    for i in range(Nx):
        for j in range(Ny):
            f[i].append(1)
    return f


def SolverPurePython(f, nu=1, dt=0.1, Nx=50, Ny=100, t0 = 0, t_end=1000,show_animation=False):
    """
    Solver for heat equation. ONLY pure python objects used.
    Dirichlet boundary conditions: ( u_edge = 0 )
    """
    u  = []; t = t0
    Nx = int(Nx); Ny = int(Ny)

    # Initiate the nested list with only zeros
    for i in range(Nx):
        u.append([])
    for i in range(Nx):
        for j in range(Ny):
            u[i].append(0)

    u_new = u[:] # Make a copy for the solution at the next timestep

    if show_animation:
        plt.ion()
        im = plt.imshow(u, cmap='gray')  # Initiate plotting / animation
        plt.colorbar(im)
        plot_every_n_frame = 10        # Plot every n frames
        plot_counter = 0               # Make sure to plot first frame

    # Loop over all timesteps
    while t < t_end:
        u = u_new
        for i in range(1,Nx-1): # Not including first and last element
            for j in range(1,Ny-1):
                u_new[i][j] = u[i][j] \
                            + dt*(nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] \
                            +     nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        t += dt # Jump to next timestep

        if show_animation:
            if plot_counter == plot_every_n_frame:
                im.set_array(u_new)     # Set new values for u in plot
                im.autoscale()          # Fix colorbar and color map to map from min-max
                plt.draw()              # Update the figure with latest solution
                plot_every_n_frame += 1 # Plot less frames the further in time we go
                plot_counter = 0        # Reset the counter
            plot_counter += 1

        percent = t/float(t_end)*100.0 if t<t_end else 100
        sys.stdout.write("\rRunning calculations... %d%% " % percent) # Print out a simple "progress bar" showing percent
        sys.stdout.flush()


    return u_new


if __name__ == '__main__':
    Nx = 50  # Mesh-length in x-direction
    Ny = 100 # Mesh-length in y-direction

    f = SourceTermF_LIST(Nx,Ny)
    dt = 0.1; t0 = 0; t_end = 1000; nu = 1.0
    u = SolverPurePython(f,nu,dt,Nx,Ny,t0,t_end)#,show_animation=True)

    print "\nMax. temp.:", max(max(u))
    # Show the solution at the last timesteps
    raw_input('\nPress enter to quit...')
