# funkt noch nicht richtig!!
# https://qgis.org/pyqgis/master/analysis/QgsRasterCalculator.html
# https://gis.stackexchange.com/questions/218835/raster-calculation-in-qgis-using-python-script

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

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

print(layer_list)
#print(vector_layer)

entries = []
i = 0
for layer in layer_list:
    bohLayer = layer_list[i]
    # Define band1
    boh1 = QgsRasterCalculatorEntry()
    boh1.ref = "EFI_Forest_WGS@1"
    boh1.raster = bohLayer
    boh1.bandNumber = 1
    entries.append( boh1 )
    
# Process calculation with input extent and resolution
    calc = QgsRasterCalculator( '("EFI_Forest_WGS@1"/100)*layer', 
                            '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/FRM/test.gif', 
                            'GTiff',
                            bohLayer.extent(), 
                            bohLayer.width(), 
                            bohLayer.height(), 
                            entries )

    calc.processCalculation()
    print(layer,' calculated')