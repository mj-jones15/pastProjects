# Project 4 Filled Implementations

import numpy as np
import matplotlib.pyplot as plt
from polyLagrange import PolyEvalLagrange

###############################################################
# P1. Natural Cubic Spline
###############################################################

def SplineCubic(tdata, ydata, x):
    tdata = np.array(tdata, dtype=float)
    ydata = np.array(ydata, dtype=float)
    x = np.array(x, dtype=float)

    n = len(tdata) - 1
    h = np.diff(tdata)

    # Build tridiagonal system for M (second derivatives)
    A = np.zeros((n+1, n+1))
    b = np.zeros(n+1)

    # Natural spline boundary conditions
    A[0,0] = 1
    A[n,n] = 1

    # Fill interior rows
    for i in range(1, n):
        A[i, i-1] = h[i-1]
        A[i, i]   = 2*(h[i-1] + h[i])
        A[i, i+1] = h[i]
        b[i] = 6*((ydata[i+1]-ydata[i])/h[i] - (ydata[i]-ydata[i-1])/h[i-1])

    # Solve for M
    M = np.linalg.solve(A, b)

    # Evaluate spline piecewise
    sx = np.zeros_like(x)
    for j, xv in enumerate(x):
        # find interval
        i = np.searchsorted(tdata, xv) - 1
        if i < 0:
            i = 0
        if i >= n:
            i = n-1

        hi = h[i]
        t_i = tdata[i]
        t_ip = tdata[i+1]

        term1 = (M[i]/(6*hi)) * (t_ip - xv)**3
        term2 = (M[i+1]/(6*hi)) * (xv - t_i)**3
        term3 = (ydata[i]/hi - M[i]*hi/6) * (t_ip - xv)
        term4 = (ydata[i+1]/hi - M[i+1]*hi/6) * (xv - t_i)

        sx[j] = term1 + term2 + term3 + term4

    return sx

###############################################################
# P1. Lagrange Interpolation Wrapper
###############################################################

def lagrange_interpolant(xdata, ydata, x):
    return PolyEvalLagrange(x, xdata, ydata)

###############################################################
# Runge Function
###############################################################

def runge_function(x):
    return 1/(1 + 25*x*x)

###############################################################
# P2. Euler and RK4
###############################################################

def euler_method(f, x0, t0, tf, h):
    N = int((tf - t0)/h)
    t = np.linspace(t0, tf, N+1)
    x = np.zeros(N+1)
    x[0] = x0

    for i in range(N):
        x[i+1] = x[i] + h*f(t[i], x[i])

    return t, x


def rk4_method(f, x0, t0, tf, h):
    N = int((tf - t0)/h)
    t = np.linspace(t0, tf, N+1)
    x = np.zeros(N+1)
    x[0] = x0

    for i in range(N):
        k1 = f(t[i], x[i])
        k2 = f(t[i] + h/2, x[i] + h*k1/2)
        k3 = f(t[i] + h/2, x[i] + h*k2/2)
        k4 = f(t[i] + h, x[i] + h*k3)
        x[i+1] = x[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

    return t, x

###############################################################
# Exact Solutions
###############################################################

def exact_ivp1(t):
    return 1 + 0.5*np.exp(-4*t) - 0.5*np.exp(-2*t)


def exact_ivp2(t):
    return np.exp(t/2)*np.sin(5*t)

###############################################################
# IVP Right-hand Sides
###############################################################

def f_ivp1(t, x):
    return 2 - 2*x - np.exp(-4*t)


def f_ivp2(t, x):
    return x + 5*np.exp(t/2)*np.cos(5*t) - 0.5*np.exp(t/2)*np.sin(5*t)


###############################################################
# Runge Comparison and IVP Plotting
###############################################################

def compare_runge(n):
    # Equally spaced nodes
    xdata = np.linspace(-1, 1, n+1)
    ydata = runge_function(xdata)

    # Fine grid
    xf = np.linspace(-1, 1, 1000)
    yf = runge_function(xf)

    # Lagrange polynomial
    ylag = lagrange_interpolant(xdata, ydata, xf)

    # Natural cubic spline
    yspl = SplineCubic(xdata, ydata, xf)

    # Plot
    plt.figure(figsize=(8,5))
    plt.plot(xf, yf, label="Runge f(x)")
    plt.plot(xf, ylag, label=f"Lagrange P_{n}(x)")
    plt.plot(xf, yspl, label="Natural Cubic Spline S(x)")
    plt.scatter(xdata, ydata, color='black', s=15)
    plt.title(f"Runge Comparison for n = {n}")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_ivp_solutions():
    hs = [0.1, 0.05, 0.01]

    for h in hs:
        # IVP1
        t_exact = np.linspace(0, 5, 1000)
        x_exact = exact_ivp1(t_exact)

        t_eu, x_eu = euler_method(f_ivp1, x0=1, t0=0, tf=5, h=h)

        plt.figure(figsize=(8,4))
        plt.plot(t_exact, x_exact, label="Exact")
        plt.plot(t_eu, x_eu, label=f"Euler h={h}")
        plt.title(f"IVP1 with h = {h}")
        plt.grid(True)
        plt.legend()
        plt.show()

        # IVP2
        x_exact2 = exact_ivp2(t_exact)
        t_eu2, x_eu2 = euler_method(f_ivp2, x0=0, t0=0, tf=5, h=h)

        plt.figure(figsize=(8,4))
        plt.plot(t_exact, x_exact2, label="Exact")
        plt.plot(t_eu2, x_eu2, label=f"Euler h={h}")
        plt.title(f"IVP2 with h = {h}")
        plt.grid(True)
        plt.legend()
        plt.show()

        # RK4 for IVP1
        t_rk, x_rk = rk4_method(f_ivp1, x0=1, t0=0, tf=5, h=h)

        plt.figure(figsize=(8,4))
        plt.plot(t_exact, x_exact, label="Exact")
        plt.plot(t_rk, x_rk, label=f"RK4 h={h}")
        plt.title(f"IVP1 RK4 with h = {h}")
        plt.grid(True)
        plt.legend()
        plt.show()

        # RK4 for IVP2
        t_rk2, x_rk2 = rk4_method(f_ivp2, x0=0, t0=0, tf=5, h=h)

        plt.figure(figsize=(8,4))
        plt.plot(t_exact, x_exact2, label="Exact")
        plt.plot(t_rk2, x_rk2, label=f"RK4 h={h}")
        plt.title(f"IVP2 RK4 with h = {h}")
        plt.grid(True)
        plt.legend()
        plt.show()


###############################################################
# Main Driver for Project 4
###############################################################

def main():
    # Runge comparisons for n = 5, 10, 20
    for n in [5, 10, 20]:
        compare_runge(n)

    # IVP plots
    plot_ivp_solutions()


if __name__ == "__main__":
    main()
