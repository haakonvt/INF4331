from heat_equation_numpy import SolverNumpy
from heat_equation_weave import SolverWeave
from heat_equation import SolverPurePython
import matplotlib.pyplot as plt
from numpy import sin,pi,arange,meshgrid,diff,array
import time

def test_manufactured_solution():
    n = 50; m = 100; nu = 1.0

    def f_list(n,m):
        import math # Not supposed to use numpy for "sin" and "pi"
        f = []
        for i in range(n):
            f.append([])
        for i in range(n):
            for j in range(m):
                fij = nu*((2*math.pi/n)**2 \
                    + (2*math.pi/m)**2)*math.sin(2*math.pi/m*i)*math.sin(2*math.pi/n*j)
                f[i].append(fij)
        #plt.imshow(zip(*f),cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return f

    def f_array(n,m):
        x   = arange(n); y = arange(m)
        X,Y = meshgrid(x,y) # Make a 2D grid
        f   = nu*((2*pi/n)**2 + (2*pi/m)**2)*sin(2*pi/m*X)*sin(2*pi/n*Y)
        #plt.imshow(f,cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return f.transpose()

    def u_analytic_list(n,m):
        u_a = []
        for i in range(n):
            u_a.append([])
        for i in range(n):
            for j in range(m):
                u_a_ij = sin(2*pi/m*i)*sin(2*pi/n*j)
                u_a[i].append(u_a_ij)
        #plt.imshow(zip(*u_a),cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return u_a

    def u_analytic_array(n,m):
        x   = arange(n); y = arange(m)
        X,Y = meshgrid(x,y) # Make a 2D grid
        u_a = sin(2*pi/m*X)*sin(2*pi/n*Y)
        #plt.imshow(u_a,cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return u_a.transpose()

    u_a_l = u_analytic_list(n,m)
    u_a_a = u_analytic_array(n,m)
    assert sum(sum(abs(u_a_l - u_a_a))) < 1E-15 # Make sure analytic solution "agrees"

    f_l = f_list(n,m)
    f_a = f_array(n,m)
    assert sum(sum(abs(f_l - f_a))) < 1E-15 # Make sure source terms "agrees"

    # Test the speed of the solvers
    t_end = 200; cpu_t = [time.clock()]
    u_p = SolverPurePython(f_list(n,m),t_end=t_end); cpu_t.append(time.clock())
    u_n = SolverNumpy(f_array(n,m),    t_end=t_end); cpu_t.append(time.clock())
    u_w = SolverWeave(f_array(n,m),    t_end=t_end); cpu_t.append(time.clock())

    cpu_t   = diff(array(cpu_t))
    solvers = ['Python', 'Numpy ', 'Weave ']

    for t,func in zip(cpu_t,solvers):
        print "Solver %s used %.3f seconds. Speedup: %d X" %(func,t,int(round(cpu_t[0]/t)))

    print abs(u_p - array(u_a_l)).max()
    print abs(u_n - u_a_a).max()
    print abs(u_w - u_a_a).max()


if __name__ == '__main__':
    test_manufactured_solution()
