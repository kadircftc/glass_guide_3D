import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from offset_surface import poly33


def cut_glass_guide(surf_offset_dist1, surf_offset_cut_1, is_draw=False):
    """Cut glass guide surface using cutting surface"""
    # Get grid points
    X = surf_offset_dist1['points']['x']
    Y = surf_offset_dist1['points']['y']
    
    # Calculate surface values
    Z1 = surf_offset_dist1['points']['z']
    Z2=poly33(X, Y,*surf_offset_cut_1['sf'][0])
    # Calculate intersection difference
    delta = Z1 - Z2
    
    mask = delta < 0


    offset_dist1_updated_points = {
    'x': X[~mask],
    'y': Y[~mask],
    'z': Z1[~mask]
    }

    Z1_masked = offset_dist1_updated_points['z']
    
    if is_draw:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z1_masked, cmap='viridis', edgecolor='none')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Kesişimden sonra kalan taraf')
        plt.show()
    
    return offset_dist1_updated_points

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf1 = fit_polynom(points, alpha=5)
    surf2 = fit_polynom(points, alpha=5)
    
    cut_points = cut_glass_guide(surf1, surf2, is_draw=True)
    print(f"Cut surface created with {len(cut_points['x'])} points") 