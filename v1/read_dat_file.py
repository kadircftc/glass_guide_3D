import numpy as np


def read_dat_file(filename):
    """Read .dat file and return points as numpy array (like MATLAB version)"""
    data = []

    with open(filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and header
            if not line or line.startswith('*NODE'):
                continue
            # Parse numeric data
            parts = list(map(float, line.split(',')))
            data.append(parts)

    data = np.array(data)

    # Create structure similar to MATLAB struct
    points = {
        'x': data[:, 1],
        'y': data[:, 2],
        'z': data[:, 3]
    }
    return points

if __name__ == "__main__":
    points = read_dat_file('matlab/glass2.5kpoint.dat')
    print(f"Number of points: {len(points['x'])}")
    print(f"First point: ({points['x'][0]}, {points['y'][0]}, {points['z'][0]})")
