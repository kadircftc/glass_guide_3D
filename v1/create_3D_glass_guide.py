import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_3D_glass_guide(glass_guide_3d):
    """Create 3D visualization of glass guide"""
    # Plot solid object
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot glass guide
    ax.plot_trisurf(glass_guide_3d['x'], glass_guide_3d['y'], glass_guide_3d['z'],
                   triangles=glass_guide_3d['shp'].simplices, color='green', alpha=0.7)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Glass Guide')
    fig.savefig('output/3D_glass_guide.png')
    #plt.show()

if __name__ == "__main__":
    # Test the function
    from combine_guide import combine_guide
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
    
    glass_guide_3d = combine_guide(guide1, guide2, guide3, guide4, guide5, 5)
    
    create_3D_glass_guide(glass_guide_3d) 