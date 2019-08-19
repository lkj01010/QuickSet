from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QStyle, QApplication, QAction, QMenu, QSystemTrayIcon, \
    QMessageBox
from pkg_resources import require, DistributionNotFound, resource_filename
import sys

def about():
    pass

def status():
    pass

def client():
    pass

def stop():
    pass

def customAction(signal):
    print "left click pressed"

def main():
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    # Create the tray
    # tray = QSystemTrayIcon(QIcon(resource_filename("application.server",
    #                                                "res/bolt.png")))

    w = QWidget()  # just to get the style(), haven't seen other way
    icon = w.style().standardIcon(QStyle.SP_MessageBoxInformation)
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.activated.connect(customAction)

    menu = QMenu()
    controls = []

    controls.append(QAction("About"))
    controls[-1].triggered.connect(about)
    menu.addAction(controls[-1])

    controls.append(QAction("Check Status"))
    controls[-1].triggered.connect(status)
    menu.addAction(controls[-1])

    menu.addSeparator()

    controls.append(QAction("Launch client"))
    controls[-1].triggered.connect(client)
    menu.addAction(controls[-1])

    controls.append(QAction("Stop Server"))
    controls[-1].triggered.connect(stop)
    menu.addAction(controls[-1])

    # Add the menu to the tray
    tray.setContextMenu(menu)
    tray.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()