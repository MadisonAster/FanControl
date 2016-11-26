import sys, os, time, traceback, datetime, pprint
import logging, threading, multiprocessing
import json, copy
from pprint import pprint

from PySide import QtGui, QtCore

    
class MainWindow(QtGui.QMainWindow):
    #Purpose: Provides QMainWindow on which owns all widgets in the application
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setDockOptions(False)
        self.setDockNestingEnabled(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('FanControl')
        self.Exit = False
        
        self.StopHit = False
        self.CapturingPicture = False
        
        self.KeepRunning = True
        self.CapturingPicture = False
        self.CapturePictureArgs = None
        
        self.EventControls = EventControls(self)
        self.RunControls = RunControls(self)
        self.TopPane = TopPane(self)
        
        self.SettingsWidget = SettingsWidget(self)
        
        self.dockThisWidget(self.TopPane, dockArea = QtCore.Qt.LeftDockWidgetArea, noTitle = True)
        #self.dockThisWidget(self.RunControls, dockArea = QtCore.Qt.BottomDockWidgetArea, noTitle = True)
        
        self.resize(WIDTH, HEIGHT)
        self.show()

    def ShowSettings(self):
        self.SettingsWidget.show()
    def dockThisWidget(self, widget, dockArea = QtCore.Qt.TopDockWidgetArea, noTitle = False):
        widgetName = widget.accessibleName()
        if widgetName == '':
            widgetName = type(widget).__name__
        dockWidget = QtGui.QDockWidget()
        dockWidget.setFeatures(False)
        dockWidget.setWidget(widget)
        dockWidget.setObjectName(widgetName)
        dockWidget.setWindowTitle(widgetName)
        if noTitle:
            dockWidget.setTitleBarWidget(QtGui.QWidget())
        self.addDockWidget(dockArea, dockWidget)
    def sizeHint(self):
        return QtCore.QSize(800,600)
    def QuitProgram(self):
        quitdialog = YesNoDialog("Are you sure you want to quit?")
        if quitdialog.GetResult() == True:
            self.Exit = True
            QtGui.QApplication.exit()

class YesNoDialog(QtGui.QMessageBox):
    #Purpose: Provides a stylized modal dialog for a consistent look across aplication
    def __init__(self, Question):
        super(YesNoDialog, self).__init__()
        self.setText(Question)
        self.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.move(self.width()/2, self.height()/2)
        self.ret = self.exec_()
        
    def GetResult(self):
        if self.ret == QtGui.QMessageBox.Yes:
            return True
        else:
            return False
class OkCancelDialog(QtGui.QMessageBox):
    #Purpose: Provides a stylized modal dialog for a consistent look across aplication
    def __init__(self, Question):
        super(OkCancelDialog, self).__init__()
        self.setText(Question)
        self.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        self.ret = self.exec_()
    def GetResult(self):
        if self.ret == QtGui.QMessageBox.Ok:
            return True
        else:
            return False
        
        
class IconButton(QtGui.QPushButton):
    #Purpose: Provides a stylized push button for a consistent look across aplication
    def __init__(self, Icon):
        super(IconButton, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFlat(True)
        self.setIcon(Icon)
        self.setIconSize(QtCore.QSize(45,45))
    def sizeHint(self):
        return QtCore.QSize(45,45)
class TextButton(QtGui.QPushButton):
    #Purpose: Provides a stylized push button with text on it for a consistent look across aplication
    def __init__(self, Text):
        super(TextButton, self).__init__(Text)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)
    def sizeHint(self):
        return QtCore.QSize(54,54)
        
class TextInputButton(QtGui.QPushButton):
    #Input button that displays it's text, and calls a touch keyboard for input
    def __init__(self, parent, CurrentText):
        super(TextInputButton, self).__init__(CurrentText)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.pressed.connect(self.ShowDialog)
    def ShowDialog(self):
        #self.parent.hide()
        self.TouchKeyboard = TouchKeyboard(self)
        self.TouchKeyboard.show()
    def setValue(self, value):
        self.setText(value)
    def getValue(self):
        return self.text()
    def sizeHint(self):
        return QtCore.QSize(200,25)

class BoolInputWidget(QtGui.QWidget):
    def __init__(self, parent, Label, CurrentText):
        super(IntInputWidget, self).__init__()
        self.parent = parent
        self.Label = QtGui.QLabel(Label)
        self.InputLine = IntInputLine(self, str(CurrentText))
        
        self.Layout = HLayout()
        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.InputLine)
        self.setLayout(self.Layout)
    def getValue(self):
        return self.InputLine.getValue()
    def setValue(self, value):
        return self.InputLine.setValue(value)
    def text(self):
        return self.Label.text() 
    def setTempValue(self):
        self.parent.setTempValue(self.text(), self.InputLine.getValue())
