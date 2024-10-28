from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtGui import QIcon
from network_capture import start_capture

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EtherApe Clone")
        self.setGeometry(100, 100, 800, 600)
        
        self.initUI()
        
    def initUI(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        # Interface selector
        self.interface_label = QLabel("Select Network Interface:", self)
        layout.addWidget(self.interface_label)
        self.interface_dropdown = QComboBox(self)
        self.interface_dropdown.addItems(["eth0", "eth1", "lo"])  # Populate with real interfaces
        layout.addWidget(self.interface_dropdown)

        # Protocol selector
        self.protocol_label = QLabel("Select Protocol:", self)
        layout.addWidget(self.protocol_label)
        self.protocol_dropdown = QComboBox(self)
        self.protocol_dropdown.addItems(["ALL", "IP", "TCP", "UDP"])
        layout.addWidget(self.protocol_dropdown)

        # Start capture button
        self.start_button = QPushButton("Start Capture", self)
        self.start_button.clicked.connect(self.start_capture)
        layout.addWidget(self.start_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_capture(self):
        interface = self.interface_dropdown.currentText()
        protocol = self.protocol_dropdown.currentText()
        start_capture(interface, protocol)
