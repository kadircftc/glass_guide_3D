import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from combine_guide import combine_guide
from create_3D_full_solid_figures import create_3D_full_solid_figures
from create_3D_glass import create_3D_glass
from create_3D_glass_guide import create_3D_glass_guide
from create_3D_partial_solid_figures import create_3D_partial_solid_figures
from cut_glass_guide import cut_glass_guide
from find_normal_surface import (find_normal_surface,
                                 find_normal_surface_optimized)
from fit_polynom import fit_polynom
from offset_surface import offset_surface
from read_dat_file import read_dat_file
from surf_2_3D_object import surf_2_3D_object

# FreeCAD yolunu burada tanımlayın - kendi sisteminize göre değiştirin
FREECAD_PATH = r"C:\Program Files\FreeCAD 1.0\bin"

def reduce_points(points, factor=2):
    """Reduce the number of points by sampling every nth point"""
    return {
        'x': points['x'][::factor],
        'y': points['y'][::factor],
        'z': points['z'][::factor]
    }

def save_to_freecad(obj_3d, filename, freecad_path=None):
    """3D modeli FreeCAD formatında kaydet"""
    try:
        if freecad_path is None:
            # Varsayılan FreeCAD yolu - global değişkenden al
            freecad_path = FREECAD_PATH
            
        if freecad_path not in sys.path:
            sys.path.append(freecad_path)
            
        
        os.add_dll_directory(freecad_path)
           
        
        import FreeCAD
        import Mesh
        import Part
        
        print(f"FreeCAD formatında kaydediliyor: {filename}")
        
        # Çıktı dizinini kontrol et ve oluştur
        output_dir = os.path.dirname(filename)
        if not os.path.exists(output_dir) and output_dir:
            os.makedirs(output_dir)
        
        # FreeCAD belgesi oluştur
        doc = FreeCAD.newDocument("Model")
        
        # Nokta ve yüz verilerini hazırla
        points = []
        for i in range(len(obj_3d['x'])):
            points.append(FreeCAD.Vector(obj_3d['x'][i], obj_3d['y'][i], obj_3d['z'][i]))
        
        faces = obj_3d['shp'].simplices
        
        # Mesh oluştur
        mesh_faces = []
        for face in faces:
            mesh_faces.append([points[face[0]], points[face[1]], points[face[2]]])
        
        mesh_obj = Mesh.Mesh(mesh_faces)
        mesh_feature = doc.addObject("Mesh::Feature", "ModelMesh")
        mesh_feature.Mesh = mesh_obj
        
        # Mesh'i solide dönüştürmeyi dene
        try:
            # Mesh'ten şekil oluştur
            shape = Part.Shape()
            shape.makeShapeFromMesh(mesh_obj.Topology, 0.1)
            
            # Kapalı şekilden solid oluştur
            if shape.isClosed():
                solid = Part.makeSolid(shape)
                solid_obj = doc.addObject("Part::Feature", "ModelSolid")
                solid_obj.Shape = solid
                print("  Solid model oluşturuldu")
        except Exception as e:
            print(f"  Solid dönüştürme hatası: {e}")
        
        # Belgeyi yeniden hesapla ve kaydet
        doc.recompute()
        doc.saveCopy(filename)
        
        # STEP formatında da kaydet
        try:
            step_file = os.path.splitext(filename)[0] + ".stp"
            Part.export(doc.Objects, step_file)
            print(f"  STEP formatında kaydedildi: {step_file}")
        except Exception as e:
            print(f"  STEP dışa aktarma hatası: {e}")
            
        return True
        
    except ImportError as e:
        print(f"FreeCAD modülleri yüklenemedi: {e}")
        print("  FreeCAD'in yüklü olduğundan emin olun.")
        print("  Bu fonksiyon FreeCAD'in Python yorumlayıcısı ile çalıştırılmalıdır.")
        print(f"  FreeCAD yolu: {freecad_path}")
        return False
        
    except Exception as e:
        print(f"FreeCAD'e kaydetme hatası: {e}")
        return False


