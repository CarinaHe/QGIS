# Carina Heiling
# 2021-08-21

pygis_dir = "/home/c/Schreibtisch/GIS/pygis/"
QgsCoordinateReferenceSystem("EPSG:32633")
SL = []


def get_list(layer):
    for i in range(0, layer.featureCount()):
        feat = layer.getFeature(i)
        SL.append((feat[8]/feat[18]))   # 1=Bezirkname, 2=sea-level
        


layer1 = iface.addRasterLayer(f'{pygis_dir}Wien_Bild_klein.grib2', 'Bild')
layer2 = iface.addRasterLayer(f'{pygis_dir}DEM_wien.tif', 'DEM')
layer3 = iface.addVectorLayer(
    f'{pygis_dir}zonenstatistik.shp',
    'Bezirke',
    'ogr')

layer3.loadNamedStyle(f'{pygis_dir}stil_shp.qml')
get_list(layer3)
SL.sorted(key=lambda x:x[1])
print(SL)

