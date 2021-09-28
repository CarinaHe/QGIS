
from pathlib import Path
import sys
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.PyQt.QtCore import QVariant

file_path ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/files'
source_dir = Path(file_path)
file_pathShare ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/tree_shares_reprojected'
source_dirShare = Path(file_pathShare)
file_pathRC ='/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/rastercalc'
source_dirRC = Path(file_pathRC)

filesShare = source_dirShare.iterdir()
filesShare = source_dirShare.glob('*.tif')
filesFuture = source_dir.iterdir()
filesFuture = source_dir.glob('*81_00_85ens.tif')
filesPast1 = source_dir.iterdir()
filesPast1 = source_dir.glob('*1961_90ens.tif')
filesPast2 = source_dir.iterdir()
filesPast2 = source_dir.glob('*1961_90_ens.tif')
filesRC = source_dirRC.iterdir()
filesRC = source_dirRC.glob('*.tif')

layer_list_share=[]
layer_list_future=[]
layer_list_past=[]
layer_list=[]
layer_list_rc = []

def open_tree_files():
    for file in filesShare:
        name = str(file)[len(file_pathShare)+1:]
        name_index = name.index('.')
        name1=name[:name_index]
        layer_list_share.append(iface.addRasterLayer(file_pathShare+'/'+name, name1+'_S'))
       
    for file in filesFuture:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('2')
        name=name[:name_index]
        layer_list_future.append(iface.addRasterLayer(file_path+'/'+name+'2081_00_85ens.tif', name+'_F'))   

    for file in filesPast1:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('1')
        name=name[:name_index]
        layer_list_past.append(iface.addRasterLayer(file_path+'/'+name+'1961_90ens.tif', name+'_P')) 
       
    
    for file in filesPast2:
        name = str(file)[len(file_path)+1:]
        name_index = name.index('1')
        name=name[:name_index]
        layer_list_past.append(iface.addRasterLayer(file_path+'/'+name+'1961_90_ens.tif', name+'_P')) 
        

def open_files_setting():
    layer_list.append(iface.addVectorLayer(f'{file_path}/NUTS2.shp', 'NUTS2', 'ogr'))
    
    for layer in QgsProject.instance().mapLayers().values():
        layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(4326)) 
        
def rastercalc():
    for layer in layer_list_share:
        input_raster1=layer
        name_to_compare = str(layer.name())
        
        for layer in layer_list_future:
            compare = str(layer.name())
            print(name_to_compare)
            print(compare)
            if compare[:3] == name_to_compare[:3]:
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
                    
                outPath = '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/rastercalc/R_F_'+fileName[:6]+'.tif'    
                    # Process calculation with input extent and resolution
                calc = QgsRasterCalculator( "('boh@1'/100)*(1000-'boh@2')", outPath,
                                                'GTiff', input_raster1.extent(),
                                                input_raster1.width(), input_raster1.height(), entries )
                calc.processCalculation()
                
               
                print(layer,' calculated')
            
                outPath = '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/rastercalc/P_F_'+fileName[:6]+'.tif'    
                    # Process calculation with input extent and resolution
                calc = QgsRasterCalculator( "('boh@1'/100)*('boh@2')", outPath,
                                                'GTiff', input_raster1.extent(),
                                                input_raster1.width(), input_raster1.height(), entries )
                calc.processCalculation()
                    
                   
                print(layer,' calculated')
            
            else:
                print(layer,' skipped')
                continue
            
            
        for layer in layer_list_past:
            compare = str(layer.name())
            print('past:'+name_to_compare)
            print('past:'+compare)
            if compare[:3] == name_to_compare[:3]:
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
                    
                outPath = '/home/c/Schreibtisch/BFW/Projekt_ForestRiskMap/rastercalc/P_P_'+fileName[:6]+'.tif'    
                        # Process calculation with input extent and resolution
                calc = QgsRasterCalculator( "('('boh@1'/100)*('boh@2')')", outPath,
                                                    'GTiff', input_raster1.extent(),
                                                    input_raster1.width(), input_raster1.height(), entries )
                calc.processCalculation()
                        
                       
                print(layer,' Past calculated')
                
            else:
                print(layer,' Past skipped')
                continue
                
        
def open_rc_layer():
    for file in filesRC:
        name = str(file)[len(file_pathRC)+1:]
        layer_list_rc.append(iface.addRasterLayer(file_pathRC+'/'+name, name))
        
          
