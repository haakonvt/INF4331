from heat_equation_numpy import SolverNumpy
from heat_equation_weave import SolverWeave
from heat_equation import SolverPurePython
import matplotlib.pyplot as plt
from numpy import sin,pi,arange,meshgrid

def test_manufactured_solution():
    n = 50; m = 100; nu = 1.0

    def f_list(n,m):
        f = []
        for i in range(n):
            f.append([])
        for i in range(n):
            for j in range(m):
                fij = nu*((2*pi/n)**2 \
                    + (2*pi/m)**2)*sin(2*pi/m*i)*sin(2*pi/n*j)
                f[i].append(fij)
        #plt.imshow(zip(*f),cmap='gray'); plt.show() # Visualize the source term
        return f

    def f_array(n,m):
        x   = arange(n); y = arange(m)
        X,Y = meshgrid(x,y) # Make a 2D grid
        f   = nu*((2*pi/n)**2 + (2*pi/m)**2)*sin(2*pi/m*X)*sin(2*pi/n*Y)
        #plt.imshow(f,cmap='gray'); plt.show() # Visualize the source term
        return f

    f_l = zip(*f_list(n,m)) # Need to take the transpose of f
    f_a = f_array(n,m)
    assert abs(sum(sum(f_l - f_a))) < 1E-15 # Make sure source terms "agrees"

    def u_analytic_list(n,m):
        u_a = []
        for i in range(n):
            u_a.append([])
        for i in range(n):
            for j in range(m):
                u_a_ij = sin(2*pi/m*i)*sin(2*pi/n*j)
                u_a[i].append(u_a_ij)
        #plt.imshow(zip(*u_a),cmap='gray'); plt.show() # Visualize the source term
        return u_a

    def u_analytic_array(n,m):
        x   = arange(n); y = arange(m)
        X,Y = meshgrid(x,y) # Make a 2D grid
        u_a = sin(2*pi/m*X)*sin(2*pi/n*Y)
        #plt.imshow(u_a,cmap='gray'); plt.show() # Visualize the source term
        return u_a

    u_a_l = zip(*u_analytic_list(n,m)) # Need to take the transpose of u_a
    u_a_a = u_analytic_array(n,m)
    assert abs(sum(sum(u_a_l - u_a_a))) < 1E-15 # Make sure analytic solution "agrees"

test_manufactured_solution()
