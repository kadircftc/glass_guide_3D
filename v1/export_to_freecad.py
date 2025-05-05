#!/usr/bin/env python

"""
v1 tarafından oluşturulan 3D modelleri FreeCAD formatında kaydetmek için script.
Bu script, FreeCAD Python API'sini kullanarak 3D modelleri hem FCStd hem de STEP formatında kaydeder.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# FreeCAD yolunu burada tanımlayın - Windows için örnek
# Kendi sisteminize göre bu yolu değiştirin
FREECAD_PATH = r"C:\Program Files\FreeCAD\bin"
if FREECAD_PATH not in sys.path:
    sys.path.append(FREECAD_PATH)

if os.name == 'nt':  # Windows işletim sistemi kontrolü
    try:
        os.add_dll_directory(FREECAD_PATH)
    except (AttributeError, FileNotFoundError):
        print("DLL dizini eklenemedi, devam ediliyor...")

# Ana dizini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import FreeCAD
    import Part
    FREECAD_LOADED = True
    print("FreeCAD modülleri başarıyla yüklendi.")
except ImportError as e:
    FREECAD_LOADED = False
    print(f"FreeCAD modülleri yüklenemedi: {e}")
    print("FreeCAD'in yüklü olduğundan ve doğru Python sürümünü kullandığınızdan emin olun.")
    print("Bu script FreeCAD'in Python yorumlayıcısı ile çalıştırılmalıdır.")
    sys.exit(1)

def mesh_to_solid(vertices, faces):
    """Mesh verilerini FreeCAD solid nesnesine dönüştürür."""
    try:
        # Yüzeyler oluştur
        mesh_faces = []
        for face in faces:
            v1, v2, v3 = face
            mesh_faces.append([vertices[v1], vertices[v2], vertices[v3]])
        
        # Mesh nesnesini oluştur
        mesh = FreeCAD.Mesh.Mesh(mesh_faces)
        
        # Mesh'ten şekil oluştur
        shape = Part.Shape()
        shape.makeShapeFromMesh(mesh.Topology, 0.1)
        
        # Kapalı şekilden solid oluştur
        if shape.isClosed():
            solid = Part.makeSolid(shape)
            return solid
        else:
            print("Uyarı: Mesh kapalı değil, solid oluşturulamadı.")
            return shape
    except Exception as e:
        print(f"Mesh'ten solid oluşturma hatası: {e}")
        return None

def save_3d_object_to_freecad(obj_3d, name, output_dir):
    """3D nesne verilerini FreeCAD formatında kaydeder."""
    try:
        # Dizin oluştur
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # FreeCAD belgesi oluştur
        doc = FreeCAD.newDocument(name)
        
        # Nokta ve yüz verilerini hazırla
        points = []
        for i in range(len(obj_3d['x'])):
            points.append(FreeCAD.Vector(obj_3d['x'][i], obj_3d['y'][i], obj_3d['z'][i]))
        
        faces = obj_3d['shp'].simplices
        
        # Mesh oluştur
        mesh_faces = []
        for face in faces:
            mesh_faces.append([points[face[0]], points[face[1]], points[face[2]]])
        
        mesh_obj = FreeCAD.Mesh.Mesh(mesh_faces)
        mesh_feature = doc.addObject("Mesh::Feature", f"{name}_Mesh")
        mesh_feature.Mesh = mesh_obj
        
        # Mesh'i solide dönüştürmeyi dene
        try:
            solid = mesh_to_solid(points, faces)
            if solid:
                solid_obj = doc.addObject("Part::Feature", f"{name}_Solid")
                solid_obj.Shape = solid
        except Exception as e:
            print(f"Uyarı: Solid dönüştürme hatası - {e}")
        
        # Belgeyi yeniden hesapla
        doc.recompute()
        
        # FCStd formatında kaydet
        fcstd_file = os.path.join(output_dir, f"{name}.FCStd")
        doc.saveCopy(fcstd_file)
        print(f"FreeCAD dosyası kaydedildi: {fcstd_file}")
        
        # STEP formatında kaydet
        try:
            step_file = os.path.join(output_dir, f"{name}.stp")
            Part.export(doc.Objects, step_file)
            print(f"STEP dosyası kaydedildi: {step_file}")
        except Exception as e:
            print(f"STEP dışa aktarma hatası: {e}")
        
        return True
    except Exception as e:
        print(f"FreeCAD'e kaydetme hatası: {e}")
        return False

def main():
    """Ana fonksiyon"""
    # v1 modüllerini import et
    try:
        from combine_guide import combine_guide
        from create_3D_full_solid_figures import create_3D_full_solid_figures
        from create_3D_glass import create_3D_glass
        from create_3D_glass_guide import create_3D_glass_guide
        from create_3D_partial_solid_figures import \
            create_3D_partial_solid_figures
        from cut_glass_guide import cut_glass_guide
        from find_normal_surface import find_normal_surface
        from fit_polynom import fit_polynom
        from main import main as run_main
        from offset_surface import offset_surface
        from read_dat_file import read_dat_file
        from surf_2_3D_object import surf_2_3D_object
    except ImportError as e:
        print(f"v1 modülleri içe aktarılamadı: {e}")
        sys.exit(1)
    
    print("\n=== 3D modelleri oluşturuluyor ===")
    
    # Veri dosyalarını oku
    print("Veri dosyaları okunuyor...")
    GLASS_POINTS = read_dat_file('../matlab/glass2.5kpoint.dat')
    GLASS_GUIDE_POINTS = read_dat_file('../matlab/glass_guide_wall2.5kpoints.dat')
    GLASS_TRIMLINE_POINTS = read_dat_file('../matlab/glass_trimline.dat')
    
    # Ana parametreler
    delta_glass = 3.8  # cam kalınlığı
    delta_guide = 0.1  # kanal kalınlığı
    dist_1 = 3.5  # dış kanala mesafe
    dist_2 = 13.1 + delta_glass  # iç kanala mesafe
    dist_3 = 6.2  # karşı kanala mesafe
    len_1 = 13.3 - delta_guide  # dış kanal uzunluğu
    len_2 = 28.8 - delta_guide  # iç kanal uzunluğu
    alpha = 4  # polinom uydurmada yüzey sınırlarını belirleyen parametre
    
    # Polinom yüzeyi uydur
    print("Polinom yüzeyi uyduruluyor...")
    SURF_glass = fit_polynom(GLASS_POINTS, alpha, False)
    
    # Normal yüzeyi bul
    print("Normal yüzey hesaplanıyor...")
    normal_sf_point = find_normal_surface(SURF_glass['sf'][0], GLASS_TRIMLINE_POINTS, dist_1, dist_2, 100, False)
    SURF_normal2glass = fit_polynom(normal_sf_point, alpha, False)
    
    # Ofset yüzey oluştur
    print("Ofset yüzey oluşturuluyor...")
    offset_normal2glass_points, _ = offset_surface(SURF_normal2glass, dist_3, GLASS_TRIMLINE_POINTS, False)
    SURF_offset_normal2glass = fit_polynom(offset_normal2glass_points, alpha)
    
    # dist_1 için ofset yüzey
    offset_glass_points_dist1, trimline_dist1 = offset_surface(SURF_glass, dist_1, GLASS_TRIMLINE_POINTS, False)
    SURF_offset_dist1 = fit_polynom(offset_glass_points_dist1, alpha)
    
    # dist_2 için ofset yüzey
    offset_glass_points_dist2, trimline_dist2 = offset_surface(SURF_glass, -dist_2, GLASS_TRIMLINE_POINTS, False)
    SURF_offset_dist2 = fit_polynom(offset_glass_points_dist2, alpha)
    
    # Orta kanallar
    ara_dist1_sf_point = find_normal_surface(SURF_normal2glass['sf'][0], trimline_dist1, dist_3, 0, 100, False)
    SURF_ara_dist1 = fit_polynom(ara_dist1_sf_point, alpha)
    
    ara_dist2_sf_point = find_normal_surface(SURF_normal2glass['sf'][0], trimline_dist2, dist_3, 0, 100, False)
    SURF_ara_dist2 = fit_polynom(ara_dist2_sf_point, alpha)
    
    # Cam kılavuzunun üst ve alt kısmını kes
    cut_sf_point = find_normal_surface(SURF_glass['sf'][0], GLASS_TRIMLINE_POINTS, 1.5*dist_1, 1.5*dist_2, 100, False)
    SURF_cut = fit_polynom(cut_sf_point, alpha)
    
    # Cam kılavuzunun üst kısmını kesmek için yüzey
    offset_cut_points_1, _ = offset_surface(SURF_cut, -(len_1-dist_3), GLASS_TRIMLINE_POINTS, False)
    SURF_offset_cut_1 = fit_polynom(offset_cut_points_1, alpha)
    
    # Cam kılavuzunun alt kısmını kesmek için yüzey
    offset_cut_points_2, _ = offset_surface(SURF_cut, -(len_2-dist_3), GLASS_TRIMLINE_POINTS, False)
    SURF_offset_cut_2 = fit_polynom(offset_cut_points_2, alpha)
    
    # Cam kılavuzlarını kes
    offset_dist1_updated_points = cut_glass_guide(SURF_offset_dist1, SURF_offset_cut_1, False)
    SURF_offset_dist1_updated = fit_polynom(offset_dist1_updated_points, alpha)
    
    offset_dist2_updated_points = cut_glass_guide(SURF_offset_dist2, SURF_offset_cut_2, False)
    SURF_offset_dist2_updated = fit_polynom(offset_dist2_updated_points, alpha)
    
    # 3D nesneleri oluştur
    print("3D nesneler oluşturuluyor...")
    GLASS_3D = surf_2_3D_object(SURF_glass, delta_glass, alpha, False)
    
    GLASS_GUIDE_OFFSET_2_3D = surf_2_3D_object(SURF_offset_dist2_updated, delta_guide, alpha, False)
    GLASS_GUIDE_OFFSET_1_3D = surf_2_3D_object(SURF_offset_dist1_updated, -delta_guide, alpha, False)
    GLASS_GUIDE_ARA_2_3D = surf_2_3D_object(SURF_ara_dist2, delta_guide, alpha, False)
    GLASS_GUIDE_ARA_1_3D = surf_2_3D_object(SURF_ara_dist1, -delta_guide, alpha, False)
    GLASS_GUIDE_NORMAL_3D = surf_2_3D_object(SURF_offset_normal2glass, delta_guide, alpha, False)
    
    # Cam kılavuzu parçalarını birleştir
    print("Cam kılavuzu parçaları birleştiriliyor...")
    GLASS_GUIDE_3D = combine_guide(GLASS_GUIDE_OFFSET_2_3D,
                                  GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D,
                                  GLASS_GUIDE_ARA_1_3D, GLASS_GUIDE_NORMAL_3D, 1, False)
    
    # FreeCAD'e kaydet
    print("\n=== 3D modeller FreeCAD formatına kaydediliyor ===")
    output_dir = '../output/freecad'
    
    # Cam modelini kaydet
    print("Cam modeli kaydediliyor...")
    save_3d_object_to_freecad(GLASS_3D, "Cam", output_dir)
    
    # Cam kılavuzu modelini kaydet
    print("Cam kılavuzu modeli kaydediliyor...")
    save_3d_object_to_freecad(GLASS_GUIDE_3D, "CamKilavuzu", output_dir)
    
    # Parça modelleri kaydet
    print("Parça modelleri kaydediliyor...")
    save_3d_object_to_freecad(GLASS_GUIDE_OFFSET_1_3D, "UstKanal", output_dir)
    save_3d_object_to_freecad(GLASS_GUIDE_OFFSET_2_3D, "AltKanal", output_dir)
    save_3d_object_to_freecad(GLASS_GUIDE_ARA_1_3D, "OrtaKanal1", output_dir)
    save_3d_object_to_freecad(GLASS_GUIDE_ARA_2_3D, "OrtaKanal2", output_dir)
    save_3d_object_to_freecad(GLASS_GUIDE_NORMAL_3D, "NormalKanal", output_dir)
    
    # Birleşik model oluştur ve kaydet
    print("Birleşik model oluşturuluyor...")
    
    # Yeni belge oluştur
    doc = FreeCAD.newDocument("CamVeKilavuz")
    
    # Cam ve kılavuz için mesh yüzleri oluştur
    glass_points = []
    for i in range(len(GLASS_3D['x'])):
        glass_points.append(FreeCAD.Vector(GLASS_3D['x'][i], GLASS_3D['y'][i], GLASS_3D['z'][i]))
    
    glass_faces = []
    for face in GLASS_3D['shp'].simplices:
        glass_faces.append([glass_points[face[0]], glass_points[face[1]], glass_points[face[2]]])
    
    guide_points = []
    for i in range(len(GLASS_GUIDE_3D['x'])):
        guide_points.append(FreeCAD.Vector(GLASS_GUIDE_3D['x'][i], GLASS_GUIDE_3D['y'][i], GLASS_GUIDE_3D['z'][i]))
    
    guide_faces = []
    for face in GLASS_GUIDE_3D['shp'].simplices:
        guide_faces.append([guide_points[face[0]], guide_points[face[1]], guide_points[face[2]]])
    
    # Mesh nesneleri oluştur ve belgeye ekle
    glass_mesh = FreeCAD.Mesh.Mesh(glass_faces)
    glass_obj = doc.addObject("Mesh::Feature", "Cam_Mesh")
    glass_obj.Mesh = glass_mesh
    
    guide_mesh = FreeCAD.Mesh.Mesh(guide_faces)
    guide_obj = doc.addObject("Mesh::Feature", "CamKilavuzu_Mesh")
    guide_obj.Mesh = guide_mesh
    
    # Mesh'leri solide dönüştürmeyi dene
    try:
        glass_solid = mesh_to_solid(glass_points, GLASS_3D['shp'].simplices)
        if glass_solid:
            glass_solid_obj = doc.addObject("Part::Feature", "Cam_Solid")
            glass_solid_obj.Shape = glass_solid
        
        guide_solid = mesh_to_solid(guide_points, GLASS_GUIDE_3D['shp'].simplices)
        if guide_solid:
            guide_solid_obj = doc.addObject("Part::Feature", "CamKilavuzu_Solid")
            guide_solid_obj.Shape = guide_solid
    except Exception as e:
        print(f"Solid dönüştürme hatası: {e}")
    
    # Belgeyi yeniden hesapla
    doc.recompute()
    
    # Birleşik belgeyi kaydet
    birlesik_fcstd = os.path.join(output_dir, "CamVeKilavuz.FCStd")
    doc.saveCopy(birlesik_fcstd)
    print(f"Birleşik model kaydedildi: {birlesik_fcstd}")
    
    # STEP olarak dışa aktar
    try:
        birlesik_step = os.path.join(output_dir, "CamVeKilavuz.stp")
        Part.export(doc.Objects, birlesik_step)
        print(f"Birleşik STEP dosyası kaydedildi: {birlesik_step}")
    except Exception as e:
        print(f"Birleşik STEP dışa aktarma hatası: {e}")
    
    print("\n=== İşlem tamamlandı ===")
    print(f"Tüm dosyalar '{output_dir}' dizinine kaydedildi.")

if __name__ == "__main__":
    main() 