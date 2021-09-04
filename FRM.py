# Carina Heiling
# 2021_09_01

from pathlib import Path
import sys
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.PyQt.QtCore import QVariant


FRM_dir = "/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/FRM/"
file_path ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/SDM_Europe_SUSTREE'
source_dir = Path(file_path)
file_pathRC ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/output'
source_dirRC = Path(file_pathRC)

filesFuture = source_dir.iterdir()
filesFuture = source_dir.glob('*81_00_85ens.tif')
filesPast1 = source_dir.iterdir()
filesPast1 = source_dir.glob('*1961_90ens.tif')
filesPast2 = source_dir.iterdir()
filesPast2 = source_dir.glob('*1961_90_ens.tif')
filesRC = source_dirRC.iterdir()
filesRC = source_dirRC.glob('R_*.tif')

layer_list_future=[]
layer_list_past=[]
layer_list=[]
layer_list_rc = []

def open_tree_files_future():
    for file in filesFuture:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('2')
        name=name[:name_index]
        layer_list_future.append(iface.addRasterLayer(file_path+'/'+name+'2081_00_85ens.tif', 'F_'+name))
       
        
def open_tree_files_past():
    for file in filesPast1:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('1')
        name=name[:name_index]
        layer_list_past.append(iface.addRasterLayer(file_path+'/'+name+'1961_90ens.tif', 'P_'+name)) 
       
    
    for file in filesPast2:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('1')
        name=name[:name_index]
        layer_list_past.append(iface.addRasterLayer(file_path+'/'+name+'1961_90_ens.tif', 'P_'+name)) 
        
def open_files_setting():
    layer_list.append(iface.addVectorLayer(f'{FRM_dir}NUTS2.shp', 'NUTS2', 'ogr'))
    layer_list.append(iface.addRasterLayer(f'{FRM_dir}EFI_Forest_WGS.tif', 'EFI_Forest_WGS'))

    for layer in QgsProject.instance().mapLayers().values():
        layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(4326))
    
        
def rastercalc():
    input_raster1=layer_list[1]
    for layer in layer_list_future:
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
            
        outPath = '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/output/R_'+fileName[:6]+'.tif'    
            # Process calculation with input extent and resolution
        calc = QgsRasterCalculator( "('boh@1'/100)*(1000-'boh@2')", outPath,
                                        'GTiff', input_raster1.extent(),
                                        input_raster1.width(), input_raster1.height(), entries )
        calc.processCalculation()
            
           
        print(layer,' calculated')
        

def open_rc_layer():
    for file in filesRC:
        name = str(file)[len(file_pathRC)+1:]
        layer_list_rc.append(iface.addRasterLayer(file_pathRC+'/'+name, name))
        
          
def zone_stat():
    zoneStat = QgsZonalStatistics (layer_list[0], layer_list[1], 'FS_', 1, QgsZonalStatistics.Mean)
    zoneStat.calculateStatistics(None)

    for layer in layer_list_rc:
        zoneStat = QgsZonalStatistics (layer_list[0], layer, layer.name(), 1, QgsZonalStatistics.Median)
        zoneStat.calculateStatistics(None)
        print(layer, 'processed')
        
    for layer in layer_list_future:
        zoneStat = QgsZonalStatistics (layer_list[0], layer, layer.name(), 1, QgsZonalStatistics.Median)
        zoneStat.calculateStatistics(None)
        print(layer, 'processed')
        
    for layer in layer_list_past:
        zoneStat = QgsZonalStatistics (layer_list[0], layer, layer.name(), 1, QgsZonalStatistics.Median)
        zoneStat.calculateStatistics(None)
        print(layer, 'processed')
    

def delete_layer():
    
    QgsProject.instance().removeMapLayer(layer_list[1])
    
    for layer in layer_list_future:
        QgsProject.instance().removeMapLayer(layer)
   
    for layer in layer_list_past:
        QgsProject.instance().removeMapLayer(layer)
        
    for layer in layer_list_rc:
        QgsProject.instance().removeMapLayer(layer)


