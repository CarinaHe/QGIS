
from qgis.PyQt.QtCore import QVariant

layer_list=iface.mapCanvas().layers()

i=0

for layer in layer_list:
    layerType = layer.type()
    if layerType == QgsMapLayer.VectorLayer:
        work_layer=layer_list[i]
        layer_list.pop(i)
    i+=1

print(layer_list)

print(work_layer)


work_layer.dataProvider().addAttributes([QgsField("PS_Fs_ha", QVariant.Double), 
                                        QgsField("PS_Ps_ha", QVariant.Double),
                                        QgsField("PS_Pa_ha", QVariant.Double),
                                        QgsField("LS_Fs_ha", QVariant.Double), 
                                        QgsField("LS_Ps_ha", QVariant.Double),
                                        QgsField("LS_Pa_ha", QVariant.Double),
                                        QgsField("PS_tot_ha", QVariant.Double),
                                        QgsField("LS_tot_ha", QVariant.Double),])
        
work_layer.updateFields()

expression1 = QgsExpression('("gsv_fag_ha"*("FsZmedian"/1000)/("FsVmedian"/1000))')
expression2 = QgsExpression('("gsv_pin_ha"*("PsZmedian"/1000)/("PsVmedian"/1000))')
expression3 = QgsExpression('("gsv_pic_ha"*("PaZmedian"/1000)/("PaVmedian"/1000))')
expression4 = QgsExpression('"gsv_fag_ha"-"PS_Fs_ha"')
expression5 = QgsExpression('"gsv_pin_ha"-"PS_Ps_ha"')
expression6 = QgsExpression('"gsv_pic_ha"-"PS_Pa_ha"')
expression7 = QgsExpression('"PS_Fs_ha"+"PS_Ps_ha"+"PS_Pa_ha"')
expression8 = QgsExpression('"LS_Fs_ha"+"LS_Ps_ha"+"LS_Pa_ha"')


context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(work_layer))

with edit(work_layer):
    for f in work_layer.getFeatures():
        context.setFeature(f)
        f['PS_Fs_ha'] = expression1.evaluate(context)
        f['PS_Ps_ha'] = expression2.evaluate(context)
        f['PS_Pa_ha'] = expression3.evaluate(context)
        work_layer.updateFeature(f)
    
print("PS done")

with edit(work_layer):
    for f in work_layer.getFeatures():
        context.setFeature(f)
        f['LS_Fs_ha'] = expression4.evaluate(context)
        f['LS_Ps_ha'] = expression5.evaluate(context)
        f['LS_Pa_ha'] = expression6.evaluate(context)
        work_layer.updateFeature(f)
    
print("LS done")


with edit(work_layer):
    for f in work_layer.getFeatures():
        context.setFeature(f)
        f['PS_tot_ha'] = expression7.evaluate(context)
        f['LS_tot_ha'] = expression8.evaluate(context)
        work_layer.updateFeature(f)

print("total done")    