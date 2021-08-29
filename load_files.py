from pathlib import Path
import sys

FRM_dir = "/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/FRM/"
file_path ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/SDM_Europe_SUSTREE'
source_dir = Path(file_path)

files = source_dir.iterdir()
files = source_dir.glob('*81_00_85ens.tif')

layer_list=[]

def open_tree_files():
    for file in files:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('2')
        name=name[:name_index]
        layer_list.append(iface.addRasterLayer(file_path+'/'+name+'2081_00_85ens.tif', name))
              
    
open_tree_files()
layer_list.append(iface.addVectorLayer(f'{FRM_dir}NUTS2.shp', 'NUTS2', 'ogr'))
layer_list.append(iface.addRasterLayer(f'{FRM_dir}EFI_Forest_WGS.tif', 'Forestshare'))

for layer in QgsProject.instance().mapLayers().values():
    layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(4326))




