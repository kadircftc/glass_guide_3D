import matplotlib

matplotlib.use('TkAgg')  # veya 'Qt5Agg', sisteminizde ne yüklüyse
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull, Delaunay, QhullError


def poly33(x, y, a, b, c, d, e, f, g, h, i, j):
    """Third order polynomial surface function"""
    return (a*x**3 + b*y**3 + c*x**2*y + d*x*y**2 + 
            e*x**2 + f*y**2 + g*x*y + h*x + i*y + j)


def fit_polynom(points, alpha=10, is_draw=False):
    """Fit polynomial surface to points using poly33"""
    # Check if points are empty
    if not points['x'].size or not points['y'].size or not points['z'].size:
        raise ValueError("Input points cannot be empty")
    
    x = points['x']
    y = points['y']
    z = points['z']
    
    sf = fit_surface_poly33(x, y, z)

    z_poly=poly33(x,y,*sf)


    if is_draw:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='r', marker='o')
        ax.scatter(x, y, z_poly, c='b', marker='.')
        plt.show()

    # Return both fitted data and polynomial coefficients
    return {
        'points': {'x': x, 'y': y, 'z': z_poly},
        'sf': [sf]  # Add sf field to match MATLAB structure
    }


def fit_surface_poly33(x, y, z):
    # Tasarım matrisi: tüm 3. derece terimler
    G = np.column_stack((
        x**3,
        y**3,
        x**2 * y,
        x * y**2,
        x**2,
        y**2,
        x * y,
        x,
        y,
        np.ones_like(x)
    ))
    
    coeffs, residuals, rank, s = np.linalg.lstsq(G, z, rcond=None)
    return coeffs

if __name__ == "__main__":
    # Test the function
    from read_dat_file import read_dat_file
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5, is_draw=True)
    print(f"Surface fitted with {len(surf['points']['x'])} points") 