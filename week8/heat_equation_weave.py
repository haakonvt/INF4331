import matplotlib.pyplot as plt
from scipy import weave
import numpy as np
import sys,time

def SourceTermF_ARRAY(n,m,constant=1):
    # Initiate the array with constant f = 1
    f = constant*np.ones((n,m))
    return f


def SolverWeave(f, nu=1, dt=0.1, n=50, m=100, t0 = 0, t_end=1000, u0=None,
                    show_animation=False, print_progress=False):
    """
    Solver for heat equation. Solved in C using weave.
    Dirichlet boundary conditions: ( u_edge = 0 )
    """
    t = t0; t_end = t_end + 1E-8
    no_anim_print_prog = False

    # Initiate the solution array for u and u_new (un)
    u  = np.zeros((n,m)) if u0 == None else u0
    un = np.zeros((n,m)) if u0 == None else u0.copy()

    if show_animation: # Keep time loop in python code for easy plotting
        plt.ion()
        im = plt.imshow(u.transpose(), cmap='gray') # Initiate plotting / animation
        plt.colorbar(im)                # Add a colorbar
        plt.title('2D Temp. dist. t=%f' %t)
        plot_every_n_frame = 10         # Plot every n frames
        plot_counter = 0                # Make sure to plot first frame
        code = """
        int i,j;
        for (i=1; i<Nu[0]-1; i++) {
           for (j=1; j<Nu[1]-1; j++) {
               UN2(i,j) = U2(i,j) \
                        + dt*(nu*U2(i-1,j) + nu*U2(i,j-1) - 4*nu*U2(i,j) \
                        + nu*U2(i,j+1) + nu*U2(i+1,j) + F2(i,j));
           }
        }
        for (i=1; i<Nu[0]-1; i++) {
           for (j=1; j<Nu[1]-1; j++) {
               U2(i,j) = UN2(i,j);
           }
        }
        """
    elif print_progress: # Print out progress but no plot
        no_anim_print_prog = True
        code = """
        int i,j;
        for (i=1; i<Nu[0]-1; i++) {
           for (j=1; j<Nu[1]-1; j++) {
               UN2(i,j) = U2(i,j) \
                        + dt*(nu*U2(i-1,j) + nu*U2(i,j-1) - 4*nu*U2(i,j) \
                        + nu*U2(i,j+1) + nu*U2(i+1,j) + F2(i,j));
           }
        }
        for (i=1; i<Nu[0]-1; i++) {
           for (j=1; j<Nu[1]-1; j++) {
               U2(i,j) = UN2(i,j);
           }
        }
        """

    else:       # Keep time loop in C-code for improved speed
        code = """
        int t,i,j;
        for (t=0; t*dt<t_end+dt; t++){
            for (i=1; i<Nu[0]-1; i++) {
               for (j=1; j<Nu[1]-1; j++) {
                   UN2(i,j) = U2(i,j) \
                            + dt*(nu*U2(i-1,j) + nu*U2(i,j-1) - 4*nu*U2(i,j) \
                            + nu*U2(i,j+1) + nu*U2(i+1,j) + F2(i,j));
               }
            }
            for (i=1; i<Nu[0]-1; i++) {
               for (j=1; j<Nu[1]-1; j++) {
                   U2(i,j) = UN2(i,j);
               }
            }
        }
        """

    if show_animation or no_anim_print_prog:
        while t < t_end: # Loop over all timesteps
            weave.inline(code, ['dt', 'u', 'un','f', 'nu']) # One update of solution
            t += dt # Jump to next timestep

            if show_animation:
                if plot_counter == plot_every_n_frame or t > t_end: #Also plot the very last solution:
                    im.set_array(u.transpose())         # Set new values for u in plot
                    plt.title('2D Temp. dist. t=%f' %(t-dt)) # Update title with current time
                    im.autoscale()          # Fix colorbar and color map to map from min-max
                    plt.draw()              # Update the figure with latest solution
                    plot_every_n_frame += 1 # Plot less frames the further in time we go (ok since solution changes more slowly)
                    plot_counter = 0        # Reset the counter
                plot_counter += 1

            if print_progress:
                percent = t/float(t_end)*100.0 if t<t_end else 100
                sys.stdout.write("\rRunning calculations... %d%% " % percent) # Print out a simple "progress bar" showing percent
                sys.stdout.flush()
    else: # No plot or progress print = fastest possible solution:
        weave.inline(code, ['t_end','dt', 'u', 'un','f', 'nu']) # Time loop in C
    return u


if __name__ == '__main__':
    n = 50  # Mesh-length in x-direction
    m = 100 # Mesh-length in y-direction

    f = SourceTermF_ARRAY(n,m)
    dt = 0.1; t0 = 0; t_end = 200.0; nu = 1.0
    cpu_t0   = time.clock()
    u = SolverWeave(f,nu,dt,n,m,t0,t_end,show_animation=False,print_progress=False)
    cpu_time = time.clock() - cpu_t0

    print "\nMax. temp.:", u.max(), "time taken:", cpu_time
    # Show the solution at the last timesteps (i.e. not close the plot..)
    raw_input('\nPress enter to quit...')
