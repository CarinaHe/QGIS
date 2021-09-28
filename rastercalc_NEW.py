from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

layer_list_rc=iface.mapCanvas().layers()

i=0

vector_layer = ""

while len(layer_list_rc)>i:
    layerType = layer_list_rc[i].type()
              
    if layerType == QgsMapLayer.VectorLayer:
       vector_layer=layer_list_rc[i]
       layer_list_rc.pop(i)
       continue
    i+=1

print(layer_list_rc)

print(vector_layer)

for layer in layer_list_rc:
    zoneStat = QgsZonalStatistics (vector_layer, layer, layer.name(), 1, QgsZonalStatistics.Median)
    zoneStat.calculateStatistics(None)
    print(layer, 'processed')