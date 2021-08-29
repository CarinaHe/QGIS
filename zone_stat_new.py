from qgis.analysis import QgsZonalStatistics


layer_list=iface.mapCanvas().layers()

i=0

for layer in layer_list:
    layerType = layer.type()
    layerName = layer.name()
           
    if layerName == 'EFI_Forest_WGS':
        raster_layer=layer_list[i]
        layer_list.pop(i)
        
    elif layerType == QgsMapLayer.VectorLayer:
        vector_layer=layer_list[i]
        layer_list.pop(i)
    i+=1

print('Liste:',layer_list)
# layers = QgsProject.instance().mapLayersByName('EFI_Forest_WGS')
print('vektorlayer:',vector_layer)
print('rasterlayer:', raster_layer)

zoneStat = QgsZonalStatistics (vector_layer, raster_layer, 'FS_', 1, QgsZonalStatistics.Mean)
zoneStat.calculateStatistics(None)

c=1
for layer in layer_list:
    zoneStat = QgsZonalStatistics (vector_layer, layer, layer.name(), 1, QgsZonalStatistics.Median)
    zoneStat.calculateStatistics(None)
    c+=1
    print(layer, 'processed')

    
