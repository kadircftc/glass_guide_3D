import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_3D_partial_solid_figures(glass_3d, glass_guide_offset_2_3d,
                                   glass_guide_offset_1_3d, glass_guide_ara_2_3d,
                                   glass_guide_ara_1_3d, glass_guide_normal_3d):
    """Create 3D visualization of glass and partial glass guide parts"""
    # Plot solid objects
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot glass
    ax.plot_trisurf(glass_3d['x'], glass_3d['y'], glass_3d['z'],
                   triangles=glass_3d['shp'].simplices, color='blue', alpha=1.0)
    
    # Plot glass guide parts
    ax.plot_trisurf(glass_guide_offset_2_3d['x'], glass_guide_offset_2_3d['y'], glass_guide_offset_2_3d['z'],
                   triangles=glass_guide_offset_2_3d['shp'].simplices, color='green', alpha=0.7)
    ax.plot_trisurf(glass_guide_offset_1_3d['x'], glass_guide_offset_1_3d['y'], glass_guide_offset_1_3d['z'],
                   triangles=glass_guide_offset_1_3d['shp'].simplices, color='green', alpha=0.7)
    ax.plot_trisurf(glass_guide_ara_2_3d['x'], glass_guide_ara_2_3d['y'], glass_guide_ara_2_3d['z'],
                   triangles=glass_guide_ara_2_3d['shp'].simplices, color='green', alpha=0.7)
    ax.plot_trisurf(glass_guide_ara_1_3d['x'], glass_guide_ara_1_3d['y'], glass_guide_ara_1_3d['z'],
                   triangles=glass_guide_ara_1_3d['shp'].simplices, color='green', alpha=0.7)
    ax.plot_trisurf(glass_guide_normal_3d['x'], glass_guide_normal_3d['y'], glass_guide_normal_3d['z'],
                   triangles=glass_guide_normal_3d['shp'].simplices, color='green', alpha=0.7)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Solid görünüm (Parçalı Glass Guide)')
    fig.savefig('output/3D_partial_solid_figures.png')
    plt.show()

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    from surf_2_3D_object import surf_2_3D_object
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    
    # Create test objects
    glass_3d = surf_2_3D_object(surf, 3.8, 5)
    guide1 = surf_2_3D_object(surf, 0.1, 5)
    guide2 = surf_2_3D_object(surf, -0.1, 5)
    guide3 = surf_2_3D_object(surf, 0.1, 5)
    guide4 = surf_2_3D_object(surf, -0.1, 5)
    guide5 = surf_2_3D_object(surf, 0.1, 5)
    
    create_3D_partial_solid_figures(glass_3d, guide1, guide2, guide3, guide4, guide5) 