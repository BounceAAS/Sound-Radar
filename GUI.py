import sys
from pyqt_frameless_window import FramelessMainWindow
from PyQt5.QtWidgets import QApplication, QTextEdit, QDesktopWidget

class Window(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()
    def __initUi(self):
        self.setWindowTitle('SoundRadar')
        self.setWindowIcon('./Stark-icon.png')
        self.setTitleBarVisible(False)

        mainWidget = self.centralWidget()
        lay = mainWidget.layout()
        lay.addWidget(QTextEdit())
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

        screen_geometry = QDesktopWidget().screenGeometry()
        self.move((screen_geometry.width() - self.width()) // 2, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.resize(1200, 50)
    sys.exit(app.exec())