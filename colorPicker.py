# -*- coding: UTF-8 -*-

import sys, os, threading
import math
from midlog import log

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtOpenGL import *

# from pynput.keyboard import Controller, Key, Listener
import pynput.keyboard as keyboard
import pynput.mouse as mouse

# import logging as log
#
# log.basicConfig(level=log.DEBUG,
#                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 handlers={log.FileHandler(filename='test.log', mode='a', encoding='utf-8')})
#
# log.debug('-----调试信息[debug]-----')
# log.info('-----有用的信息[info]-----')
# log.warning('-----警告信息[warning]-----')
# log.error('-----错误信息[error]-----')
# log.critical('-----严重错误信息[critical]-----')

# import colorlog
# from colorlog import ColoredFormatter
#
# handler = colorlog.StreamHandler()
#
# formatter = ColoredFormatter(
#     "%(log_color)s%(asctime)s (%(module)s:%(lineno)d) %(levelname)-8s%(reset)s %(message_log_color)s%(message)s ",
#     datefmt="%y/%m/%d %H:%M:%S",
#     reset=True,
#     log_colors={
#         'DEBUG': 'white',
#         'INFO': 'white',
#         'WARNING': 'white',
#         'ERROR': 'white',
#         'CRITICAL': 'black,bg_white',
#     },
#     secondary_log_colors={
#         'message': {
#             'DEBUG': 'blue',
#             'INFO': 'cyan',
#             'WARNING': 'yellow',
#             'ERROR': 'red',
#             'CRITICAL': 'red'
#         }
#     },
#     style='%'
# )
# handler.setFormatter(formatter)
#
# logger = colorlog.getLogger('example')
# logger.addHandler(handler)
# logger.setLevel('DEBUG')


try:
    from OpenGL import GL
except ImportError:
    app = QApplication(sys.argv)
    messageBox = QMessageBox(QMessageBox.Critical, "OpenGL 2dpainting",
                             "PyOpenGL must be installed to run this example.",
                             QMessageBox.Close)
    messageBox.setDetailedText("Run:\npip install PyOpenGL PyOpenGL_accelerate")
    messageBox.exec_()
    sys.exit(1)


class Helper:
    def __init__(self):
        gradient = QLinearGradient(QPointF(50, -20), QPointF(80, 20))
        gradient.setColorAt(0.0, Qt.white)
        gradient.setColorAt(1.0, QColor(0xa6, 0xce, 0x39))

        self.background = QBrush(QColor(64, 32, 64))
        self.circleBrush = QBrush(gradient)
        self.circlePen = QPen(Qt.black)
        self.circlePen.setWidth(1)
        self.textPen = QPen(Qt.white)
        self.textFont = QFont()
        self.textFont.setPixelSize(50)

    def paint(self, painter, event, elapsed):
        painter.fillRect(event.rect(), self.background)
        painter.translate(100, 100)

        painter.save()
        painter.setBrush(self.circleBrush)
        painter.setPen(self.circlePen)
        painter.rotate(elapsed * 0.030)

        r = elapsed / 1000.0
        n = 30
        for i in range(n):
            painter.rotate(30)
            radius = 0 + 120.0 * ((i + r) / n)
            circleRadius = 1 + ((i + r) / n) * 20
            painter.drawEllipse(QRectF(radius, -circleRadius,
                                       circleRadius * 2, circleRadius * 2))

        painter.restore()

        painter.setPen(self.textPen)
        painter.setFont(self.textFont)
        painter.drawText(QRect(-50, -50, 100, 100), Qt.AlignCenter, "Qt")


class Widget(QWidget):
    def __init__(self, helper, parent=None):
        QWidget.__init__(self, parent)

        self.helper = helper
        self.elapsed = 0
        self.setFixedSize(200, 200)

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()


class GLWidget(QGLWidget):
    def __init__(self, helper, parent=None):
        QGLWidget.__init__(self, QGLFormat(QGL.SampleBuffers), parent)

        self.helper = helper
        self.elapsed = 0
        self.setFixedSize(200, 200)

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()

    # class Useful(object):
    def code1(self):
        x = 200
        y = 200
        winId = QApplication.desktop().winId()

        screen = QGuiApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        pixmap.save("image.png")
        # pixmap = QPixmap.grabWindow(0)
        # pixmap = QPixmap.grabWindow(0, x, y, 1, 1)
        # QRgb
        # pixelValue = pixmap.toImage().pixel(0, 0)
        # return pixelValue

        # shortcut = QShortcut(QKeySequence(Qt.Key_F1), QApplication.desktop())
        shortcut = QShortcut(QKeySequence(Qt.Key_F1), self)
        shortcut.setContext(Qt.ApplicationShortcut)
        shortcut.activated.connect(self.handler)

        # https://my.oschina.net/zjuysw/blog/496949

    def handler(self):
        print("short cut press" + str(self.elapsed))
        return


