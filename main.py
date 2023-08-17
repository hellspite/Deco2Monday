# Python script to export orders from DecoNetwork into Monday tasks
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QStatusBar,
                             QDesktopWidget)
from PyQt5 import QtCore

import sys
import deco
import monday

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Deco2Monday")
    window.setMinimumWidth(600)
    window.setMinimumHeight(130)
    rect = window.frameGeometry()
    screen_center = QDesktopWidget().availableGeometry(window).center()
    rect.moveCenter(screen_center)
    window.move(rect.topLeft())

    layout = QVBoxLayout()
    first_label_text = "Applicazione per importare ordini da Deco in Monday"
    first_label = QLabel(first_label_text)
    first_label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(first_label)
    layout.addStretch()

    second_label_text = "Quanti giorni vuoi andare indietro nella ricerca degli ordini?"
    second_label = QLabel(second_label_text)
    layout.addWidget(second_label)

    h_layout = QHBoxLayout()
    h_layout.addStretch()
    spin_box = QSpinBox()
    spin_box.setMinimum(1)
    spin_box.setMaximum(14)
    spin_box.setValue(14)

    h_layout.addWidget(spin_box)

    status_bar = QStatusBar()

    import_btn = QPushButton("Importa ordini")


    def import_orders():
        status_bar.showMessage("Importazione in corso...")
        window.repaint()
        days_back = spin_box.value()
        orders = deco.get_orders(days_back)
        print(f"Number of orders retrieved from Deco: {len(orders)}")
        monday.write_new_orders(orders)
        status_bar.showMessage("Eventuali nuovi ordini sono stati importati", 10000)


    import_btn.clicked.connect(import_orders)
    h_layout.addWidget(import_btn)

    h_layout.addStretch()

    layout.addLayout(h_layout)

    layout.addWidget(status_bar)

    window.setLayout(layout)
    window.show()

    app.exec()
