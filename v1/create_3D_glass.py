import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_3D_glass(glass_3d):
    """Create 3D visualization of glass"""
    # Plot solid object
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot glass
    ax.plot_trisurf(glass_3d['x'], glass_3d['y'], glass_3d['z'],
                   triangles=glass_3d['shp'].simplices, color='blue', alpha=1.0)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Glass')
    fig.savefig('output/3D_glass.png')
    #plt.show()

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    from surf_2_3D_object import surf_2_3D_object
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    
    # Create test glass object
    glass_3d = surf_2_3D_object(surf, 3.8, 5)
    
    create_3D_glass(glass_3d) 