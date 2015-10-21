import matplotlib.pyplot as plt
from scipy import weave
import numpy as np
import sys,time


def SourceTermF_ARRAY(Nx,Ny):
    # Initiate the array with constant f = 1
    f = np.ones((Nx,Ny))
    return f


def SolverWeave(f, nu=1, dt=0.1, Nx=50, Ny=100, t0 = 0, t_end=1000):
    """
    Solver for heat equation. Solved in C using weave.
    Dirichlet boundary conditions: ( u_edge = 0 )
    """
    t = t0

    # Initiate the solution array for u_n
    u     = np.zeros((Nx,Ny))

    code = """
    int t,i,j,max_steps;
    max_steps = int(round(t_end/dt));
    for (t=0; t<max_steps; t++){
        for (i=1; i<Nu[0]-1; i++) {
           for (j=1; j<Nu[1]-1; j++) {
               U2(i,j) = U2(i,j) \
                        + dt*(nu*U2(i-1,j) + nu*U2(i,j-1) - 4*nu*U2(i,j) \
                        + nu*U2(i,j+1) + nu*U2(i+1,j) + F2(i,j));
           }
        }
    }
    """

    # Loop over all timesteps
    weave.inline(code, ['t_end','dt', 'u', 'f', 'nu'])
    return u


if __name__ == '__main__':
    Nx = 50  # Mesh-length in x-direction
    Ny = 100 # Mesh-length in y-direction

    f = SourceTermF_ARRAY(Nx,Ny)
    dt = 0.1; t0 = 0; t_end = 1000; nu = 1.0
    cpu_t0   = time.clock()
    u = SolverWeave(f,nu,dt,Nx,Ny,t0,t_end)
    cpu_time = time.clock() - cpu_t0

    print "\nMax. temp.:", u.max(), "time taken:", cpu_time
    # Show the solution at the last timesteps (i.e. not close the plot..)
    raw_input('\nPress enter to quit...')
