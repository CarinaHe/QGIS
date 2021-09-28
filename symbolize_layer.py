# this is a copy of: https://data.library.virginia.edu/how-to-apply-a-graduated-color-symbology-to-a-layer-using-python-for-qgis-3/


FRM_dir = "/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/FRM/"
join_layer = iface.addVectorLayer(f'{FRM_dir}NUTS_aktuell.shp', "NUTS", 'ogr')



target_field = 'RP_Pa'

def apply_graduated_symbology():
    """Creates Symbology for each value in range of values. 
        Values are # of patients per zip code.
        Hard codes min value, max value, symbol (color), and label for each range of 
        values. Then QgsSymbolRenderer takes field from attribute table and item from 
        myRangeList and applies them to join_layer. Color values are hex codes, 
        in a graduated fashion from light pink to black depending on intensity"""
        
    myRangeList = []

    symbol = QgsSymbol.defaultSymbol(join_layer.geometryType())     
    symbol.setColor(QColor("white"))                              
    myRange = QgsRendererRange(0, 0.25, symbol, '0-25%')                   
    myRangeList.append(myRange)                                     

    symbol = QgsSymbol.defaultSymbol(join_layer.geometryType())
    symbol.setColor(QColor("yellow"))
    myRange = QgsRendererRange(0.251, 0.50, symbol, '25-50%')
    myRangeList.append(myRange)
    
    symbol = QgsSymbol.defaultSymbol(join_layer.geometryType())     
    symbol.setColor(QColor("orange"))                              
    myRange = QgsRendererRange(0.501, 0.75, symbol, '50-75%%')                   
    myRangeList.append(myRange)                                     

    symbol = QgsSymbol.defaultSymbol(join_layer.geometryType())
    symbol.setColor(QColor("red"))
    myRange = QgsRendererRange(0.751, 1, symbol, '75-100%')
    myRangeList.append(myRange)

    myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
    myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)               

    join_layer.setRenderer(myRenderer)                                  
    
    print(f"Graduated color scheme applied")

apply_graduated_symbology()