def zone_stat():
    

    for layer in layer_list_rc:
        zoneStat = QgsZonalStatistics (layer_list[0], layer, layer.name(), 1, QgsZonalStatistics.Median)
        zoneStat.calculateStatistics(None)
        print(layer, 'processed')
        
        

def delete_layer():
    
    for layer in layer_list_share:
        QgsProject.instance().removeMapLayer(layer)
        
    for layer in layer_list_future:
        QgsProject.instance().removeMapLayer(layer)
   
    for layer in layer_list_past:
        QgsProject.instance().removeMapLayer(layer)
        
    for layer in layer_list_rc:
        QgsProject.instance().removeMapLayer(layer)


def fieldcalc():
    work_layer.dataProvider().addAttributes([
#                                                QgsField("PS_Fs", QVariant.Double), 
#                                                QgsField("PS_Ps", QVariant.Double),
#                                                QgsField("PS_Pa", QVariant.Double),
#                                                QgsField("SC_Fs", QVariant.Double), 
#                                                QgsField("SC_Ps", QVariant.Double),
#                                                QgsField("SC_Pa", QVariant.Double),
#                                                QgsField("Risk_Fs", QVariant.Double), 
#                                                QgsField("Risk_Ps", QVariant.Double),
#                                                QgsField("Risk_Pa", QVariant.Double),
#                                                QgsField("RP_Fs", QVariant.Double), 
#                                                QgsField("RP_Ps", QVariant.Double),
#                                                QgsField("RP_Pa", QVariant.Double),
#                                                QgsField("PS_total", QVariant.Double),
#                                                QgsField("SC_total", QVariant.Double),
#                                                QgsField("Risk_total", QVariant.Double),
#                                                QgsField("RP_total", QVariant.Double),
#                                                QgsField("SC_Fs_r", QVariant.Double), 
#                                                QgsField("SC_Ps_r", QVariant.Double),
#                                                QgsField("SC_Pa_r", QVariant.Double),
#                                                QgsField("SC_total_r", QVariant.Double),
#                                                QgsField("PS_Fs_ha", QVariant.Double), 
#                                                QgsField("PS_Ps_ha", QVariant.Double),
#                                                QgsField("PS_Pa_ha", QVariant.Double),
                                                QgsField("SC_Fs_ha", QVariant.Double), 
                                                QgsField("SC_Ps_ha", QVariant.Double),
                                                QgsField("SC_Pa_ha", QVariant.Double),
                                                QgsField("PS_tot_ha", QVariant.Double),
                                                QgsField("SC_tot_ha", QVariant.Double), 
    ])
        
    work_layer.updateFields()

    expression1 = QgsExpression('(("gsv_fag"*("P_F_F_sylv"/1000)/("P_P_F_sylv"/1000)))/1000000')
    expression2 = QgsExpression('(("gsv_pin"*("P_F_P_sylv"/1000)/("P_P_P_sylv"/1000)))/1000000')
    expression3 = QgsExpression('(("gsv_pic"*("P_F_P_abie"/1000)/("P_P_P_abie"/1000)))/1000000')
    expression4 = QgsExpression('("PS_Fs"-"gsv_fag"/1000000)')
    expression5 = QgsExpression('("PS_Ps"-"gsv_pin"/1000000)')
    expression6 = QgsExpression('("PS_Pa"-"gsv_pic"/1000000)')
    expression7 = QgsExpression('("R_F_F_sylv"/1000)*"gsv_fag"/1000000')
    expression8 = QgsExpression('("R_F_P_sylv"/1000)*"gsv_pin"/1000000')
    expression9 = QgsExpression('("R_F_P_abie"/1000)*"gsv_pic"/1000000')
    expression25 = QgsExpression('("R_F_F_sylv"/1000)')
    expression26 = QgsExpression('("R_F_P_sylv"/1000)')
    expression27 = QgsExpression('("R_F_P_abie"/1000)')
    expression10 = QgsExpression('"PS_Fs"+"PS_Ps"+"PS_Pa"')
    expression11 = QgsExpression('"SC_Fs"+"SC_Ps"+"SC_Pa"')
    expression12 = QgsExpression('"Risk_Fs"*"Risk_Ps"*"Risk_Pa"')
    expression28 = QgsExpression('"RP_Fs"*"RP_Ps"*"RP_Pa"')
    expression13 = QgsExpression('"SC_Fs"*("gsv_fag"/1000000)/100')
    expression14 = QgsExpression('"SC_Ps"*("gsv_pin"/1000000)/100')
    expression15 = QgsExpression('"SC_Pa"*("gsv_pic"/1000000)/100')
    expression16 = QgsExpression('"SC_total"*(("gsv_fag"+"gsv_pic"+"gsv_pin")/1000000)/100')
    expression17 = QgsExpression('("gsv_fag_ha"*("P_F_F_sylv"/1000)/("P_P_F_sylv"/1000))')
    expression18 = QgsExpression('("gsv_pin_ha"*("P_F_P_sylv"/1000)/("P_P_P_sylv"/1000))')
    expression19 = QgsExpression('("gsv_pic_ha"*("P_F_P_abie"/1000)/("P_P_P_abie"/1000))')
    expression20 = QgsExpression('"PS_Fs_ha"-("gsv_fag_ha")')
    expression21 = QgsExpression('"PS_Ps_ha"-("gsv_pin_ha")')
    expression22 = QgsExpression('"PS_Pa_ha"-("gsv_pic_ha")')
    expression23 = QgsExpression('"PS_Fs_ha"+"PS_Ps_ha"+"PS_Pa_ha"')
    expression24 = QgsExpression('"SC_Fs_ha"+"SC_Ps_ha"+"SC_Pa_ha"')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(work_layer))

    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['PS_Fs'] = expression1.evaluate(context)
    #        f['PS_Ps'] = expression2.evaluate(context)
    #        f['PS_Pa'] = expression3.evaluate(context)
    #        work_layer.updateFeature(f)
    #        
    #print("PS done")
    #
    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['SC_Fs'] = expression4.evaluate(context)
    #        f['SC_Ps'] = expression5.evaluate(context)
    #        f['SC_Pa'] = expression6.evaluate(context)
    #        work_layer.updateFeature(f)
    #        
    #print("SC done")
    #
    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['Risk_Fs'] = expression7.evaluate(context)
    #        f['Risk_Ps'] = expression8.evaluate(context)
    #        f['Risk_Pa'] = expression9.evaluate(context)
    #        work_layer.updateFeature(f)
    #    
    #print("Risk done")
    #
    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['RP_Fs'] = expression25.evaluate(context)
    #        f['RP_Ps'] = expression26.evaluate(context)
    #        f['RP_Pa'] = expression27.evaluate(context)
    #        work_layer.updateFeature(f)
    #        
    #print("RP done")
    #
    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['PS_total'] = expression10.evaluate(context)
    #        f['SC_total'] = expression11.evaluate(context)
    #        f['Risk_total'] = expression12.evaluate(context)
    #        f['RP_total'] = expression28.evaluate(context)
    #        work_layer.updateFeature(f)
    #
    #print("total done")    
    #
    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['SC_Fs_r'] = expression13.evaluate(context)
    #        f['SC_Ps_r'] = expression14.evaluate(context)
    #        f['SC_Pa_r'] = expression15.evaluate(context)
    #        f['SC_total_r'] = expression16.evaluate(context)
    #        work_layer.updateFeature(f)
    #
    #print("% done")
    #    
    #with edit(work_layer):
    #    for f in work_layer.getFeatures():
    #        context.setFeature(f)
    #        f['PS_Fs_ha'] = expression17.evaluate(context)
    #        f['PS_Ps_ha'] = expression18.evaluate(context)
    #        f['PS_Pa_ha'] = expression19.evaluate(context)
    #        work_layer.updateFeature(f)
    #    
    #print("PS_ha done")

    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['SC_Fs_ha'] = expression20.evaluate(context)
            f['SC_Ps_ha'] = expression21.evaluate(context)
            f['SC_Pa_ha'] = expression22.evaluate(context)
            work_layer.updateFeature(f)
        
    print("SC_ha done")


    with edit(work_layer):
        for f in work_layer.getFeatures():
            context.setFeature(f)
            f['PS_tot_ha'] = expression23.evaluate(context)
            f['SC_tot_ha'] = expression24.evaluate(context)
            work_layer.updateFeature(f)

    print("total_ha done")    


open_tree_files()
open_files_setting()
rastercalc()
open_rc_layer()
zone_stat()
delete_layer()
fieldcalc()





