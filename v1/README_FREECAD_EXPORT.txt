======================================================================
FREECAD 3D MODEL DÖNÜŞTÜRME KILAVUZU
======================================================================

Bu dosya, v1 tarafından oluşturulan 3D modelleri FreeCAD formatına
dönüştürmek için gerekli adımları açıklamaktadır.

ÖN KOŞULLAR:
------------
- FreeCAD (0.19 veya üzeri sürüm) yüklü olmalıdır
- Python 3.x
- NumPy, Matplotlib, SciPy bilimsel Python kütüphaneleri

KULLANIM:
---------
1. export_to_freecad.py dosyasını v1 klasörü içine yerleştirin
2. FreeCAD'in Python yorumlayıcısı ile scripti çalıştırın:

   Windows için:
   "C:\Program Files\FreeCAD\bin\freecadcmd.exe" -c export_to_freecad.py
   veya
   "C:\Program Files\FreeCAD\bin\python.exe" export_to_freecad.py

   Linux için:
   freecadcmd -c export_to_freecad.py

   Mac için:
   /Applications/FreeCAD.app/Contents/MacOS/FreeCAD export_to_freecad.py

3. Script çalıştıktan sonra, output/freecad klasöründe aşağıdaki 
   dosyaları bulacaksınız:

   - Cam.FCStd             (Cam modeli)
   - Cam.stp               (Cam modeli - STEP formatında)
   - CamKilavuzu.FCStd     (Cam kılavuzu modeli)
   - CamKilavuzu.stp       (Cam kılavuzu modeli - STEP formatında)
   - CamVeKilavuz.FCStd    (Birleşik model)
   - CamVeKilavuz.stp      (Birleşik model - STEP formatında)
   - UstKanal.FCStd        (Üst kanal parçası)
   - AltKanal.FCStd        (Alt kanal parçası)
   - OrtaKanal1.FCStd      (Orta kanal parçası 1)
   - OrtaKanal2.FCStd      (Orta kanal parçası 2)
   - NormalKanal.FCStd     (Normal kanal parçası)

NOT: FREECAD_PATH değişkenini kendi sisteminize göre düzenlemeniz 
gerekebilir. Bu değişken export_to_freecad.py dosyasının başında 
tanımlanmıştır.

SORUN GİDERME:
--------------
- FreeCAD modülünü içe aktarma hatası alıyorsanız, FREECAD_PATH 
  değişkenini kendi sisteminize göre düzenleyin.
- Script FreeCAD'in Python yorumlayıcısı ile çalıştırılmalıdır, 
  normal Python yorumlayıcısı ile çalıştırılmaz.
- Mesh'i solide dönüştürme hatası alınabilir, bu durumda modeller 
  mesh olarak kaydedilecektir.

====================================================================== 