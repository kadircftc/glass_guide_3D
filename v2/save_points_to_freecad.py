def save_points_to_freecad(parts_dict, filename, isPart=False):
    """
    Her bir parçanın noktalarını FreeCAD dosyasına ayrı ayrı kaydeder.
    parts_dict: {'parca_adi': {'x': [...], 'y': [...], 'z': [...]}, ...}
    filename: Çıktı dosya adı (örn: 'output/freecad/Parcalar.FCStd')
    """
    import os
    import sys

    import numpy as np
    from scipy.spatial import Delaunay
    FREECAD_PATH = r"C:\Program Files\FreeCAD 1.0\bin"
    
    freecad_path = FREECAD_PATH

    if freecad_path not in sys.path:
        sys.path.append(freecad_path)
    os.add_dll_directory(freecad_path)

    import FreeCAD
    import FreeCADGui
    import Mesh
    import Part
    import Points

    print(f"FreeCAD formatında kaydediliyor: {filename}")

    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir) and output_dir:
        os.makedirs(output_dir)
        
    if isPart:
        doc = FreeCAD.newDocument("Parcali")
        for part_name, pts in parts_dict.items():
            # Nokta bulutu oluştur
            points = [FreeCAD.Vector(x, y, z) for x, y, z in zip(pts['x'], pts['y'], pts['z'])]
            cloud = Points.Points(points)
            point_obj = doc.addObject("Points::Feature", f"{part_name}_points")
            point_obj.Points = cloud
            
            # Delaunay üçgenleme ile yüzey oluştur
            points_array = np.column_stack((pts['x'], pts['y'], pts['z']))
            tri = Delaunay(points_array[:, :2])  # XY düzleminde üçgenleme
            
            # Üçgenleri FreeCAD mesh'ine dönüştür
            mesh_faces = []
            for triangle in tri.simplices:
                mesh_faces.append([
                    points[triangle[0]],
                    points[triangle[1]],
                    points[triangle[2]]
                ])
            
            mesh = Mesh.Mesh(mesh_faces)
            mesh_obj = doc.addObject("Mesh::Feature", f"{part_name}_mesh")
            mesh_obj.Mesh = mesh
            
            # Mesh'i yüzeye dönüştür (daha yüksek hassasiyet)
            shape = Part.Shape()
            shape.makeShapeFromMesh(mesh.Topology, 0.005)  # Hassasiyeti artırdık
            
            # Yüzeyi oluştur
            surface = doc.addObject("Part::Feature", part_name)
            surface.Shape = shape
            
            # Yüzeyi yumuşat
            try:
                # Yüzeyi yumuşatma işlemi
                surface.Shape = surface.Shape.removeSplitter()
                # Yüzeyi birleştir
                surface.Shape = surface.Shape.fuse(surface.Shape)
            except Exception as e:
                print(f"Yüzey yumuşatma hatası: {e}")
            
    else:
        doc = FreeCAD.newDocument("Tum")
        for part_name, pts in parts_dict.items():
            # Nokta bulutu oluştur
            points = [FreeCAD.Vector(x, y, z) for x, y, z in zip(pts['x'], pts['y'], pts['z'])]
            cloud = Points.Points(points)
            point_obj = doc.addObject("Points::Feature", f"{part_name}_points")
            point_obj.Points = cloud
            
            # Delaunay üçgenleme ile yüzey oluştur
            points_array = np.column_stack((pts['x'], pts['y'], pts['z']))
            tri = Delaunay(points_array[:, :2])  # XY düzleminde üçgenleme
            
            # Üçgenleri FreeCAD mesh'ine dönüştür
            mesh_faces = []
            for triangle in tri.simplices:
                mesh_faces.append([
                    points[triangle[0]],
                    points[triangle[1]],
                    points[triangle[2]]
                ])
            
            mesh = Mesh.Mesh(mesh_faces)
            mesh_obj = doc.addObject("Mesh::Feature", f"{part_name}_mesh")
            mesh_obj.Mesh = mesh
            
            # Mesh'i yüzeye dönüştür (daha yüksek hassasiyet)
            shape = Part.Shape()
            shape.makeShapeFromMesh(mesh.Topology, 0.01)  # Hassasiyeti artırdık
            
            # Yüzeyi oluştur
            surface = doc.addObject("Part::Feature", part_name)
            surface.Shape = shape
            
            # Yüzeyi yumuşat
            try:
                # Yüzeyi yumuşatma işlemi
                surface.Shape = surface.Shape.removeSplitter()
                # Yüzeyi birleştir
                surface.Shape = surface.Shape.fuse(surface.Shape)
            except Exception as e:
                print(f"Yüzey yumuşatma hatası: {e}")

    doc.recompute()
    doc.saveAs(filename)
    
    # STEP formatında da kaydet
    try:
        step_file = os.path.splitext(filename)[0] + ".stp"
        Part.export(doc.Objects, step_file)
        print(f"STEP formatında kaydedildi: {step_file}")
    except Exception as e:
        print(f"STEP dışa aktarma hatası: {e}")
    
    print(f"FreeCAD dosyası kaydedildi: {filename}")