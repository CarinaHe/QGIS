
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
                                        QgsField("Risk_total", QVariant.Double),])
        
work_layer.updateFields()

expression1 = QgsExpression('("gsv_fag"*("FS_mean"/100)*("FsZmedian"/1000)/("FsVmedian"/1000))')
expression2 = QgsExpression('("gsv_pin"*("FS_mean"/100)*("PsZmedian"/1000)/("PsVmedian"/1000))')
expression3 = QgsExpression('("gsv_pic"*("FS_mean"/100)*("PaZmedian"/1000)/("PaVmedian"/1000))')
expression4 = QgsExpression('"gsv_fag"-"PS_Fs"')
expression5 = QgsExpression('"gsv_pin"-"PS_Ps"')
expression6 = QgsExpression('"gsv_pic"-"PS_Pa"')
expression7 = QgsExpression('("R_FsZmedia"/1000)*"gsv_fag"')
expression8 = QgsExpression('("R_PsZmedia"/1000)*"gsv_pin"')
expression9 = QgsExpression('("R_FsZmedia"/1000)*"gsv_pic"')
expression10 = QgsExpression('"PS_Fs"+"PS_Ps"+"PS_Pa"')
expression11 = QgsExpression('"LS_Fs"+"LS_Ps"+"LS_Pa"')
expression12 = QgsExpression('"Risk_Fs"+"Risk_Ps"+"Risk_Pa"')

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