import os

from PySide import QtGui, QtCore, QtSvg

ApplicationColors = {
'#111111': '#212121', #Playback
'#222222': '#FFCC00', #GeneralControls
'#333333': '#000099', #Dutch
'#444444': '#4444CC', 
'#555555': '#009999', 
'#666666': '#990000', 
'#777777': '#777777',
'#888888': '#888888',
'#999999': '#999999',
'#AAAAAA': '#AAAAAA',
'#BBBBBB': '#BBBBBB',
'#CCCCCC': '#CCCCCC',
'#DDDDDD': '#DDDDDD',
'#EEEEEE': '#EEEEEE',
}
def IconFromSVG(iconPath):
    with open(iconPath, 'r') as iconFile:
        iconText = iconFile.read()
    for key in ApplicationColors.keys():
        iconText = iconText.replace(key, ApplicationColors[key])
    iconStream = QtCore.QXmlStreamReader(iconText)
    svg_renderer = QtSvg.QSvgRenderer(iconStream)
    
    iconWidth = int(float(iconText.split('<svg',1)[1].split('width="',1)[1].split('"',1)[0]))
    iconHeight = int(float(iconText.split('<svg',1)[1].split('height="',1)[1].split('"',1)[0]))
    image = QtGui.QImage(iconWidth, iconHeight, QtGui.QImage.Format_ARGB32)
    
    image.fill(0x00000000)
    svg_renderer.render(QtGui.QPainter(image))
    pixmap = QtGui.QPixmap.fromImage(image)
    icon = QtGui.QIcon(pixmap)
    icon.actualSize(QtCore.QSize(64,64))
    return icon

    
if '.zip' in __file__:
    iconsPath = __file__.replace('\\','/').split('.zip')[0].rsplit('/',1)[0]+'/Icons'
else:
    iconsPath = __file__.replace('\\','/').rsplit('/',1)[0]
for file in os.listdir(iconsPath):
    if file.rsplit('.',1)[-1] == 'svg':
        exec(file.rsplit('.',1)[0]+' = IconFromSVG(\"'+iconsPath+'/'+file+'\")')