# with the help of: https://gis.stackexchange.com/questions/411254/locking-layer-styles-in-qgis-print-layout-using-pyqgis?noredirect=1#comment667915_411254

project = QgsProject.instance()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName('Carina_atlas')
project.layoutManager().addLayout(layout)

layer_list = iface.mapCanvas().layers()
layer = layer_list[0]

# title:

title = QgsLayoutItemLabel(layout)
title.setText("Riskvalue of each Species")
title.setFont(QFont('Arial', 24))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutMillimeters))

#1. map
map1 = QgsLayoutItemMap(layout)
map1.attemptMove(QgsLayoutPoint(160,5, QgsUnitTypes.LayoutMillimeters))
map1.attemptResize(QgsLayoutSize(120,120, QgsUnitTypes.LayoutMillimeters))
map1.setExtent(layer.extent())
map1.setLayers([layer])
# map1.setScale(25000000)
layout.addLayoutItem(map1)


map1.storeCurrentLayerStyles()
map1.setKeepLayerSet(True)
map1.setKeepLayerStyles(True)

#2. map

map2 = QgsLayoutItemMap(layout)
map2.attemptMove(QgsLayoutPoint(20,120, QgsUnitTypes.LayoutMillimeters))
map2.attemptResize(QgsLayoutSize(120,120, QgsUnitTypes.LayoutMillimeters))


layer.loadNamedStyle('/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/legends/NEW_Legend_RP.qml')
layer.triggerRepaint()
map2.setExtent(layer.extent())
map2.setLayers([layer])
layout.addLayoutItem(map2)

map2.storeCurrentLayerStyles()
map2.setKeepLayerSet(True)
map2.setKeepLayerStyles(True)

#3. map

map3 = QgsLayoutItemMap(layout)
map3.attemptMove(QgsLayoutPoint(1160,120, QgsUnitTypes.LayoutMillimeters))
map3.attemptResize(QgsLayoutSize(120,120, QgsUnitTypes.LayoutMillimeters))


layer.loadNamedStyle('/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/legends/NEW_Legend_PS.qml')
layer.triggerRepaint()
map3.setExtent(layer.extent())
map3.setLayers([layer])
layout.addLayoutItem(map3)

map3.storeCurrentLayerStyles()
map3.setKeepLayerSet(True)
map3.setKeepLayerStyles(True)