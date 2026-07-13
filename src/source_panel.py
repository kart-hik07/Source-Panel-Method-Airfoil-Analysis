import numpy as np
import matplotlib.pyplot as plt

def load_airfoil(filename):
    data = np.loadtxt(filename, skiprows=1)
    x = data[:, 0]
    y = data[:, 1]
    return x, y

def source_panel_airfoil(filename, V_inf=1.0, alpha_deg=0.0):
    alpha = np.radians(alpha_deg)


    x, y = load_airfoil(filename)
    N = len(x) - 1 

   
    xc = 0.5 * (x[:-1] + x[1:])
    yc = 0.5 * (y[:-1] + y[1:])

 
    dx = x[1:] - x[:-1]
    dy = y[1:] - y[:-1]
    length = np.sqrt(dx**2 + dy**2)

    nx = dy / length
    ny = -dx / length


    A = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                A[i, j] = 0.5
            else:
                dx_ = xc[i] - xc[j]
                dy_ = yc[i] - yc[j]
                r2 = dx_**2 + dy_**2
                A[i, j] = (dx_ * nx[i] + dy_ * ny[i]) / (2 * np.pi * r2)

    b = -V_inf * (np.cos(alpha) * nx + np.sin(alpha) * ny)

    sigma = np.linalg.solve(A, b)

    Vt = V_inf + sigma / (2 * np.pi * length)
    Cp = 1 - (Vt / V_inf)**2

    plt.figure(figsize=(10, 4))
    plt.plot(xc, Cp, '-o')
    plt.gca().invert_yaxis()
    plt.title("Cp Distribution (Source Panel Method)")
    plt.xlabel("x")
    plt.ylabel("Cp")
    plt.grid(True)
    plt.show()

source_panel_airfoil("naca0012.dat", V_inf=1.0, alpha_deg=0.0)