def main():
    # Input parameters
    delta_glass = 3.8  # glass thickness
    delta_guide = 0.1  # channel thickness
    dist_1 = 3.5  # distance to outer (top) channel
    dist_2 = 13.1 + delta_glass  # distance to inner (bottom) channel
    dist_3 = 6.2  # distance to opposite channel (reduced from 6.2 for stability)
    len_1 = 13.3 - delta_guide  # length of outer (top) channel
    len_2 = 28.8 - delta_guide  # length of inner (bottom) channel

    alpha = 4  # parameter for determining surface boundaries in polynomial fitting

    print("\n=== Reading data files ===")
    # Read data files
    GLASS_POINTS = read_dat_file('matlab/glass2.5kpoint.dat')
    print(f"GLASS_POINTS size: {len(GLASS_POINTS['x'])} points")
    
    GLASS_GUIDE_POINTS = read_dat_file('matlab/glass_guide_wall2.5kpoints.dat')
    print(f"GLASS_GUIDE_POINTS size: {len(GLASS_GUIDE_POINTS['x'])} points")
    
    GLASS_TRIMLINE_POINTS = read_dat_file('matlab/glass_trimline.dat')
    # Reduce trimline points
    GLASS_TRIMLINE_POINTS = reduce_points(GLASS_TRIMLINE_POINTS, factor=2)
    print(f"GLASS_TRIMLINE_POINTS size: {len(GLASS_TRIMLINE_POINTS['x'])} points")

    print("\n=== Fitting polynomial surface ===")
    # Fit polynomial surface
    SURF_glass = fit_polynom(GLASS_POINTS, alpha, False)
    print(f"SURF_glass points size: {len(SURF_glass['points']['x'])} points")

    # Find normal surface
    print("\n=== Finding normal surface ===")
    normal_sf_point = find_normal_surface_optimized(SURF_glass['sf'][0], GLASS_TRIMLINE_POINTS, dist_1, dist_2, 15, False)
    print(f"normal_sf_point size: {len(normal_sf_point['x'])} points")
    
    SURF_normal2glass = fit_polynom(normal_sf_point, alpha, False)
    print(f"SURF_normal2glass points size: {len(SURF_normal2glass['points']['x'])} points")
    
    print("\n=== Creating offset surface with distance:", dist_3, "===")
    offset_normal2glass_points, _ = offset_surface(SURF_normal2glass, dist_3, GLASS_TRIMLINE_POINTS, False)
    print(f"offset_normal2glass_points size: {len(offset_normal2glass_points['x'])} points")
    
    SURF_offset_normal2glass = fit_polynom(offset_normal2glass_points, alpha)
    print(f"SURF_offset_normal2glass points size: {len(SURF_offset_normal2glass['points']['x'])} points")

    # dist 1
    print("\n=== Processing dist_1 ===")
    offset_glass_points_dist1, trimline_dist1 = offset_surface(SURF_glass, dist_1, GLASS_TRIMLINE_POINTS, False)
    print(f"offset_glass_points_dist1 size: {len(offset_glass_points_dist1['x'])} points")

    SURF_offset_dist1 = fit_polynom(offset_glass_points_dist1, alpha)
    print(f"SURF_offset_dist1 points size: {len(SURF_offset_dist1['points']['x'])} points")

    # dist 2
    print("\n=== Processing dist_2 ===")
    offset_glass_points_dist2, trimline_dist2 = offset_surface(SURF_glass, -dist_2, GLASS_TRIMLINE_POINTS, False)
    print(f"offset_glass_points_dist2 size: {len(offset_glass_points_dist2['x'])} points")
    
    SURF_offset_dist2 = fit_polynom(offset_glass_points_dist2, alpha)
    print(f"SURF_offset_dist2 points size: {len(SURF_offset_dist2['points']['x'])} points")
    
    # Middle channels with optimized function
    print("\n=== Creating Middle channels ===")
    ara_dist1_sf_point = find_normal_surface_optimized(SURF_normal2glass['sf'][0], trimline_dist1, dist_3, 0, 15, False)
    print(f"ara_dist1_sf_point size: {len(ara_dist1_sf_point['x'])} points")
    
    SURF_ara_dist1 = fit_polynom(ara_dist1_sf_point, alpha)
    print(f"SURF_ara_dist1 points size: {len(SURF_ara_dist1['points']['x'])} points")

    ara_dist2_sf_point = find_normal_surface_optimized(SURF_normal2glass['sf'][0], trimline_dist2, dist_3, 0, 15, False)
    print(f"ara_dist2_sf_point size: {len(ara_dist2_sf_point['x'])} points")
    
    SURF_ara_dist2 = fit_polynom(ara_dist2_sf_point, alpha)
    print(f"SURF_ara_dist2 points size: {len(SURF_ara_dist2['points']['x'])} points")
    
    # Cut top and bottom glass guide with optimized function
    print("\n=== Cutting top and bottom glass guide ===")
    cut_sf_point = find_normal_surface_optimized(SURF_glass['sf'][0], GLASS_TRIMLINE_POINTS, 1.5*dist_1, 1.5*dist_2, 15, False)
    print(f"cut_sf_point size: {len(cut_sf_point['x'])} points")
    
    SURF_cut = fit_polynom(cut_sf_point, alpha)
    print(f"SURF_cut points size: {len(SURF_cut['points']['x'])} points")

    # Surface to cut top of glass guide
    print("\n=== Creating surface to cut top of glass guide ===")
    offset_cut_points_1, _ = offset_surface(SURF_cut, -(len_1-dist_3), GLASS_TRIMLINE_POINTS, False)
    print(f"offset_cut_points_1 size: {len(offset_cut_points_1['x'])} points")
    
    SURF_offset_cut_1 = fit_polynom(offset_cut_points_1, alpha)
    print(f"SURF_offset_cut_1 points size: {len(SURF_offset_cut_1['points']['x'])} points")

    # Surface to cut bottom of glass guide
    print("\n=== Creating surface to cut bottom of glass guide ===")
    offset_cut_points_2, _ = offset_surface(SURF_cut, -(len_2-dist_3), GLASS_TRIMLINE_POINTS, False)
    print(f"offset_cut_points_2 size: {len(offset_cut_points_2['x'])} points")
    
    SURF_offset_cut_2 = fit_polynom(offset_cut_points_2, alpha)
    print(f"SURF_offset_cut_2 points size: {len(SURF_offset_cut_2['points']['x'])} points")

    # Cut glass guides
    print("\n=== Cutting glass guides ===")
    offset_dist1_updated_points = cut_glass_guide(SURF_offset_dist1, SURF_offset_cut_1, False)
    print(f"offset_dist1_updated_points size: {len(offset_dist1_updated_points['x'])} points")
    
    SURF_offset_dist1_updated = fit_polynom(offset_dist1_updated_points, alpha)
    print(f"SURF_offset_dist1_updated points size: {len(SURF_offset_dist1_updated['points']['x'])} points")
    
    offset_dist2_updated_points = cut_glass_guide(SURF_offset_dist2, SURF_offset_cut_2, False)
    print(f"offset_dist2_updated_points size: {len(offset_dist2_updated_points['x'])} points")
    
    SURF_offset_dist2_updated = fit_polynom(offset_dist2_updated_points, alpha)
    print(f"SURF_offset_dist2_updated points size: {len(SURF_offset_dist2_updated['points']['x'])} points")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(SURF_offset_dist1_updated['points']['x'], SURF_offset_dist1_updated['points']['y'], SURF_offset_dist1_updated['points']['z'], c='r', marker='.')
    ax.scatter(SURF_offset_dist2_updated['points']['x'], SURF_offset_dist2_updated['points']['y'], SURF_offset_dist2_updated['points']['z'], c='b', marker='.')
    #ax.scatter(normal_sf_point['x'], normal_sf_point['y'], normal_sf_point['z'], c='b', marker='.')
    #ax.scatter(GLASS_TRIMLINE_POINTS['x'], GLASS_TRIMLINE_POINTS['y'], GLASS_TRIMLINE_POINTS['z'], c='g', marker='o',s=10)
    ax.scatter(SURF_offset_normal2glass['points']['x'], SURF_offset_normal2glass['points']['y'], SURF_offset_normal2glass['points']['z'], c='y', marker='.')
    ax.scatter(SURF_ara_dist1['points']['x'], SURF_ara_dist1['points']['y'], SURF_ara_dist1['points']['z'], c='g', marker='.')
    ax.scatter(SURF_ara_dist2['points']['x'], SURF_ara_dist2['points']['y'], SURF_ara_dist2['points']['z'], c='g', marker='.')
    #ax.scatter(SURF_normal2glass['points']['x'], SURF_normal2glass['points']['y'], SURF_normal2glass['points']['z'], c='g', marker='.')
    #plt.show() 

    
    # Create 3D objects
    print("\n=== Creating 3D objects ===")
    GLASS_3D = surf_2_3D_object(SURF_glass, delta_glass, alpha, False)
    print(f"GLASS_3D size: {len(GLASS_3D['x'])} points")
    
    GLASS_GUIDE_OFFSET_2_3D = surf_2_3D_object(SURF_offset_dist2_updated, delta_guide, alpha, False)
    print(f"GLASS_GUIDE_OFFSET_2_3D size: {len(GLASS_GUIDE_OFFSET_2_3D['x'])} points")
    
    GLASS_GUIDE_OFFSET_1_3D = surf_2_3D_object(SURF_offset_dist1_updated, -delta_guide, alpha, False)
    print(f"GLASS_GUIDE_OFFSET_1_3D size: {len(GLASS_GUIDE_OFFSET_1_3D['x'])} points")
    
    GLASS_GUIDE_ARA_2_3D = surf_2_3D_object(SURF_ara_dist2, delta_guide, alpha, False)
    print(f"GLASS_GUIDE_ARA_2_3D size: {len(GLASS_GUIDE_ARA_2_3D['x'])} points")
    
    GLASS_GUIDE_ARA_1_3D = surf_2_3D_object(SURF_ara_dist1, -delta_guide, alpha, False)
    print(f"GLASS_GUIDE_ARA_1_3D size: {len(GLASS_GUIDE_ARA_1_3D['x'])} points")
    
    GLASS_GUIDE_NORMAL_3D = surf_2_3D_object(SURF_offset_normal2glass, delta_guide, alpha, False)
    print(f"GLASS_GUIDE_NORMAL_3D size: {len(GLASS_GUIDE_NORMAL_3D['x'])} points")

    # Create partial solid figures
    print("\n=== Creating partial solid figures ===")
    create_3D_partial_solid_figures(GLASS_3D, GLASS_GUIDE_OFFSET_2_3D,
                                   GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D,
                                   GLASS_GUIDE_ARA_1_3D, GLASS_GUIDE_NORMAL_3D)

    # Combine glass guide parts
    print("\n=== Combining glass guide parts ===")
    GLASS_GUIDE_3D = combine_guide(GLASS_GUIDE_OFFSET_2_3D,
                                  GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D,
                                  GLASS_GUIDE_ARA_1_3D, GLASS_GUIDE_NORMAL_3D, 1, False)
    print(f"GLASS_GUIDE_3D size: {len(GLASS_GUIDE_3D['x'])} points")

    # Create full solid figures
    print("\n=== Creating full solid figures ===")
    create_3D_full_solid_figures(GLASS_3D, GLASS_GUIDE_3D)

    # Create individual visualizations
    print("\n=== Creating individual visualizations ===")
    create_3D_glass(GLASS_3D)
    create_3D_glass_guide(GLASS_GUIDE_3D)
    
    # FreeCAD dosyalarını kaydet
    try:
        print("\n=== Saving to FreeCAD format ===")
        output_dir = 'output/freecad'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        #save_to_freecad(GLASS_3D, os.path.join(output_dir, "Cam.FCStd"))
            
        # Save individual glass guide parts
        #save_to_freecad(GLASS_GUIDE_OFFSET_1_3D, os.path.join(output_dir, "UstKanal.FCStd"))
        #save_to_freecad(GLASS_GUIDE_OFFSET_2_3D, os.path.join(output_dir, "AltKanal.FCStd"))
        #save_to_freecad(GLASS_GUIDE_ARA_1_3D, os.path.join(output_dir, "OrtaKanal1.FCStd"))
        #save_to_freecad(GLASS_GUIDE_ARA_2_3D, os.path.join(output_dir, "OrtaKanal2.FCStd"))
        #save_to_freecad(GLASS_GUIDE_NORMAL_3D, os.path.join(output_dir, "NormalKanal.FCStd"))
        
        # Save glass model
        
        # Cam kılavuzu modelini kaydet
        save_to_freecad(GLASS_GUIDE_3D, os.path.join(output_dir, "CamKilavuzu.FCStd"))
    except Exception as e:
        print(f"FreeCAD dışa aktarma hatası: {e}")
        print("FreeCAD formatında dışa aktarma yapılabilmesi için script FreeCAD Python yorumlayıcısıyla çalıştırılmalıdır.")
    
    print("\n=== Process completed successfully ===")

if __name__ == "__main__":
    main() 