def fieldcalc():
    work_layer = layer_list[0]
    work_layer.dataProvider().addAttributes([QgsField("PS_Fs", QVariant.Double), 
                                            QgsField("PS_Ps", QVariant.Double),
                                            QgsField("PS_Pa", QVariant.Double),
                                            QgsField("LS_Fs", QVariant.Double), 
                                            QgsField("LS_Ps", QVariant.Double),
                                            QgsField("LS_Pa", QVariant.Double),
                                            QgsField("Risk_Fs", QVariant.Double), 
                                            QgsField("Risk_Ps", QVariant.Double),
                                            QgsField("Risk_Pa", QVariant.Double),
                                            QgsField("PS_total", QVariant.Double),
                                            QgsField("LS_total", QVariant.Double),
                                            QgsField("Risk_total", QVariant.Double),
                                            QgsField("LS_Fs_r", QVariant.Double), 
                                            QgsField("LS_Ps_r", QVariant.Double),
                                            QgsField("LS_Pa_r", QVariant.Double),
                                            QgsField("LS_total_r", QVariant.Double),
                                            QgsField("PS_Fs_ha", QVariant.Double), 
                                            QgsField("PS_Ps_ha", QVariant.Double),
                                            QgsField("PS_Pa_ha", QVariant.Double),
                                            QgsField("LS_Fs_ha", QVariant.Double), 
                                            QgsField("LS_Ps_ha", QVariant.Double),
                                            QgsField("LS_Pa_ha", QVariant.Double),
                                            QgsField("PS_tot_ha", QVariant.Double),
                                            QgsField("LS_tot_ha", QVariant.Double), ])
        
    work_layer.updateFields()

    expression1 = QgsExpression('("gsv_fag"*("FS_mean"/100)*("F_F_sylvat"/1000)/("P_F_sylvat"/1000))')
    expression2 = QgsExpression('("gsv_pin"*("FS_mean"/100)*("F_P_sylves"/1000)/("P_P_sylves"/1000))')
    expression3 = QgsExpression('("gsv_pic"*("FS_mean"/100)*("F_P_abiesm"/1000)/("P_P_abiesm"/1000))')
    expression4 = QgsExpression('"gsv_fag"-"PS_Fs"')
    expression5 = QgsExpression('"gsv_pin"-"PS_Ps"')
    expression6 = QgsExpression('"gsv_pic"-"PS_Pa"')
    expression7 = QgsExpression('("R_F_F_sy.t"/1000)*"gsv_fag"')
    expression8 = QgsExpression('("R_F_P_sy.t"/1000)*"gsv_pin"')
    expression9 = QgsExpression('("R_F_F_sy.t"/1000)*"gsv_pic"')
    expression10 = QgsExpression('"PS_Fs"+"PS_Ps"+"PS_Pa"')
    expression11 = QgsExpression('"LS_Fs"+"LS_Ps"+"LS_Pa"')
    expression12 = QgsExpression('"Risk_Fs"+"Risk_Ps"+"Risk_Pa"')
    expression13 = QgsExpression('"LS_Fs"*100/"gsv_fag"')
    expression14 = QgsExpression('"LS_Ps"*100/"gsv_pin"')
    expression15 = QgsExpression('"LS_Pa"*100/"gsv_pic"')
    expression16 = QgsExpression('"LS_total"*100/("gsv_fag"+"gsv_pic"+"gsv_pin")')
    expression17 = QgsExpression('("gsv_fag_ha"*("F_F_sylvat"/1000)/("P_F_sylvat"/1000))')
    expression18 = QgsExpression('("gsv_pin_ha"*("F_P_sylves"/1000)/("P_P_sylves"/1000))')
    expression19 = QgsExpression('("gsv_pic_ha"*("F_P_abiesm"/1000)/("P_P_abiesm"/1000))')
    expression20 = QgsExpression('"gsv_fag_ha"-"PS_Fs_ha"')
    expression21 = QgsExpression('"gsv_pin_ha"-"PS_Ps_ha"')
    expression22 = QgsExpression('"gsv_pic_ha"-"PS_Pa_ha"')
    expression23 = QgsExpression('"PS_Fs_ha"+"PS_Ps_ha"+"PS_Pa_ha"')
    expression24 = QgsExpression('"LS_Fs_ha"+"LS_Ps_ha"+"LS_Pa_ha"')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(work_layer))

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['PS_Fs'] = expression1.evaluate(context)
            f['PS_Ps'] = expression2.evaluate(context)
            f['PS_Pa'] = expression3.evaluate(context)
            work_layer.updateFeature(f)
        
    print("PS done")

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['LS_Fs'] = expression4.evaluate(context)
            f['LS_Ps'] = expression5.evaluate(context)
            f['LS_Pa'] = expression6.evaluate(context)
            work_layer.updateFeature(f)
        
    print("LS done")

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['Risk_Fs'] = expression7.evaluate(context)
            f['Risk_Ps'] = expression8.evaluate(context)
            f['Risk_Pa'] = expression9.evaluate(context)
            work_layer.updateFeature(f)
        
    print("Risk done")

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['PS_total'] = expression10.evaluate(context)
            f['LS_total'] = expression11.evaluate(context)
            f['Risk_total'] = expression12.evaluate(context)
            work_layer.updateFeature(f)

    print("total done")    

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['LS_Fs_r'] = expression13.evaluate(context)
            f['LS_Ps_r'] = expression14.evaluate(context)
            f['LS_Pa_r'] = expression15.evaluate(context)
            f['LS_total_r'] = expression16.evaluate(context)
            work_layer.updateFeature(f)

    print("% done")
    
    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['PS_Fs_ha'] = expression17.evaluate(context)
            f['PS_Ps_ha'] = expression18.evaluate(context)
            f['PS_Pa_ha'] = expression19.evaluate(context)
            work_layer.updateFeature(f)
    
    print("PS_ha done")

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['LS_Fs_ha'] = expression20.evaluate(context)
            f['LS_Ps_ha'] = expression21.evaluate(context)
            f['LS_Pa_ha'] = expression22.evaluate(context)
            work_layer.updateFeature(f)
        
    print("LS_ha done")


    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['PS_tot_ha'] = expression23.evaluate(context)
            f['LS_tot_ha'] = expression24.evaluate(context)
            work_layer.updateFeature(f)

    print("total_ha done")    



open_tree_files_future()
open_tree_files_past()
open_files_setting()
rastercalc()
open_rc_layer()
zone_stat()
delete_layer()
fieldcalc()





