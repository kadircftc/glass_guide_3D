import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay


def combine_guide(glass_guide_offset_2_3d, glass_guide_offset_1_3d,
                 glass_guide_ara_2_3d, glass_guide_ara_1_3d,
                 glass_guide_normal_3d, alpha=10, is_draw=False):
    """Combine guide parts into a single 3D object"""
    # Combine points
    glass_guide_3d = {
        'x': np.concatenate([
            glass_guide_offset_1_3d['x'],
            glass_guide_ara_1_3d['x'],
            glass_guide_normal_3d['x'],
            glass_guide_ara_2_3d['x'],
            glass_guide_offset_2_3d['x']
        ]),
        'y': np.concatenate([
            glass_guide_offset_1_3d['y'],
            glass_guide_ara_1_3d['y'],
            glass_guide_normal_3d['y'],
            glass_guide_ara_2_3d['y'],
            glass_guide_offset_2_3d['y']
        ]),
        'z': np.concatenate([
            glass_guide_offset_1_3d['z'],
            glass_guide_ara_1_3d['z'],
            glass_guide_normal_3d['z'],
            glass_guide_ara_2_3d['z'],
            glass_guide_offset_2_3d['z']
        ])
    }
    
    # Create alpha shape
    points = np.column_stack((glass_guide_3d['x'], glass_guide_3d['y'], glass_guide_3d['z']))
    tri = Delaunay(points)
    glass_guide_3d['shp'] = tri
    
    if is_draw:
        # Plot point cloud
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, projection='3d')
        ax1.scatter(glass_guide_3d['x'], glass_guide_3d['y'], glass_guide_3d['z'], c='b', marker='.')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D Glass: nokta bulutu')
        fig1.savefig('output/3D_glass_guide_point_cloud.png')
        # Plot solid object
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')
        ax2.plot_trisurf(glass_guide_3d['x'], glass_guide_3d['y'], glass_guide_3d['z'],
                        triangles=tri.simplices, color='green', alpha=0.8)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('3D Glass: solid görünüm')
        fig2.savefig('output/3D_glass_guide_solid.png')
        #plt.show()
    
    return glass_guide_3d

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    from surf_2_3D_object import surf_2_3D_object
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    
    # Create test guides
    guide1 = surf_2_3D_object(surf, 0.1, 5)
    guide2 = surf_2_3D_object(surf, -0.1, 5)
    guide3 = surf_2_3D_object(surf, 0.1, 5)
    guide4 = surf_2_3D_object(surf, -0.1, 5)
    guide5 = surf_2_3D_object(surf, 0.1, 5)
    
    combined = combine_guide(guide1, guide2, guide3, guide4, guide5, 5, is_draw=True)
    print(f"Combined guide created with {len(combined['x'])} points") 