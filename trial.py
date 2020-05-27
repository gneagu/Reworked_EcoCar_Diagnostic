from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
import sys

# https://stackoverflow.com/q/46392787
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel('Введите слова')
        words = QTextEdit()

        label2 = QLabel('Результат')
        result = QTextEdit()

        vbox1 = QVBoxLayout()
        # vbox1.addStretch(1)
        vbox1.addWidget(label1)
        vbox1.addWidget(words)

        vbox2 = QVBoxLayout()
        # vbox2.addStretch(1)
        vbox2.addWidget(label2)
        vbox2.addWidget(result)

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        self.setLayout(hbox)


        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('try')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())