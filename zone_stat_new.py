
from qgis.analysis import QgsZonalStatistics


layer_list=iface.mapCanvas().layers()

i=0
raster_layer = ""
vector_layer = ""

while len(layer_list)>i:
    layerType = layer_list[i].type()
    layerName = layer_list[i].name()
           
    if layerName == 'EFI_Forest_WGS':
        raster_layer=layer_list[i]
        print(layer_list.pop(i))
        continue
        
    elif layerType == QgsMapLayer.VectorLayer:
        vector_layer=layer_list[i]
        print(layer_list.pop(i))
        continue
    i+=1


print('Liste:',layer_list)
print('rasterlayer:', raster_layer)
print('vektorlayer:', vector_layer)


zoneStat = QgsZonalStatistics (vector_layer, raster_layer, 'FS_', 1, QgsZonalStatistics.Mean)
zoneStat.calculateStatistics(None)


for layer in layer_list:
    zoneStat = QgsZonalStatistics (vector_layer, layer, layer.name(), 1, QgsZonalStatistics.Median)
    zoneStat.calculateStatistics(None)
    print(layer, 'processed')

    
