import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_3D_full_solid_figures(glass_3d, glass_guide_3d):
    """Create 3D visualization of glass and glass guide"""
    # Plot point cloud
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.scatter(glass_3d['x'], glass_3d['y'], glass_3d['z'], c='b', marker='.')
    ax1.scatter(glass_guide_3d['x'], glass_guide_3d['y'], glass_guide_3d['z'], c='m', marker='.')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('3D Nokta bulutu')
    fig1.savefig('output/3D_full_solid_figures_point_cloud.png')
    # Plot solid objects
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    
    # Plot glass
    ax2.plot_trisurf(glass_3d['x'], glass_3d['y'], glass_3d['z'],
                    triangles=glass_3d['shp'].simplices, color='blue', alpha=1.0)
    
    # Plot glass guide
    ax2.plot_trisurf(glass_guide_3d['x'], glass_guide_3d['y'], glass_guide_3d['z'],
                    triangles=glass_guide_3d['shp'].simplices, color='green', alpha=0.7)
    
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('3D Solid görünüm')
    fig2.savefig('output/3D_full_solid_figures.png')
    #plt.show()

if __name__ == "__main__":
    # Test the function
    from combine_guide import combine_guide
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    from surf_2_3D_object import surf_2_3D_object
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    
    # Create test objects
    glass_3d = surf_2_3D_object(surf, 3.8, 5)
    
    # Create test guides
    guide1 = surf_2_3D_object(surf, 0.1, 5)
    guide2 = surf_2_3D_object(surf, -0.1, 5)
    guide3 = surf_2_3D_object(surf, 0.1, 5)
    guide4 = surf_2_3D_object(surf, -0.1, 5)
    guide5 = surf_2_3D_object(surf, 0.1, 5)
    
    glass_guide_3d = combine_guide(guide1, guide2, guide3, guide4, guide5, 5)
    
    create_3D_full_solid_figures(glass_3d, glass_guide_3d) 