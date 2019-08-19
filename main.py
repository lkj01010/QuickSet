# -*- coding: UTF-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import sys
import os
import subprocess


class SystrayLauncher(object):

    def __init__(self):
        super(SystrayLauncher, self).__init__()

        self.logWin = LogWindow()

        w = QtWidgets.QWidget()  # just to get the style(), haven't seen other way
        # icon = w.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload)
        icon = QtGui.QIcon("/Users/Midstream/Documents/Art/MyIcons/quick_gray.png")
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray.activated.connect(self.customAction)

        # I JUST WANT TO SEE THE MENU WHEN RIGHT CLICK...
        menu = QtWidgets.QMenu()

        self.psAction = QtWidgets.QAction("Ps", None, triggered=self.psUx)
        menu.addAction(self.psAction)

        self.logAction = QtWidgets.QAction("Log", None, triggered=self.openLog)
        menu.addAction(self.logAction)

        self.quitAction = QtWidgets.QAction("Qui&t", None, triggered=QtWidgets.QApplication.instance().quit)
        menu.addAction(self.quitAction)

        # aQuit = menu.addAction("qqquit")
        # aQuit.triggered.connect(QtWidgets.QApplication.instance().quit)

        self.trayIconMenu = menu
        self.tray.setContextMenu(menu)

        self.log('remove_from_cache, user_uid=exist.')

    def openLog(self):
        self.logWin.show()

    def customAction(self, signal):
        print("left click pressed")

    def log(self, text):
        self.logWin.textEdit.append(text)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    sl = SystrayLauncher()
    sys.exit(app.exec_())
