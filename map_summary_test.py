# with the help of: https://gis.stackexchange.com/questions/411254/locking-layer-styles-in-qgis-print-layout-using-pyqgis?noredirect=1#comment667915_411254

from pathlib import Path
import sys


file_path ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/legends/'
source_dir = Path(file_path)

files = source_dir.iterdir()

print(files)

for file in files:
    iface.addVectorLayer('/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/FRM/NUTS_TEST.shp', 'NUTS_TEST', 'ogr')
    name = str(file)[len(file_path):]
    name_index = name.index('.')
    name=name[:name_index]
    print(name)
    print(str(file))
   
    project = QgsProject.instance()
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(name)
    project.layoutManager().addLayout(layout)
    print('layout manager geladen')
    layer_list = iface.mapCanvas().layers()
    
    layer=layer_list[0]

    
    layer.loadNamedStyle(str(file))
    #layer.triggerRepaint()
    print('layout geändert')

    #map:
    map1 = QgsLayoutItemMap(layout)
    map1.attemptMove(QgsLayoutPoint(55,35, QgsUnitTypes.LayoutMillimeters))
    map1.attemptResize(QgsLayoutSize(240, 240, QgsUnitTypes.LayoutMillimeters))
    map1.setExtent(layer.extent())
    map1.setLayers([layer])
    map1.setScale(10000000)
    layout.addLayoutItem(map1)

    map1.storeCurrentLayerStyles()
    map1.setKeepLayerSet(True)
    map1.setKeepLayerStyles(True)
    print('map')
    # title:

    title = QgsLayoutItemLabel(layout)
    name_title = name.replace("_", " ")
    title.setText(name_title)
    title.setFont(QFont('Arial', 24))
    title.adjustSizeToText()
    layout.addLayoutItem(title)
    title.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutMillimeters))

    # legend:
    legend = QgsLayoutItemLegend(layout)
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(10, 40, QgsUnitTypes.LayoutMillimeters))

    # scalebar:
    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(2)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitsPerSegment(250)
    scalebar.setLinkedMap(map1)
    scalebar.setUnitLabel('km')
    scalebar.setFont(QFont('Arial', 14))
    scalebar.update()
    layout.addLayoutItem(scalebar)
    scalebar.attemptMove(QgsLayoutPoint(200, 20, QgsUnitTypes.LayoutMillimeters))
    print('scalebar')
    manager = project.layoutManager()
    layout = manager.layoutByName(name)
    exporter = QgsLayoutExporter(layout)
    fn = '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/maps/'+name+'.pdf'
#exporter.exportToImage(fn, QgsLayoutExporter.ImageExportSettings())
    exporter.exportToPdf(fn, QgsLayoutExporter.PdfExportSettings())
    project.removeMapLayers( layer_list[0])