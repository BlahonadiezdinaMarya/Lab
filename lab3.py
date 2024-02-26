import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from math import sin, cos

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.points = []
        self.color = Qt.blue
        self.line_width = 2

    def set_points(self, points):
        self.points = points
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def set_line_width(self, width):
        self.line_width = width
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(self.color)
        pen.setWidth(self.line_width)
        painter.setPen(pen)

        if len(self.points) < 2:
            return

        width = self.width()
        height = self.height()

        x_scale = width / (self.points[-1][0] - self.points[0][0])
        y_scale = height / (max(self.points, key=lambda p: p[1])[1] - min(self.points, key=lambda p: p[1])[1])

        scaled_points = [(round((p[0] - self.points[0][0]) * x_scale), round(height - (p[1] - min(self.points, key=lambda p: p[1])[1]) * y_scale)) for p in self.points]

        for i in range(len(scaled_points) - 1):
            painter.drawLine(scaled_points[i][0], scaled_points[i][1], scaled_points[i + 1][0], scaled_points[i + 1][1])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор функцій")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.function_label = QLabel("Оберіть функцію:")
        self.layout.addWidget(self.function_label)

        self.function_combo = QComboBox()
        self.function_combo.addItems(["2sin(x) - cos(x)", "(2^x + 10) / 4 + 9 / 2^(x-2)"])
        self.layout.addWidget(self.function_combo)

        self.start_label = QLabel("Початок інтервалу:")
        self.layout.addWidget(self.start_label)

        self.start_input = QLineEdit()
        self.layout.addWidget(self.start_input)

        self.end_label = QLabel("Кінець інтервалу:")
        self.layout.addWidget(self.end_label)

        self.end_input = QLineEdit()
        self.layout.addWidget(self.end_input)

        self.num_points_label = QLabel("Кількість точок:")
        self.layout.addWidget(self.num_points_label)

        self.num_points_input = QLineEdit()
        self.layout.addWidget(self.num_points_input)

        self.color_label = QLabel("Колір графіку:")
        self.layout.addWidget(self.color_label)

        self.color_combo = QComboBox()
        self.color_combo.addItems(["Червоний", "Зелений", "Синій", "Чорний"])
        self.layout.addWidget(self.color_combo)

        self.line_width_label = QLabel("Товщина лінії:")
        self.layout.addWidget(self.line_width_label)

        self.line_width_input = QLineEdit()
        self.layout.addWidget(self.line_width_input)

        self.calculate_button = QPushButton("Обчислити")
        self.calculate_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calculate_button)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.graph_widget = GraphWidget()
        self.layout.addWidget(self.graph_widget)

    def calculate(self):
        selected_function = self.function_combo.currentText()
        start = self.start_input.text()
        end = self.end_input.text()
        num_points = self.num_points_input.text()

        points, values, error = calculate_function_values(selected_function, start, end, num_points)

        if error:
            QMessageBox.warning(self, "Помилка", error)
            return

        self.table.setRowCount(len(points))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["x", "f(x)"])

        for i, (x, y) in enumerate(zip(points, values)):
            self.table.setItem(i, 0, QTableWidgetItem(str(x)))
            self.table.setItem(i, 1, QTableWidgetItem(str(y)))

        self.graph_widget.set_points(list(zip(points, values)))

        color_dict = {"Червоний": Qt.red, "Зелений": Qt.green, "Синій": Qt.blue, "Чорний": Qt.black}
        selected_color = color_dict.get(self.color_combo.currentText(), Qt.blue)
        self.graph_widget.set_color(selected_color)

        line_width = int(self.line_width_input.text())
        self.graph_widget.set_line_width(line_width)


def calculate_function_values(selected_function, start, end, num_points):
    try:
        start = float(start)
        end = float(end)
        num_points = int(num_points)
        
        if start >= end:
            raise ValueError("Початкове значення повинно бути менше за кінцеве.")
        
        if num_points < 2:
            raise ValueError("Кількість точок повинна бути 2 або більше.")
        
        step = (end - start) / (num_points - 1)
        points = [start + step * i for i in range(num_points)]
        
        if selected_function == "2sin(x) - cos(x)":
            values = [2 * sin(x) - cos(x) for x in points]
        elif selected_function == "(2^x + 10) / 4 + 9 / 2^(x-2)":
            values = [(2**x + 10) / 4 + 9 / 2**(x-2) for x in points]
        else:
            raise ValueError("Обрана неправильна функція.")
        
        return points, values, None
    except Exception as e:
        return None, None, str(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
