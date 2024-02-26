import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class StudentInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information about student")
        self.setGeometry(200, 200, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        full_name_label = QLabel("Blahonadiezhdina Marya Andriivna")
        full_name_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(full_name_label)

        group_label = QLabel("К121-20")
        group_label.setStyleSheet("color: purple; font-style: italic;")
        layout.addWidget(group_label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentInfo()
    window.show()
    sys.exit(app.exec_())
