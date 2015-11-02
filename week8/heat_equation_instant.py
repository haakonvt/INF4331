from instant import inline_with_numpy
import numpy as np
import sys,time

def SourceTermF_ARRAY(n,m,constant=1):
    """
    Initiate the array (source term f(x,y)) with constant:
    f = 1 or f = constant if specified by user.
    """
    f = constant*np.ones((n,m))
    return f


def SolverInstant(f, nu=1, dt=0.1, n=50, m=100, t0 = 0, t_end=1000, u0=None):
    """
    Solver for heat equation. Solved in C using Instant.
    Dirichlet boundary conditions: ( u_edge = 0 )
    If possible, time loop will automatically be done in C
    for additional speed.
    """
    t = t0; t_end = t_end + 1E-8
    no_anim_print_prog = False

    # Initiate the solution array for u and u_new (un)
    u  = np.zeros((n,m)) if u0 == None else u0
    un = np.zeros((n,m)) if u0 == None else u0.copy()

    # Keep time loop in C-code for improved speed
    c_code = """
    void heateq(int ux, int uy, double* u, int unx, int uny, double* un, int fx, int fy, double* f){
      double dt = %f;
      double nu = %f;
      double t_end = %f;
      int t,i,j;
      for (t=0; t*dt<t_end+dt; t++){
        for (i=1; i<ux-1; i++){
          for (j=1; j<uy-1; j++){
            un[i*uy + j] = u[i*uy +j] \
                       + dt*nu*(u[(i-1)*uy +j] + u[i*uy +j-1] - 4*u[i*uy +j] \
                       + u[i*uy +j+1] + u[(i+1)*uy +j]) + dt*nu*f[i*uy +j];
          }
        }
        for (i=1; i<ux-1; i++) {
           for (j=1; j<uy-1; j++) {
               u[i*uy + j] = un[i*uy + j];
           }
        }
      }
    }
    """%(dt,nu,t_end) # Add these values into C-code "as text"

    heateq_func = inline_with_numpy(c_code, arrays = [['ux', 'uy', 'u'],
                                                   ['unx', 'uny', 'un'],
                                                   ['fx', 'fy', 'f']])
    heateq_func(u,un,f) # Run through all time steps in C

    return u


if __name__ == '__main__':
    n = 50  # Mesh-length in x-direction
    m = 100 # Mesh-length in y-direction

    f = SourceTermF_ARRAY(n,m)
    dt = 0.1; t0 = 0; t_end = 1000.0; nu = 1.0
    cpu_t0   = time.clock()
    u = SolverInstant(f,nu,dt,n,m,t0,t_end)
    cpu_time = time.clock() - cpu_t0

    print "\nMax. temp.:", u.max(), "time taken:", cpu_time
    # Show the solution at the last timesteps (i.e. not close the plot..)
    raw_input('\nPress enter to quit...')