class BoolInputLine(QtGui.QLineEdit):
    #Input button that displays it's text, and calls a touch keyboard for input
    def __init__(self, parent, CurrentText):
        super(IntInputLine, self).__init__(CurrentText)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.editingFinished.connect(self.parent.setTempValue)
    def ShowDialog(self):
        self.TouchKeyboard = TouchKeyboard(self)
        self.TouchKeyboard.show()
    def focusInEvent(self, event):
        super(IntInputLine, self).focusInEvent(event)
        self.ShowDialog()
    def setValue(self, value):
        self.setText(str(int(value)))
    def getValue(self):
        return int(self.text())
    def sizeHint(self):
        return QtCore.QSize(100,25)        
class FloatInputWidget(QtGui.QWidget):
    def __init__(self, parent, Label, CurrentText):
        super(FloatInputWidget, self).__init__()
        self.parent = parent
        self.Label = QtGui.QLabel(Label)
        self.InputLine = FloatInputLine(self, str(CurrentText))
        
        self.Layout = HLayout()
        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.InputLine)
        self.setLayout(self.Layout)
    def getValue(self):
        return self.InputLine.getValue()
    def setValue(self, value):
        return self.InputLine.setValue(value)
    def text(self):
        return self.Label.text()
    def setTempValue(self):
        self.parent.setTempValue(self.text(), self.InputLine.getValue())
class FloatInputLine(QtGui.QLineEdit):
    #Input button that displays it's text, and calls a touch keyboard for input
    def __init__(self, parent, CurrentText):
        super(FloatInputLine, self).__init__(CurrentText)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.editingFinished.connect(self.parent.setTempValue)
    def ShowDialog(self):
        self.TouchKeyboard = TouchKeyboard(self)
        self.TouchKeyboard.show()
    def focusInEvent(self, event):
        super(FloatInputLine, self).focusInEvent(event)
        self.ShowDialog()
    def setValue(self, value):
        self.setText(str(float(value)))
    def getValue(self):
        return float(self.text())
    def sizeHint(self):
        return QtCore.QSize(100,25) 
class IntInputWidget(QtGui.QWidget):
    def __init__(self, parent, Label, CurrentText):
        super(IntInputWidget, self).__init__()
        self.parent = parent
        self.Label = QtGui.QLabel(Label)
        self.InputLine = IntInputLine(self, str(CurrentText))
        
        self.Layout = HLayout()
        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.InputLine)
        self.setLayout(self.Layout)
    def getValue(self):
        return self.InputLine.getValue()
    def setValue(self, value):
        return self.InputLine.setValue(value)
    def text(self):
        return self.Label.text() 
    def setTempValue(self):
        self.parent.setTempValue(self.text(), self.InputLine.getValue())
