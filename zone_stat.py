from qgis.analysis import QgsZonalStatistics

layer_list=iface.mapCanvas().layers()

i=0

for layer in layer_list:
    layerType = layer.type()
    if layerType == QgsMapLayer.VectorLayer:
        vector_layer=layer_list[i]
        layer_list.pop(i)
    i+=1

print(layer_list)

print(vector_layer)

c=1
for layer in layer_list:
    zoneStat = QgsZonalStatistics (vector_layer, layer, layer.name(), 1, QgsZonalStatistics.Median)
    zoneStat.calculateStatistics(None)
    print(layer, 'processed')
    c+=1
