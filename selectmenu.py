import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMessageBox, QApplication, QMainWindow

from createtraining import createtrainclass
from qt_material import apply_stylesheet

form_class = uic.loadUiType("AiDetector1_init.ui")[0]
class MyApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_1.clicked.connect(self.createtraingbut)
        self.pushButton_2.clicked.connect(self.createtraingbut)
        self.pushButton_3.clicked.connect(self.createtraingbut)

    def createtraingbut(self):
        try:
            self.a = createtrainclass()  # aaaaa 클래스의 인스턴스 생성
            self.a.show()  # 생성된 인스턴스의 show() 메소드 호출
        except Exception as e:
            print(f"Error occurred: {e}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec()
