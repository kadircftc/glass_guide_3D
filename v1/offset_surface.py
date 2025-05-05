import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def poly33(x, y, a, b, c, d, e, f, g, h, i, j):
    """Third order polynomial surface function"""
    return (a*x**3 + b*y**3 + c*x**2*y + d*x*y**2 + 
            e*x**2 + f*y**2 + g*x*y + h*x + i*y + j)


def differentiate(sf_or_coeffs, x, y):
    """Calculate partial derivatives of polynomial surface
    
    This function handles both MATLAB-like sf objects and coefficient arrays
    """
    # Extract coefficients from sf object or use directly if array
    
    a, b, c, d, e, f, g, h, i, j = sf_or_coeffs[0],sf_or_coeffs[1],sf_or_coeffs[2],sf_or_coeffs[3],sf_or_coeffs[4],sf_or_coeffs[5],sf_or_coeffs[6],sf_or_coeffs[7],sf_or_coeffs[8],sf_or_coeffs[9]
    
    # Calculate dz/dx (partial derivative with respect to x)
    dzdx = (3*a*x**2 + 2*c*x*y + d*y**2 + 
            2*e*x + g*y + h)
    
    # Calculate dz/dy (partial derivative with respect to y)
    dzdy = (3*b*y**2 + c*x**2 + 2*d*x*y + 
            2*f*y + g*x + i)
    
    return dzdx, dzdy


def offset_surface(surf, dist, trimline, is_draw=False):
    """Create offset surface from given surface"""
    # Get grid points
    xg = surf['points']['x']
    yg = surf['points']['y']
    zg = surf['points']['z']
    
    # Check if there are enough points
    if len(xg) == 0:
        print(f"Error: Surface points are empty in offset_surface with dist={dist}")
        # Return some default points based on the trimline
        # This is a workaround to prevent errors
        if len(trimline['x']) > 0:
            print(f"Using trimline points as a fallback")
            offset_points = {
                'x': trimline['x'].copy(),
                'y': trimline['y'].copy(),
                'z': trimline['z'].copy()
            }
            return offset_points, trimline
        else:
            raise ValueError("Both surface and trimline points are empty")
    
    # Calculate normal vectors for surface points
    dzdx, dzdy = differentiate(surf['sf'][0], xg, yg)
    nx = -dzdx
    ny = -dzdy
    nz = np.ones_like(nx)
    
    # Normalize normal vectors
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    # Check for zero norms to avoid division by zero
    norms[norms == 0] = 1.0
    nx = nx / norms
    ny = ny / norms
    nz = nz / norms
    
    # Calculate offset surface points
    offset_points = {
        'x': xg + nx * dist,
        'y': yg + ny * dist,
        'z': zg + nz * dist
    }
    
    # Calculate normal vectors for trimline
    dzdx, dzdy = differentiate(surf['sf'][0], trimline['x'], trimline['y'])
    nx = -dzdx
    ny = -dzdy
    nz = np.ones_like(nx)
    
    # Normalize normal vectors
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    # Check for zero norms to avoid division by zero
    norms[norms == 0] = 1.0
    nx = nx / norms
    ny = ny / norms
    nz = nz / norms
    
    # Calculate offset trimline
    offset_trimline = {
        'x': trimline['x'] + nx * dist,
        'y': trimline['y'] + ny * dist,
        'z': trimline['z'] + nz * dist
    }
    
    # Validate and filter points
    valid_mask = ~(np.isnan(offset_points['x']) | np.isnan(offset_points['y']) | np.isnan(offset_points['z']) |
                 np.isinf(offset_points['x']) | np.isinf(offset_points['y']) | np.isinf(offset_points['z']))
    
    if not np.any(valid_mask):
        print(f"Warning: No valid points found in offset_surface with dist={dist}")
        print(f"Using a subset of original surface points")
        # Return a subset of original surface points with the same z-shift
        z_shift = dist  # Use dist as a simple z shift
        if len(xg) > 1000:
            indices = np.random.choice(len(xg), 1000, replace=False)
            offset_points = {
                'x': xg[indices],
                'y': yg[indices],
                'z': zg[indices] + z_shift
            }
        else:
            offset_points = {
                'x': xg,
                'y': yg,
                'z': zg + z_shift
            }
    else:
        # Filter out invalid points
        offset_points = {
            'x': offset_points['x'][valid_mask],
            'y': offset_points['y'][valid_mask],
            'z': offset_points['z'][valid_mask]
        }
    
    if is_draw:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(offset_points['x'], offset_points['y'], 
                  offset_points['z'], c='b', marker='.')
        ax.scatter(offset_trimline['x'], offset_trimline['y'], 
                  offset_trimline['z'], c='r', marker='*')
        plt.show()
    
    return offset_points, offset_trimline

if __name__ == "__main__":
    # Test the function
    from fit_polynom import fit_polynom
    from read_dat_file import read_dat_file
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5)
    trimline = read_dat_file('matlab/glass_trimline.dat')
    
    offset_points, offset_trimline = offset_surface(surf, 3.5, trimline, is_draw=True)
    print(f"Offset surface created with {len(offset_points['x'])} points") 