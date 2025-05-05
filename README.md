# Glass Guide 3D

3D modeling and visualization tool for glass guide components.

## Features
- 3D surface reconstruction from point clouds
- Mesh generation and visualization
- FreeCAD integration for CAD file export
- Interactive 3D visualization

## Requirements
- Python 3.11+
- FreeCAD 1.0
- Required Python packages (install via pip):
  - numpy
  - scipy
  - matplotlib
  - open3d

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/glass_guide_3D.git
cd glass_guide_3D
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. Install required packages:
```bash
pip install numpy scipy matplotlib open3d
```

4. Make sure FreeCAD is installed and its path is correctly set in `v1/main.py`

## Usage

Run the main script:
```bash
python v1/main.py
```

## Project Structure
- `v1/` - Main source code directory
  - `main.py` - Main program file
  - Supporting Python modules for various functions
- `matlab/` - Input data files
- `output/` - Generated output files (CAD models, etc.)

## License
[MIT License](LICENSE) 