from heat_equation_numpy import SolverNumpy
from heat_equation_weave import SolverWeave
from heat_equation import SolverPurePython
import matplotlib.pyplot as plt
from numpy import sin,pi,arange,meshgrid,diff,array
import time

def manufactured_solution(n=50,m=100,t_end_arg=1000,ignore_assert=False):
    """
    Test function for different solvers for the heat equation.
    Not using a too large grid size or too long computation times
    is preferable since some solver are really slow
    If testing is not wanted, the ignore_assert argument should
    be set to True
    """
    nu = 1.0

    def f_list(n,m):
        from math import sin,pi # Not supposed to use numpy versions!
        f = []
        for i in range(n):
            f.append([])
        for i in range(n):
            for j in range(m):
                fij = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2) \
                      *sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
                f[i].append(fij)
        #plt.imshow(zip(*f),cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return f

    def f_array(n,m):
        x   = arange(n); y = arange(m)
        X,Y = meshgrid(x,y) # Make a 2D grid
        f   = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2) \
                *sin(2*pi/(n-1)*X)*sin(2*pi/(m-1)*Y)
        #plt.imshow(f,cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return f.transpose()

    def u_analytic_list(n,m):
        u_a = []
        for i in range(n):
            u_a.append([])
        for i in range(n):
            for j in range(m):
                u_a_ij = sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
                u_a[i].append(u_a_ij)
        #plt.imshow(zip(*u_a),cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return u_a

    def u_analytic_array(n,m):
        x   = arange(n); y = arange(m)
        X,Y = meshgrid(x,y) # Make a 2D grid
        u_a = sin(2*pi/(n-1)*X)*sin(2*pi/(m-1)*Y)
        #plt.imshow(u_a,cmap='gray')
        #plt.colorbar(); plt.show() # Visualize the source term
        return u_a.transpose()

    u_a_l = u_analytic_list(n,m)
    u_a_a = u_analytic_array(n,m)
    if not ignore_assert:
        assert sum(sum(abs(u_a_l - u_a_a))) < 1E-15 # Make sure analytic solution "agrees"

    f_l = f_list(n,m)
    f_a = f_array(n,m)
    if not ignore_assert:
        assert sum(sum(abs(f_l - f_a))) < 1E-15 # Make sure source terms "agrees"

    # Test the speed of the solvers
    t_end = t_end_arg; cpu_t = [time.clock()]
    u_p = SolverPurePython(f_list(n,m), n=n, m=m, t_end=t_end); cpu_t.append(time.clock())
    u_n = SolverNumpy(f_array(n,m), n=n, m=m, t_end=t_end);     cpu_t.append(time.clock())
    u_w = SolverWeave(f_array(n,m), n=n, m=m, t_end=t_end);     cpu_t.append(time.clock())

    cpu_t   = diff(array(cpu_t))
    solvers = ['Python', 'Numpy ', 'Weave ']

    for t,func in zip(cpu_t,solvers):
        print "     Solver %s used %.3f seconds. Speedup: %d X" %(func,t,int(round(cpu_t[0]/float(t))))

    # Compute the largest absolute error on the mesh
    err_p = abs(u_p - array(u_a_l) ).max()
    err_n = abs(u_n - u_a_a).max()
    err_w = abs(u_w - u_a_a).max()

    # Have a look at the abs. error across the mesh (uncomment line)
    #plt.imshow(u_n-u_a_a, cmap='gray', interpolation='None'); plt.colorbar(); plt.show()

    tol = 0.0012
    #print "     Abs. err.: Python: %.2e" %err_p
    #print "     Abs. err.: Numpy:  %.2e" %err_n
    print "     Abs. err.:  %.2e" %err_w
    if not ignore_assert:
        assert err_p < tol and err_n < tol and err_w < tol


def test_manufactured_solution():
    """This will be tested by i.e. py.test or nosetest.
    Checks if analytic solution is achieved after some t_end time has passed"""
    n = 50; m = 80; t_end = 300
    manufactured_solution(n,m,t_end,ignore_assert=False)


if __name__ == '__main__':
    n_list = [10,20,50]; m_list = [20,40,100]
    t_end  = 1000
    for n,m in zip(n_list,m_list):
        print "\nTesting n=%d, m=%d with t1=%d" %(n,m,t_end)
        manufactured_solution(n,m,t_end,ignore_assert=True)