class IntInputLine(QtGui.QLineEdit):
    #Input button that displays it's text, and calls a touch keyboard for input
    def __init__(self, parent, CurrentText):
        super(IntInputLine, self).__init__(CurrentText)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.editingFinished.connect(self.parent.setTempValue)
    def ShowDialog(self):
        self.TouchKeyboard = TouchKeyboard(self)
        self.TouchKeyboard.show()
    def focusInEvent(self, event):
        super(IntInputLine, self).focusInEvent(event)
        self.ShowDialog()
    def setValue(self, value):
        self.setText(str(int(value)))
    def getValue(self):
        return int(self.text())
    def sizeHint(self):
        return QtCore.QSize(100,25)
class TextInputWidget(QtGui.QWidget):
    def __init__(self, parent, Label, CurrentText):
        super(TextInputWidget, self).__init__()
        self.parent = parent
        self.Label = QtGui.QLabel(Label)
        self.InputLine = TextInputLine(self, CurrentText)
        
        self.Layout = HLayout()
        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.InputLine)
        self.setLayout(self.Layout)
    def getValue(self):
        return self.InputLine.getValue()
    def setValue(self, value):
        return self.InputLine.setValue(value)
    def text(self):
        return self.Label.text()
    def setTempValue(self):
        self.parent.setTempValue(self.text(), self.InputLine.getValue())
class TextInputLine(QtGui.QLineEdit):
    #Input button that displays it's text, and calls a touch keyboard for input
    def __init__(self, parent, CurrentText):
        super(TextInputLine, self).__init__(CurrentText)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.editingFinished.connect(self.parent.setTempValue)
    def ShowDialog(self):
        self.TouchKeyboard = TouchKeyboard(self)
        self.TouchKeyboard.show()
    def focusInEvent(self, event):
        super(TextInputLine, self).focusInEvent(event)
        self.ShowDialog()
    def setValue(self, value):
        self.setText(value)
    def getValue(self):
        return self.text()
    def sizeHint(self):
        return QtCore.QSize(200,25)
        