class ListenKeyThread(QThread):
    ColormapSize = 512

    signal = Signal(QImage, float)

    def __init__(self, parent=None):
        super(ListenKeyThread, self).__init__(parent)

        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.centerX = 0.0
        self.centerY = 0.0
        self.scaleFactor = 0.0
        self.resultSize = QSize()
        self.colormap = []

        self.restart = False
        self.abort = False

    def run(self):
        # i = 0
        # while True:
        #     i += 1
        listenKeyboard()


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        helper = Helper()
        native = Widget(helper, self)
        openGL = GLWidget(helper, self)
        nativeLabel = QLabel(self.tr("Native"))
        nativeLabel.setAlignment(Qt.AlignHCenter)
        openGLLabel = QLabel(self.tr("OpenGL"))
        openGLLabel.setAlignment(Qt.AlignHCenter)

        layout = QGridLayout()
        layout.addWidget(native, 0, 0)
        layout.addWidget(openGL, 0, 1)
        layout.addWidget(nativeLabel, 1, 0)
        layout.addWidget(openGLLabel, 1, 1)
        self.setLayout(layout)

        # pixmap = native.grab()
        # pixmap.save("image.png")

        openGL.code1()

        # i = 0
        # while True:
        #     i += 1

        # !!! 可以不阻塞主线程！！！Wonderful !
        self.thread = ListenKeyThread()
        self.thread.signal.connect(self.updatePixmap)
        self.thread.start()

        # !!! 如果死循环，cpu可以到200%以上，应该是可以利用多核！！！
        # self.t2 = ListenKeyThread()
        # self.t2.start()
        #
        # self.t3 = ListenKeyThread()
        # self.t3.start()

        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), native.animate)
        self.connect(timer, SIGNAL("timeout()"), openGL.animate)
        timer.start(20)

        self.setWindowTitle(self.tr("2D Painting on Native and OpenGL Widgets"))

    def updatePixmap(self, image, scaleFactor):
        return


def xxx():
    print("x")


# 监听按压
def on_press(key):
    try:
        # print((u"正在按压:").encode('utf-8'), format(key.char))
        log.debug("this is a debugging message")
        log.info("this is an informational message")
        log.warning("this is a warning message")
        log.error("this is an error message")
        log.critical("this is a critical message")
        # print("\033[1;37;40m Bright Colour\033[0;37;40m \n")

    except AttributeError:
        print((u"正在按压:").encode('utf-8'), format(key))


# 监听释放
def on_release(key):
    print(u"已经释放:", format(key))

    if key == keyboard.Key.esc:
        # 停止监听
        return False


# 开始监听
def start_listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def listenKeyboard():
    kb = keyboard.Controller()

    # 使用键盘输入一个字母
    # kb.press('a')
    # kb.release('a')

    # 使用键盘输入字符串hello world ,注意当前键盘调成英文
    # kb.type("hello world")

    # 使用Key.xxx输入
    # kb.press(Key.space)

    # 开始监听,按esc退出监听
    start_listen()


# def app():
#     app = QApplication(sys.argv)
#
#     # Useful().code1()
#
#     window = Window()
#
#     # w = QWidget(window)
#     # shortcut = QShortcut(QKeySequence(Qt.Key_F12), w)
#     # shortcut.activated.connect(xxx)
#     # window.setWindowFlags(Qt.WindowStaysOnTopHint)
#
#     window.show()
#     # sys.exit(app.exec_())
#
#     app.exec_()


if __name__ == '__main__':
    # t1 = threading.Thread(target=listenKeyboard, name='LoopThread')
    # t1.start()
    # t1.join()

    app = QApplication(sys.argv)
    window = Window()

    # w = QWidget(window)
    # shortcut = QShortcut(QKeySequence(Qt.Key_F12), w)
    # shortcut.activated.connect(xxx)
    # window.setWindowFlags(Qt.WindowStaysOnTopHint)

    window.show()
    sys.exit(app.exec_())
