import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import SIGNAL
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QSizePolicy
from scapy.all import sr1, IP, ICMP


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.expandPolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.expandPolicy.setHorizontalStretch(0)
        self.expandPolicy.setVerticalStretch(0)

        self.button = QtWidgets.QPushButton("Click me!")

        self.button01 = QtWidgets.QPushButton("Click me!")
        self.button01.setFixedSize(50, 50)

        self.input = QtWidgets.QPlainTextEdit(self)
        self.input.resize(200, 100)

        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button01)

        #Définie le positionnement
        self.httpWidget = QtWidgets.QWidget(self)
        self.httpWidget.setLayout(self.layout)
        self.httpWidget.setSizePolicy(self.expandPolicy)
        self.httpWidget.resize(self.width(), self.height())

        #Affiche les onglets
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setSizePolicy(self.expandPolicy)
        self.tabs.resize(self.width(), self.height())
        self.tabs.addTab(self.httpWidget, "HTTP")
        self.tabs.addTab(QtWidgets.QWidget(self), "ARP")
        self.tabs.addTab(QtWidgets.QWidget(self), "DNS")

        self.button.clicked.connect(self.magic)
        self.button01.clicked.connect(self.start01)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(self.input.toPlainText())

    @QtCore.Slot()
    def start01(self):
        p = sr1(IP(dst="192.168.1.1") / ICMP())
        if p:
            self.text.setText(p.sprintf(
                "--IP Layer-- \n"
                "Timestamps : %.time% \n"
                "Source IP : %IP.src% \n"
                "Destination IP : %IP.dst% \n"
                "Checksum %IP.chksum% \n"
                "%03xr,IP.proto% %r,TCP.type% \n"
                "--ICMP Layer-- \n"
                "Type : %ICMP.type% \n"
                "Code : %ICMP.code% \n"
                "ID : %ICMP.id% \n"
                "Seq : %ICMP.seq% \n"
                "Unused : %ICMP.unused% \n"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
