
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

layer_list=iface.mapCanvas().layers()

i=0
input_raster1 = ""
vector_layer = ""

while len(layer_list)>i:
    layerType = layer_list[i].type()
    layerName = layer_list[i].name()
           
    if layerName == 'EFI_Forest_WGS':
        input_raster1=layer_list[i]
        layer_list.pop(i)
        continue
        
    elif layerType == QgsMapLayer.VectorLayer:
        vector_layer=layer_list[i]
        layer_list.pop(i)
        continue
    i+=1

print(layer_list)
print(input_raster1)
print(vector_layer)

try:

    for layer in layer_list:
        input_raster2 = layer
        fileName = layer.name()
               
        entries = []
            # Define Layer1
        boh1 = QgsRasterCalculatorEntry()
        boh1.ref = 'boh@1'
        boh1.raster = input_raster1
        boh1.bandNumber = 1
        entries.append( boh1 )
            
            # Define Layer2
        boh2 = QgsRasterCalculatorEntry()
        boh2.ref = 'boh@2'
        boh2.raster = input_raster2
        boh2.bandNumber = 1
        entries.append( boh2 )
            
        outPath = '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/rastercalc/'+fileName[:4]+'_rc.tif'    
            # Process calculation with input extent and resolution
        calc = QgsRasterCalculator( "('boh@1'/100)*('boh@2')", outPath,
                                        'GTiff', input_raster1.extent(),
                                        input_raster1.width(), input_raster1.height(), entries )
        calc.processCalculation()
            
           
        print(layer,' calculated')

except:
    
    print("Missing layers")
