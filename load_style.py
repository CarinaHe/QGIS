# stilfile laden
# geht nicht!


FRM_dir = "/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/FRM/"
layer = iface.addVectorLayer(f'{FRM_dir}NUTS_aktuell.shp', 'NUTS2', 'ogr')

print (layer)

layer.loadNamedStyle('/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/legends/NEW_Legend_LS_r.qml')
layer.triggerRepaint()
    

print ('styling done')