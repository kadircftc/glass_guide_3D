import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from offset_surface import differentiate


def find_normal_surface(sf, trimline, dist_1, dist_2, nSteps=100, is_draw=False):
    """Find normal surface points from trimline curve"""
    # Calculate normal vectors
    dzdx, dzdy = differentiate(sf, trimline['x'], trimline['y'])
    nx = -dzdx
    ny = -dzdy
    nz = np.ones_like(nx)
    
    # Normalize normal vectors
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = nx / norms
    ny = ny / norms
    nz = nz / norms
    
    nPoints = len(trimline['x'])
    
    # Create distance vector
    V = np.linspace(-dist_2, dist_1, nSteps)
    Xs, Vs = np.meshgrid(np.arange(nPoints), V)
    
    # Calculate new points
    newX = trimline['x'][Xs] + nx[Xs] * Vs
    newY = trimline['y'][Xs] + ny[Xs] * Vs
    newZ = trimline['z'][Xs] + nz[Xs] * Vs
    
    # Reshape points
    normal_sf_point = {
        'x': newX.flatten(),
        'y': newY.flatten(),
        'z': newZ.flatten()
    }
    
    if is_draw:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(normal_sf_point['x'], normal_sf_point['y'], 
                  normal_sf_point['z'], c='g', marker='.')
        plt.show()
    
    return normal_sf_point

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    trimline = read_dat_file('matlab/glass_trimline.dat')
    
    normal_sf = find_normal_surface(surf, trimline, 3.5, 13.1, nSteps=100, is_draw=True)
    print(f"Normal surface created with {len(normal_sf['x'])} points") 