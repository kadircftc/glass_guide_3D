import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from offset_surface import differentiate


def find_normal_surface(sf, trimline, dist_1, dist_2, nSteps=100, is_draw=False):
    """Find normal surface points from trimline curve using vectorized operations"""
    # Calculate normal vectors
    dzdx, dzdy = differentiate(sf, trimline['x'], trimline['y'])
    
    # Vectorized normal vector calculation
    nx = -dzdx
    ny = -dzdy
    nz = np.ones_like(nx)
    
    # Vectorized normalization
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = nx / norms
    ny = ny / norms
    nz = nz / norms
    
    nPoints = len(trimline['x'])
    
    # Create distance vector with reduced steps
    V = np.linspace(-dist_2, dist_1, nSteps)
    
    # Pre-allocate arrays for better memory efficiency
    total_points = nPoints * nSteps
    newX = np.zeros(total_points)
    newY = np.zeros(total_points)
    newZ = np.zeros(total_points)
    
    # Vectorized point calculation
    for i, v in enumerate(V):
        start_idx = i * nPoints
        end_idx = (i + 1) * nPoints
        newX[start_idx:end_idx] = trimline['x'] + nx * v
        newY[start_idx:end_idx] = trimline['y'] + ny * v
        newZ[start_idx:end_idx] = trimline['z'] + nz * v
    
    # Create result dictionary
    normal_sf_point = {
        'x': newX,
        'y': newY,
        'z': newZ
    }
    
    if is_draw:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(normal_sf_point['x'], normal_sf_point['y'], 
                  normal_sf_point['z'], c='g', marker='.')
        plt.show()
    
    return normal_sf_point

def find_normal_surface_optimized(sf, trimline, dist_1, dist_2, nSteps=15, is_draw=False):
    """Optimized version of find_normal_surface for middle and normal channels"""
    # Reduce trimline points by taking every 3rd point
    reduced_trimline = {
        'x': trimline['x'][::3],
        'y': trimline['y'][::3],
        'z': trimline['z'][::3]
    }
    
    # Calculate normal vectors for reduced points
    dzdx, dzdy = differentiate(sf, reduced_trimline['x'], reduced_trimline['y'])
    
    # Vectorized normal vector calculation
    nx = -dzdx
    ny = -dzdy
    nz = np.ones_like(nx)
    
    # Vectorized normalization
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = nx / norms
    ny = ny / norms
    nz = nz / norms
    
    nPoints = len(reduced_trimline['x'])
    
    # Create distance vector with reduced steps
    V = np.linspace(-dist_2, dist_1, nSteps)
    
    # Pre-allocate arrays for better memory efficiency
    total_points = nPoints * nSteps
    newX = np.zeros(total_points)
    newY = np.zeros(total_points)
    newZ = np.zeros(total_points)
    
    # Vectorized point calculation
    for i, v in enumerate(V):
        start_idx = i * nPoints
        end_idx = (i + 1) * nPoints
        newX[start_idx:end_idx] = reduced_trimline['x'] + nx * v
        newY[start_idx:end_idx] = reduced_trimline['y'] + ny * v
        newZ[start_idx:end_idx] = reduced_trimline['z'] + nz * v
    
    # Create result dictionary
    normal_sf_point = {
        'x': newX,
        'y': newY,
        'z': newZ
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
    
    normal_sf = find_normal_surface_optimized(surf, trimline, 3.5, 13.1, nSteps=15, is_draw=True)
    print(f"Normal surface created with {len(normal_sf['x'])} points") 