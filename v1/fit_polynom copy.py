import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend to avoid GUI issues
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from scipy.spatial import Delaunay


def poly33(x, y, a, b, c, d, e, f, g, h, i, j):
    """Third order polynomial surface function"""
    return (a*x**3 + b*y**3 + c*x**2*y + d*x*y**2 + 
            e*x**2 + f*y**2 + g*x*y + h*x + i*y + j)


def fit_polynom(points, alpha=10, is_draw=False):
    """Fit polynomial surface to points using poly33"""
    # Check if points are empty
    if not points['x'].size or not points['y'].size or not points['z'].size:
        raise ValueError("Input points cannot be empty")
    
    x = points['x']
    y = points['y']
    z = points['z']
    
    # Remove any NaN or infinite values
    valid_mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(z) |
                  np.isinf(x) | np.isinf(y) | np.isinf(z))
    x = x[valid_mask]
    y = y[valid_mask]
    z = z[valid_mask]
    
    if not x.size:
        raise ValueError("No valid points after removing NaN and infinite values")
    
    # Center and scale the data
    x_mean, y_mean, z_mean = np.mean(x), np.mean(y), np.mean(z)
    x_scale = np.max(np.abs(x - x_mean))
    y_scale = np.max(np.abs(y - y_mean))
    z_scale = np.max(np.abs(z - z_mean))
    
    x_norm = (x - x_mean) / x_scale
    y_norm = (y - y_mean) / y_scale
    z_norm = (z - z_mean) / z_scale
    
    # Create grid for interpolation
    x_min, x_max = np.min(x_norm), np.max(x_norm)
    y_min, y_max = np.min(y_norm), np.max(y_norm)
    
    xi = np.linspace(x_min, x_max, 500)
    yi = np.linspace(y_min, y_max, 500)
    xi, yi = np.meshgrid(xi, yi)
    
    # Define the function to fit
    def func(data, a, b, c, d, e, f, g, h, i, j):
        x, y = data
        return poly33(x, y, a, b, c, d, e, f, g, h, i, j)
    
    # Initial guess for parameters based on data characteristics
    p0 = [0.0] * 10
    p0[8] = np.mean(z_norm)  # Linear term in y
    p0[7] = np.mean(z_norm)  # Linear term in x
    p0[9] = np.mean(z_norm)  # Constant term
    
    # Fit polynomial surface with increased max iterations and bounds
    try:
        popt, _ = curve_fit(func, (x_norm, y_norm), z_norm, p0=p0, 
                           maxfev=20000, bounds=(-10, 10))
    except RuntimeError:
        # If first attempt fails, try with different initial guess
        p0 = [0.1] * 10
        popt, _ = curve_fit(func, (x_norm, y_norm), z_norm, p0=p0, 
                           maxfev=20000, bounds=(-10, 10))
    
    # Denormalize coefficients
    a, b, c, d, e, f, g, h, i, j = popt
    
    # Scale back the coefficients
    a = a / (x_scale**3 * z_scale)
    b = b / (y_scale**3 * z_scale)
    c = c / (x_scale**2 * y_scale * z_scale)
    d = d / (x_scale * y_scale**2 * z_scale)
    e = e / (x_scale**2 * z_scale)
    f = f / (y_scale**2 * z_scale)
    g = g / (x_scale * y_scale * z_scale)
    h = h / (x_scale * z_scale)
    i = i / (y_scale * z_scale)
    j = j / z_scale - (a*x_mean**3 + b*y_mean**3 + c*x_mean**2*y_mean + 
                      d*x_mean*y_mean**2 + e*x_mean**2 + f*y_mean**2 + 
                      g*x_mean*y_mean + h*x_mean + i*y_mean)
    
    # Calculate z values for the grid
    zi = poly33(xi, yi, *popt)
    zi = zi * z_scale + z_mean
    
    # Create alpha shape, more similar to MATLAB's approach
    # Skip alpha shape filtering if there are too few points
    if len(x) > 3:
        try:
            # Try to use Delaunay triangulation to filter points
            tri = Delaunay(np.column_stack((x_norm, y_norm)))
            in_shape = np.zeros_like(xi, dtype=bool)
            
            # Limit the number of points to check to prevent very long execution times
            # Sample points from the grid at regular intervals
            step = max(1, xi.shape[0] // 100)  # Check up to 100x100 points
            
            for i in range(0, xi.shape[0], step):
                for j in range(0, xi.shape[1], step):
                    if tri.find_simplex([xi[i,j], yi[i,j]]) >= 0:
                        in_shape[i:i+step, j:j+step] = True
            
            # Set points outside alpha shape to NaN
            zi[~in_shape] = np.nan
        except Exception as e:
            print(f"Alpha shape creation failed: {e}. Using all points.")
    
    # Reshape data
    fitted_data = {
        'x': xi.flatten(),
        'y': yi.flatten(),
        'z': zi.flatten()
    }
    
    # Remove NaN values
    valid_indices = ~np.isnan(fitted_data['z'])
    fitted_data = {k: v[valid_indices] for k, v in fitted_data.items()}
    
    # If no valid points remain, use a subsample of the original points
    # This ensures we always have some points
    if len(fitted_data['x']) == 0:
        print("Warning: No valid points after alpha shape. Using original points.")
        # Use a random subset of the original points to prevent memory issues with large datasets
        if len(x) > 1000:
            indices = np.random.choice(len(x), 1000, replace=False)
            fitted_data = {
                'x': x[indices], 
                'y': y[indices], 
                'z': z[indices]
            }
        else:
            fitted_data = {'x': x, 'y': y, 'z': z}
    
    if is_draw:
        # Plot original points
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='r', marker='o')
        
        # Plot fitted surface
        if len(fitted_data['x']) > 0:
            # Use scatter for fitted points
            ax.scatter(fitted_data['x'], fitted_data['y'], fitted_data['z'], 
                      c='b', marker='.', alpha=0.5)
        
        plt.show()
    
    # Return both fitted data and polynomial coefficients
    return {
        'points': fitted_data,
        'coefficients': [a, b, c, d, e, f, g, h, i, j],
        'sf': [a, b, c, d, e, f, g, h, i, j]  # Add sf field to match MATLAB structure
    }

if __name__ == "__main__":
    # Test the function
    from read_dat_file import read_dat_file
    
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    surf = fit_polynom(points, alpha=5, is_draw=True)
    print(f"Surface fitted with {len(surf['points']['x'])} points") 