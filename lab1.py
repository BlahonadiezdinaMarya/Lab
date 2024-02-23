import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from math import sin, cos

def calculate_function_value():
    selected_function = function_selector.currentText()
    point = float(point_input.text())
    
    if selected_function == "2sin(x) - cos(x)":
        result = 2 * sin(point) - cos(point)
    elif selected_function == "(2^x + 10) / 4 + 9 / 2^(x - 2)":
        result = (2**point + 10) / 4 + 9 / 2**(point - 2)
    else:
        result = None
    
    if result is not None:
        result_label.setText(f"Результат обчислення {selected_function} в точці {point}: {result}")
    else:
        result_label.setText("Невірно вибрана функція")


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Обчислення значення функції')
layout = QVBoxLayout()

function_selector = QComboBox()
function_selector.addItems(["2sin(x) - cos(x)", "(2^x + 10) / 4 + 9 / 2^(x - 2)"])
layout.addWidget(function_selector)

point_input = QLineEdit()
point_input.setPlaceholderText("Введіть точку")
layout.addWidget(point_input)

calculate_button = QPushButton("Обчислити")
calculate_button.clicked.connect(calculate_function_value)
layout.addWidget(calculate_button)

result_label = QLabel()
layout.addWidget(result_label)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
