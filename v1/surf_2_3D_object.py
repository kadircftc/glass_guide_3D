import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from offset_surface import differentiate
from scipy.spatial import Delaunay


def surf_2_3D_object(surf_obj, delta, alpha=10, is_draw=False):
    """Convert surface to 3D object with given thickness"""
    # Calculate number of layers
    N = max(round(delta/0.8), 3)
    
    # Calculate normal vectors
    dzdx, dzdy = differentiate(surf_obj['sf'][0], surf_obj['points']['x'], surf_obj['points']['y'])
    nx = -dzdx
    ny = -dzdy
    nz = np.ones_like(nx)
    
    # Normalize normal vectors
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = nx / norms
    ny = ny / norms
    nz = nz / norms
    
    # Create distance vector
    dist = np.linspace(0, -delta, N)
    M = len(surf_obj['points']['x'])
    
    # Initialize arrays
    obj_3d = {
        'x': np.zeros(M*N),
        'y': np.zeros(M*N),
        'z': np.zeros(M*N)
    }
    
    # Create layers
    for n in range(N):
        start_idx = n * M
        end_idx = (n + 1) * M
        obj_3d['x'][start_idx:end_idx] = surf_obj['points']['x'] + dist[n] * nx
        obj_3d['y'][start_idx:end_idx] = surf_obj['points']['y'] + dist[n] * ny
        obj_3d['z'][start_idx:end_idx] = surf_obj['points']['z'] + dist[n] * nz
    
    # Create alpha shape
    points = np.column_stack((obj_3d['x'], obj_3d['y'], obj_3d['z']))
    tri = Delaunay(points)
    obj_3d['shp'] = tri
    
    if is_draw:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot solid object
        ax.plot_trisurf(obj_3d['x'], obj_3d['y'], obj_3d['z'], 
                       triangles=tri.simplices, color='blue', alpha=0.8)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Glass: solid görünüm')
        plt.show()
    
    return obj_3d

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    
    obj_points = surf_2_3D_object(surf, 3.8, 5, is_draw=True)
    print(f"3D object created with {len(obj_points['x'])} points") 