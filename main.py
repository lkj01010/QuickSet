# -*- coding: UTF-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import sys
import os
import subprocess

from PySide2.QtOpenGL import *

kTerminalPath = "/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal"


class SystrayLauncher(object):

    def __init__(self):
        super(SystrayLauncher, self).__init__()

        self.logWin = LogWindow()
        self.curDir = os.path.dirname(__file__)

        w = QtWidgets.QWidget()  # just to get the style(), haven't seen other way
        # icon = w.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload)
        icon = QtGui.QIcon("/Users/Midstream/Documents/Art/MyIcons/quick_gray.png")
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray.activated.connect(self.onActivated)

        # shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1), self.tray)
        # shortcut.setContext(QtCore.Qt.ApplicationShortcut)
        # shortcut.activated.connect(self.handler)

        # I JUST WANT TO SEE THE MENU WHEN RIGHT CLICK...
        menu = QtWidgets.QMenu()

        ##################################################

        submenu = menu.addMenu("打开")

        self.act_open_Terminal = QtWidgets.QAction("Terminal", None, triggered=self.open_Terminal)
        submenu.addAction(self.act_open_Terminal)

        self.act_open_Monitor = QtWidgets.QAction("Monitor", None, triggered=self.open_Monitor)
        submenu.addAction(self.act_open_Monitor)

        self.act_open_SysPref = QtWidgets.QAction("偏好设置", None, triggered=self.open_SysPref)
        submenu.addAction(self.act_open_SysPref)

        self.act_open_Mail = QtWidgets.QAction("邮件", None, triggered=self.open_Mail)
        submenu.addAction(self.act_open_Mail)

        submenu.addSeparator()

        self.act_open_Shadow = QtWidgets.QAction("ShadowRocket", None, triggered=self.open_Shadow)
        submenu.addAction(self.act_open_Shadow)

        self.act_open_Dict = QtWidgets.QAction("欧路词典", None, triggered=self.open_Dict)
        submenu.addAction(self.act_open_Dict)

        self.act_open_QQMusic = QtWidgets.QAction("QQ音乐", None, triggered=self.open_QQMusic)
        submenu.addAction(self.act_open_QQMusic)

        self.act_open_Note = QtWidgets.QAction("云笔记", None, triggered=self.open_Note)
        submenu.addAction(self.act_open_Note)

        ##################################################

        # self.psAction = QtWidgets.QAction("Ps", None, triggered=self.psUx)
        # menu.addAction(self.psAction)
        #
        # self.logAction = QtWidgets.QAction("Log", None, triggered=self.openLog)
        # menu.addAction(self.logAction)

        menu.addSeparator()

        self.watchAction1 = QtWidgets.QAction("WsFx -> Unity", None, triggered=self.watch1)
        menu.addAction(self.watchAction1)

        self.colorPickerAction = QtWidgets.QAction("Color Picker", None, triggered=self.openColorPicker)
        menu.addAction(self.colorPickerAction)

        menu.addSeparator()

        self.openScriptsQuickSetAction = QtWidgets.QAction("脚本 QuickSet", None, triggered=self.openScriptsQuickSet)
        menu.addAction(self.openScriptsQuickSetAction)

        self.openScriptsMayaAction = QtWidgets.QAction("脚本 Maya", None, triggered=self.openScriptsMaya)
        menu.addAction(self.openScriptsMayaAction)

        self.openScripts3Action = QtWidgets.QAction("脚本 3D-Coat", None, triggered=self.openScripts3)
        menu.addAction(self.openScripts3Action)

        menu.addSeparator()

        self.openDirFxAction = QtWidgets.QAction("目录 特效", None, triggered=self.openDirFx)
        menu.addAction(self.openDirFxAction)

        menu.addSeparator()

        self.quitAction = QtWidgets.QAction("Qui&t", None, triggered=QtWidgets.QApplication.instance().quit)
        menu.addAction(self.quitAction)

        # aQuit = menu.addAction("qqquit")
        # aQuit.triggered.connect(QtWidgets.QApplication.instance().quit)

        self.trayIconMenu = menu
        self.tray.setContextMenu(menu)

        self.log('start cur dir = ' + self.curDir)

    def testHandle(self):
        print("test")

    def openLog(self):
        self.logWin.show()

    def onActivated(self, signal):
        # print("left click pressed")
        pass

    def log(self, text):
        self.logWin.textEdit.append(text)

    def open_Terminal(self):
        subprocess.Popen(
            ["/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal"],
            shell=True)

    def open_Monitor(self):
        subprocess.Popen(
            ["/Applications/Utilities/Activity\ Monitor.app/Contents/MacOS/Activity\ Monitor"],
            shell=True)

    def open_Shadow(self):
        subprocess.Popen(
            ["/Applications/ShadowsocksX-NG-R8.app/Contents/MacOS/ShadowsocksX-NG"],
            shell=True)

    def open_Dict(self):
        subprocess.Popen(
            ["/Applications/Eudb_en_free.app/Contents/MacOS/Eudb_en_free"],
            shell=True)

    def open_QQMusic(self):
        subprocess.Popen(
            ["/Applications/QQMusic.app/Contents/MacOS/QQMusic"],
            shell=True)

    def open_Note(self):
        subprocess.Popen(
            ["/Applications/YoudaoNote.localized/YoudaoNote.app/Contents/MacOS/YoudaoNote"],
            shell=True)

    def open_Mail(self):
        subprocess.Popen(
            ["/Applications/Mail.app/Contents/MacOS/Mail"],
            shell=True)

    def open_SysPref(self):
        subprocess.Popen(
            ["/Applications/System\ Preferences.app/Contents/MacOS/System\ Preferences"],
            shell=True)

    def psUx(self):
        # cmdstr = "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7 /Users/Midstream/Documents/Dev/Desktop/PySide2_examples/declarative/signals/qmltopy1/main.py"
        cmdstr = "ps aux"

        if 'darwin' in sys.platform:
            p = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE)

            with p.stdout as f:
                for line in f:
                    line = line.strip()
                    self.log(line)

        # for line in runProcess("", []):
        #     self.log(line)

    def watch1(self):
        # kSrc = "/Users/Midstream/Documents/Cur/Ws-Effect/O_Sprite"
        subprocess.Popen(
            # ["open /Users/Midstream/Documents/Dev/Desktop/QuickSet/watch_copy.command"],
            ["open -a " + kTerminalPath + " " + self.curDir + "/watch_copy.py"],
            shell=True)

    def openScriptsQuickSet(self):
        # subprocess.Popen(
        #     ["/Applications/PyCharm2018.3.app/Contents/MacOS/pycharm"]
        # )
        subprocess.Popen(
            ["/Applications/PyCharm2018.3.app/Contents/MacOS/pycharm " + self.curDir],
            shell=True)
        # subprocess.Popen(["/Applications/Visual\ Studio\ Code.app/Contents/MacOS/Electron /Users/Midstream/3D-CoatV48/Scripts"], shell=True)
        # subprocess.Popen(["/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal ssh moba"], shell=True)

        # subprocess.Popen(["open ."], shell=True)

    def openScriptsMaya(self):
        subprocess.Popen(
            ["/Applications/PyCharm2018.3.app/Contents/MacOS/pycharm /Users/Midstream/Documents/Soft_Cfgs/Maya"],
            shell=True)

    def openScripts3(self):
        subprocess.Popen(
            ["/Applications/Visual\ Studio\ Code.app/Contents/MacOS/Electron /Users/Midstream/3D-CoatV48/Scripts"],
            shell=True)

    def openDirFx(self):
        subprocess.Popen(["open /Users/Midstream/Documents/Cur/Ws-Effect"], shell=True)
        subprocess.Popen(["open /Users/Midstream/Documents/Cur/Moba2D/Assets/Textures/Fx"], shell=True)

    def openColorPicker(self):
        return


def runProcess(command, arguments):
    process = QtCore.QProcess()
    process.start(command, arguments)
    process.waitForFinished()
    std_output = process.readAllStandardOutput().data().decode('utf-8')
    return std_output.split('\n')


class LogWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LogWindow, self).__init__()

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)

        self.setCentralWidget(self.textEdit)
        self.setWindowTitle("Log")

        screenGeo = QtWidgets.QDesktopWidget().screenGeometry()
        # print screenGeo
        self.resize(700, 300)
        self.move(screenGeo.width() - 800, 40)


def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    txt = data.encode('utf-8')
    return txt


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    sl = SystrayLauncher()
    sys.exit(app.exec_())