class TouchKeyboard(QtGui.QWidget):
    #Purpose: A Touch keyboard for use with touchscreen
    def __init__(self, parent):
        super(TouchKeyboard, self).__init__()
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.TextPreview = QtGui.QTextEdit(str(self.parent.getValue()))
        self.CursorPosition = self.TextPreview.textCursor().position()
        self.TextPreview.cursorPositionChanged.connect(self.KeepCursor)
        self.TextPreview.zoomIn(range=8)
        self.TextPreview.moveCursor(QtGui.QTextCursor.EndOfLine)
        
        self.CapsActivated = False        
        self.show()
        
        
        #Define Buttons
        self.BackButton = TextButton('Backspace')
        self.BackButton.pressed.connect(self.Backspace)
        self.BackslashButton = TextButton('\\')
        self.BackslashButton.pressed.connect(self.KeyPress)
        self.EnterButton = TextButton('Enter')
        self.EnterButton.pressed.connect(self.EnterPress)
        self.CapsLockButton = TextButton('Caps')
        self.CapsLockButton.pressed.connect(self.Caps)
        self.CancelButton = TextButton('Cancel')
        self.CancelButton.pressed.connect(self.Cancel)
        self.ApplyButton = TextButton('Apply')
        self.ApplyButton.pressed.connect(self.Apply)     
        
        self.KeyL1 = HLayout()
        self.KeyL2 = HLayout()
        self.KeyL3 = HLayout()
        self.KeyL4 = HLayout()
        KeyLayouts = [self.KeyL1, self.KeyL2, self.KeyL3, self.KeyL4]
        KeyLists = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]
        for KeyLayout, KeyList in zip(KeyLayouts, KeyLists):
            KeyLayout.addWidget(HSpacer())
            for a in KeyList:
                Button = TextButton(a)
                Button.pressed.connect(self.KeyPress)
                KeyLayout.addWidget(Button)
            KeyLayout.addWidget(HSpacer())        
        
        
        #Define Layouts
        self.Layout = VLayout()
        
        self.KeysLayout = VLayout()
        self.KeysLayout.addWidget(VSpacer())
        self.KeysLayout.addLayout(self.KeyL1)
        self.KeysLayout.addLayout(self.KeyL2)
        self.KeysLayout.addLayout(self.KeyL3)
        self.KeysLayout.addLayout(self.KeyL4)
        
        self.SpecialKeys = VLayout()
        self.SpecialKeys.addWidget(VSpacer())
        self.SpecialKeys.addWidget(self.BackButton)
        self.SpecialKeys.addWidget(VSpacer())
        self.SpecialKeys.addWidget(self.BackslashButton)
        self.SpecialKeys.addWidget(VSpacer())
        self.SpecialKeys.addWidget(VSpacer())
        self.SpecialKeys.addWidget(self.EnterButton)
        self.SpecialKeys.addWidget(VSpacer())
        self.SpecialKeys.addWidget(self.CapsLockButton)
        self.SpecialKeys.addWidget(VSpacer())
        
        self.KeyBoard = HLayout()
        self.KeyBoard.addLayout(self.KeysLayout)
        self.KeyBoard.addLayout(self.SpecialKeys)
        
        self.Buttons = HLayout()
        self.Buttons.addWidget(self.CancelButton)
        self.Buttons.addWidget(self.ApplyButton)
        
        
        #Final Layout
        self.Layout.addWidget(VSpacer())
        self.Layout.addWidget(self.TextPreview)
        self.Layout.addWidget(VSpacer())
        self.Layout.addLayout(self.KeyBoard)
        self.Layout.addLayout(self.Buttons)
        self.setLayout(self.Layout)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(WIDTH, HEIGHT)
    def Cancel(self):
        self.parent.clearFocus()
        self.close()
    def Apply(self):
        self.parent.setValue(self.TextPreview.toPlainText())
        self.parent.clearFocus()
        self.parent.editingFinished.emit()
        self.close()
    def Backspace(self):
        CurrentText = self.TextPreview.toPlainText()
        CursorPosition = self.CursorPosition
        self.TextPreview.setText(CurrentText[0:CursorPosition-1]+CurrentText[CursorPosition:])
        self.TextPreview.setFocus()
        newcursor = self.TextPreview.textCursor()
        newcursor.setPosition(CursorPosition-1)
        self.TextPreview.setTextCursor(newcursor)
    def EnterPress(self):
        CurrentText = self.TextPreview.toPlainText()
        SentText = '\n'
        CursorPosition = self.CursorPosition
        self.TextPreview.setText(CurrentText[0:CursorPosition]+SentText+CurrentText[CursorPosition:])
        self.TextPreview.setFocus()
        
        newcursor = self.TextPreview.textCursor()
        newcursor.setPosition(CursorPosition+1)
        self.TextPreview.setTextCursor(newcursor)
    def Caps(self):
        self.CapsActivated = not self.CapsActivated
    def KeyPress(self):
        CurrentText = self.TextPreview.toPlainText()
        SentText = self.sender().text()
        if not self.CapsActivated:
            SentText = SentText.lower()
        CursorPosition = self.CursorPosition
        self.TextPreview.setText(CurrentText[0:CursorPosition]+SentText+CurrentText[CursorPosition:])
        #self.TextPreview.setFocus()
        
        newcursor = self.TextPreview.textCursor()
        newcursor.setPosition(CursorPosition+1)
        self.TextPreview.setTextCursor(newcursor)
    def KeepCursor(self):
        self.CursorPosition = self.TextPreview.textCursor().position()
    def sizeHint(self):
        return QtCore.QSize(800,600)
        
class ProgressBar(QtGui.QProgressBar):
    #Purpose: Progress bar to indicate playback position
    def __init__(self):
        super(ProgBar, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    def sizeHint(self):
        return QtCore.QSize(100,45)
        
class ConfigHandler():
    #Purpose: Saves/Loads json objects, and stores the current configuration
    def __init__(self):
        self.LoadConfig()
        self.LoadDefaultConfig()
    def LoadConfig(self):
        self.CurrentConf = json.load(open('Conf.json'))
        self.TempConf = copy.copy(self.CurrentConf)
    def LoadDefaultConfig(self):
        self.DefaultConf = json.load(open('DefaultConf.json'))
    def ApplyDefaultConfig(self):
        self.CurrentConf = copy.copy(self.DefaultConf)
    def ApplyTempConfig(self):
        self.CurrentConf = copy.copy(self.TempConf)
    def CopyCurrentConfig(self):
        self.TempConf = copy.copy(self.TempConf)
    def setValue(self, key, value):
        self.TempConf[key] = value
    def WriteConfig(self):
        with open('newconf.json', 'w') as file:
            json.dump(self.CurrentConf, file, sort_keys=True, indent=4, separators=(',', ': '))
    def SaveSettings(self):
        self.ApplyTempConfig()
        self.WriteConfig()
        
class EchoSlider(QtGui.QSlider):
    def __init__(self, SliderNumber):
        super(EchoSlider, self).__init__(QtCore.Qt.Vertical)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setRange(0.0, 10)
        self.setSingleStep(1)
        self.setPageStep(1)
        
        self.SliderNumber = SliderNumber
    def sizeHint(self):
        return QtCore.QSize(50,300)
class VertSlider(QtGui.QWidget):
    def __init__(self, SliderNumber, Label, action):
        super(VertSlider, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.Label = QtGui.QLabel(str(Label))
        self.Label.setIndent(35)
        self.EchoSlider = EchoSlider(SliderNumber)
        
        self.Layout = QtGui.QStackedLayout()
        self.Layout.setStackingMode(QtGui.QStackedLayout.StackAll)
        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.EchoSlider)
        
        self.setLayout(self.Layout)
        
        self.EchoSlider.valueChanged.connect(action)
    def sizeHint(self):
        return QtCore.QSize(50,300)
    def setRepeatAction(self, *args):
        return self.EchoSlider.setRepeatAction(*args)
    def setSliderPosition(self, *args):
        return self.EchoSlider.setSliderPosition(*args)
    def setSliderPosition(self, *args):
        return self.EchoSlider.setSliderPosition(*args)
    def sliderPosition(self):
        return self.EchoSlider.sliderPosition()
    
class ToolSpacer(QtGui.QWidget):
    #Purpose: Useful for spacing inside a QToolBar
    def __init__(self):
        super(ToolSpacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    def sizeHint(self):
        return QtCore.QSize(0,0)
class ButtonSpacer(QtGui.QWidget):
    #Purpose: Fixed spacing of a standard size to keep buttons consistently spaced
    def __init__(self):
        super(ButtonSpacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    def sizeHint(self):
        return QtCore.QSize(45,45)
class FixedSpacer(QtGui.QWidget):
    #Purpose: Useful for providing spacing of a fixed size within a layout
    def __init__(self, width = 0, height = 0):
        super(FixedSpacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.width = width
        self.height = height
    def sizeHint(self):
        return QtCore.QSize(self.width, self.height)
class HLayout(QtGui.QHBoxLayout):
    #Purpose: Horizontal box layout
    def __init__(self):
        super(HLayout, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
class HSpacer(QtGui.QWidget):
    #Purpose: Use for spacing objects within a horizontal layout
    def __init__(self):
        super(HSpacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
    def sizeHint(self):
        return QtCore.QSize(0,0)
class VLayout(QtGui.QVBoxLayout):
    #Purpose: Vertical box layout
    def __init__(self):
        super(VLayout, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
class VSpacer(QtGui.QWidget):
    #Purpose: Use for spacing objects within a vertical layout
    def __init__(self):
        super(VSpacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
    def sizeHint(self):
        return QtCore.QSize(0,0)
class EventControls(QtGui.QWidget):
    def __init__(self, parent):
        super(EventControls, self).__init__()
        self.parent = parent
        self.Layout = QtGui.QVBoxLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)
        #self.Layout.addWidget(VSpacer())
        self.SettingsButton = TextButton('Settings')
        self.Layout.addWidget(self.SettingsButton)
        self.QuitButton = TextButton('Quit')
        self.Layout.addWidget(self.QuitButton)
        
        self.setLayout(self.Layout)
        
        self.SettingsButton.pressed.connect(self.parent.ShowSettings)
        self.QuitButton.pressed.connect(self.parent.QuitProgram)
        
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
    def __getitem__(self, item):
        return self.Layers.widgetList[item]
    def sizeHint(self):
        return QtCore.QSize(200,100)
 
class TopPane(QtGui.QWidget):
    def __init__(self, parent):
        super(TopPane, self).__init__()
        self.parent = parent
        
        self.Layout = QtGui.QHBoxLayout()
        self.Sliders = QtGui.QVBoxLayout()
        self.SliderSet1 = QtGui.QHBoxLayout()
        self.SliderSet2 = QtGui.QHBoxLayout()
        
        FanList1 = [10,3,5,7,9,11,13,15]
        FanList2 = [17,19,21,23,25,27,26]
        self.FanWidgets = []
        
        self.MasterSlider = VertSlider(0, 'master', self.SetSliders)
        
        for a in FanList1:
            slider = VertSlider(a, str(a), self.EchoValue)
            self.SliderSet1.addWidget(slider)
            self.FanWidgets.append(slider)
        for a in FanList2:
            slider = VertSlider(a, str(a), self.EchoValue)
            self.SliderSet2.addWidget(slider)
            self.FanWidgets.append(slider)
        else:
            self.SliderSet2.addWidget(FixedSpacer(width = 62, height = 300))
        
        
        self.Sliders.addLayout(self.SliderSet1)
        self.Sliders.addLayout(self.SliderSet2)
        self.Layout.addWidget(self.parent.EventControls)
        self.Layout.addWidget(self.MasterSlider)
        self.Layout.addLayout(self.Sliders)
        
        self.setLayout(self.Layout)
    def SetSliders(self):
        for slider in self.FanWidgets:
            slider.setSliderPosition(self.MasterSlider.sliderPosition())
    def EchoValue(self):
        value = 1.0-(self.sender().sliderPosition()/10.0)
        pin = self.sender().SliderNumber
        cmd = 'echo "'+str(pin)+'='+str(value)+'" > /dev/pi-blaster'
        os.system(cmd)
class CheckboxKnob(QtGui.QCheckBox):
    def __init__(self, labelText):
        super(CheckboxKnob, self).__init__(labelText)
    #def sizeHint(self):
    #    return QtCore.QSize(16,16)
    def setValue(self, value):
        if value == True:
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)
        self.update()
    def getValue(self):
        value = self.checkState()
        if value == QtCore.Qt.Checked:
            return True
        if value == QtCore.Qt.Unchecked:
            return False
        
class SettingsWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(SettingsWidget, self).__init__()
        self.parent = parent
        self.config = ConfigHandler()
        
        self.Layout = QtGui.QVBoxLayout()
        self.SettingsColumns = QtGui.QHBoxLayout()
        self.Column1 = QtGui.QVBoxLayout()
        self.Column2 = QtGui.QVBoxLayout()
        self.ControlButtons = QtGui.QHBoxLayout()
        
        self.SettingsColumns.addLayout(self.Column1)
        self.SettingsColumns.addLayout(self.Column2)
        self.Layout.addLayout(self.SettingsColumns)
        self.Layout.addLayout(self.ControlButtons)
        
        #########################################
        
        self.LoginButton = TextInputButton(self, 'Username')
        self.PasswordButton = TextInputButton(self, 'Password')
        
        self.BackButton = TextButton('Back')
        self.DefaultsButton = TextButton('Restore Defaults')
        self.ApplyButton = TextButton('Apply')

        self.ConfigButtons = {}
        for a in self.config.CurrentConf:
            value = self.config.CurrentConf[a]
            if type(value) == bool:
                thisbutton = CheckboxKnob(a)
                thisbutton.setValue(value)
                thisbutton.stateChanged.connect(self.setBool)
            elif type(value) == float:
                thisbutton = FloatInputWidget(self, str(a), value)
            elif type(value) == int:
                thisbutton = IntInputWidget(self, str(a), value)
            elif type(value) == unicode:
                thisbutton = TextInputWidget(self, str(a), value)
            self.ConfigButtons[a] = thisbutton
        
        ########################################
        
        counter = 0
        for a in self.ConfigButtons:
            if counter < 12:
                counter += 1
                self.Column1.addWidget(self.ConfigButtons[a])
            else:
                self.Column2.addWidget(self.ConfigButtons[a])
        
        self.ControlButtons.addWidget(self.BackButton)
        self.ControlButtons.addWidget(self.DefaultsButton)
        self.ControlButtons.addWidget(self.ApplyButton)
        
        self.BackButton.pressed.connect(self.Back)
        self.DefaultsButton.pressed.connect(self.ApplyDefault)
        self.ApplyButton.pressed.connect(self.Apply)
        self.setLayout(self.Layout)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(WIDTH, HEIGHT)
    def setValuesToCurrent(self):
        for a in self.config.CurrentConf:
            value = self.config.CurrentConf[a]
            self.ConfigButtons[a].setValue(value)
    def setBool(self):
        BoolState = self.sender().checkState()
        SentText = self.sender().text()
    def setTempValue(self, key, value):
        self.config.setValue(key, value)
    def Apply(self):    
        self.config.SaveSettings()
        self.setValuesToCurrent()
    def ApplyDefault(self):    
        self.config.ApplyDefaultConfig()
        self.setValuesToCurrent()
    def Back(self):
        self.config.CopyCurrentConfig()
        self.setValuesToCurrent()
        self.hide()
    
class RunControls(QtGui.QToolBar):
    def __init__(self, parent):
        super(RunControls, self).__init__()
        self.parent = parent
        self.setIconSize(QtCore.QSize(45, 45))
        
        self.addWidget(ToolSpacer())
        
        RunBackward = QtGui.QAction(Icons.RPlay, 'RunBackward', self)
        #RunBackward.triggered.connect(self.parent.ThreadRunBackward)
        self.addAction(RunBackward)
        
        self.addWidget(ToolSpacer())
        
        StepBackward = QtGui.QAction(Icons.RAdvance, 'StepBackward', self)
        #StepBackward.triggered.connect(self.parent.StepBackward)
        self.addAction(StepBackward)
        
        self.addWidget(ToolSpacer())
        
        StopRunning = QtGui.QAction(Icons.Stop, 'StopRunning', self)
        #StopRunning.triggered.connect(self.parent.StopRunning)
        self.addAction(StopRunning)
        
        self.addWidget(ToolSpacer())
        
        StepForward = QtGui.QAction(Icons.Advance, 'StepForward', self)
        #StepForward.triggered.connect(self.parent.StepForwardCmd)
        self.addAction(StepForward)
        
        self.addWidget(ToolSpacer())
        
        RunForward = QtGui.QAction(Icons.Play, 'RunForward', self)
        #RunForward.triggered.connect(self.parent.ThreadRunForward)
        self.addAction(RunForward)
        
        self.addWidget(ToolSpacer())

def generateStyleSheet(App):
        palette = App.palette()
        Window = palette.window().color().name()
        WindowText = palette.windowText().color().name()
        Base = palette.base().color().name()
        AlternateBase = palette.alternateBase().color().name()
        ToolTipBase = palette.toolTipBase().color().name()
        ToolTipText = palette.toolTipText().color().name()
        Text = palette.text().color().name()
        Button = palette.button().color().name()
        ButtonText = palette.buttonText().color().name()
        BrightText = palette.brightText().color().name()
        Light = palette.light().color().name()
        Midlight = palette.midlight().color().name()
        Dark = palette.dark().color().name()
        Mid = palette.mid().color().name()
        Shadow = palette.shadow().color().name()
        Highlight = palette.highlight().color().name()
        HighlightedText = palette.highlightedText().color().name()
        Link = palette.link().color().name()
        LinkVisited = palette.linkVisited().color().name()
        
        stylesheet = 'QPushButton {background: '+Button+'; color: '+ButtonText+';}\n'
        stylesheet += 'QLineEdit {background: '+Button+'; color: '+ButtonText+'; border: '+Shadow+';}\n'
        stylesheet += 'QComboBox {background: '+Button+'; color: '+ButtonText+'; border: '+Shadow+';}\n'
        stylesheet += 'QCheckBox {color: '+ButtonText+'; border: '+Shadow+';}\n'
        stylesheet += 'QDockWidget {border: '+Shadow+';}\n'
        stylesheet += 'QDockWidget::title {background: '+Dark+';}\n'
        stylesheet += 'QMessageBox {background: '+Dark+'; color: '+WindowText+';}\n'
        stylesheet += 'QMenuBar {background: '+Window+'; color: '+WindowText+';}\n'
        stylesheet += 'QMenuBar::item {background: '+Window+';}\n'
        stylesheet += 'QMenu {background: '+Window+'; color: '+WindowText+';}\n'
        
        stylesheet += 'QScrollBar:vertical {background: '+Window+'; border: 1px inset;}\n'
        stylesheet += 'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}\n'
        stylesheet += 'QScrollBar::handle:vertical {background: '+Button+'; margin: 24px 0 24px 0;}\n'
       
        stylesheet += 'QScrollBar:horizontal {background: '+Window+'; border: 1px inset;}\n'
        stylesheet += 'QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {background: none;}\n'
        stylesheet += 'QScrollBar::handle:horizontal {background: '+Button+'; margin: 0 24px 0 24px;}\n'
        
        stylesheet += 'QToolBar{background: '+Window+'; spacing: 3px;}\n'
        #stylesheet += "QScrollBar::add-line:vertical { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130)); height: px; subcontrol-position: bottom; subcontrol-origin: margin;}"
        
        return stylesheet
        
def main():
    global mainAPP
    mainAPP = QtGui.QApplication(sys.argv)
    palette = mainAPP.palette()
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(30,30,30))
    palette.setColor(QtGui.QPalette.Shadow, QtGui.QColor(0,0,0))
    palette.setColor(QtGui.QPalette.Dark, QtGui.QColor(45,45,45))
    palette.setColor(QtGui.QPalette.Background, QtGui.QColor(60,60,60))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(60,60,60))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(60,60,60))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255,255,255))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255,255,255))
    palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255,255,255))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255,255,255))
    palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255,255,255))
    mainAPP.setPalette(palette)
    
    mainAPP.setStyleSheet(generateStyleSheet(mainAPP))
    
    global WIDTH, HEIGHT
    WIDTH = QtGui.QDesktopWidget().availableGeometry().width()
    HEIGHT = QtGui.QDesktopWidget().availableGeometry().height()
    
    WIDTH = 800
    HEIGHT = 450
    
    global Icons
    import Icons
    
    global CurrentDirectory
    CurrentDirectory = __file__.replace('\\','/')
    if '/' in CurrentDirectory:
        CurrentDirectory = CurrentDirectory.rsplit('/',1)[0]
    else:
        CurrentDirectory = './'
    
    Window = MainWindow()
    sys.exit(mainAPP.exec_())
if __name__ == '__main__':
    main()