from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QDockWidget, QWidget, QLabel, QStatusBar, QDialog, QDialogButtonBox, QFormLayout, QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyshark
import asyncio

# Modal dialog for interface and protocol selection
class StartupDialog(QDialog):
    def __init__(self, interfaces, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Interface and Mode")
        self.setModal(True)
        
        # Form layout
        layout = QFormLayout(self)
        
        # Interface selector
        self.interface_combo = QComboBox()
        self.interface_combo.addItems(interfaces)
        layout.addRow("Select Interface:", self.interface_combo)
        
        # Protocol selector
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["ALL", "TCP", "UDP", "ICMP"])
        layout.addRow("Select Protocol:", self.protocol_combo)
        
        # OK/Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def get_selections(self):
        return self.interface_combo.currentText(), self.protocol_combo.currentText()

# CaptureThread to run packet capture in background
class CaptureThread(QThread):
    packet_received = pyqtSignal(object)

    def __init__(self, interface, protocol):
        super().__init__()
        self.interface = interface
        self.protocol = protocol
        self.running = True
        self.capture = None  # Capture object

    def run(self):
        # Create an event loop for the thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self.capture_packets())
        finally:
            self.loop.close()

    async def capture_packets(self):
        """
        Asynchronous packet capture using pyshark.
        Emits `packet_received` for each packet.
        """
        self.capture = pyshark.LiveCapture(interface=self.interface, bpf_filter=self.protocol)

        # Run sniff_continuously in an executor
        with self.capture:
            await self.loop.run_in_executor(None, self.sniff_packets)

    def sniff_packets(self):
        """
        Synchronous packet capture loop.
        """
        for packet in self.capture.sniff_continuously():
            if not self.running:
                break
            self.packet_received.emit(packet)

    def stop(self):
        self.running = False
        if self.capture:
            self.capture.close()  # Ensure capture is closed
        self.quit()
        self.wait()

# Graph canvas for visualizing the network graph
class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure, self.ax = plt.subplots()
        super().__init__(self.figure)
        self.setParent(parent)

    def draw_graph(self, graph):
        self.ax.clear()
        nx.draw(graph, ax=self.ax, with_labels=True, node_color="red", edge_color="blue")
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self, interface, protocol, parent=None):
        super().__init__(parent)
        
        # Store selected interface and protocol
        self.interface = interface
        self.protocol = protocol
        
        # Set up the main window
        self.setWindowTitle("NetVine - Network Interface Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Graph Canvas
        self.graph_canvas = GraphCanvas(self)
        
        # Toolbar setup
        self.setup_toolbar()
        
        # Status bar
        self.setStatusBar(QStatusBar(self))
        
        # Populate the central widget with the graph view
        self.setCentralWidget(self.graph_canvas)

        # Dock widgets for preferences and protocol data
        self.setup_docks()

        # Initialize an empty network graph
        self.network_graph = nx.Graph()
        
        # Initialize the capture thread
        self.capture_thread = CaptureThread(self.interface, self.protocol)
        self.capture_thread.packet_received.connect(self.packet_callback)

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        start_action = QAction("Start", self)
        start_action.triggered.connect(self.start_capture)
        toolbar.addAction(start_action)

        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_capture)
        toolbar.addAction(stop_action)

        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.show_preferences)
        toolbar.addAction(preferences_action)

    def setup_docks(self):
        self.preferences_dock = QDockWidget("Preferences", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.preferences_dock)
        
        preferences_widget = QWidget()
        self.preferences_dock.setWidget(preferences_widget)

        self.protocols_dock = QDockWidget("Protocols", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.protocols_dock)
        
        protocols_widget = QLabel("Protocol data here")
        self.protocols_dock.setWidget(protocols_widget)

    def show_preferences(self):
        self.preferences_dock.show()

    def start_capture(self):
        """
        Starts the capture thread.
        """
        self.capture_thread.start()
        self.statusBar().showMessage(f"Capture started on {self.interface} with protocol {self.protocol}")

    def stop_capture(self):
        """
        Stops the capture thread.
        """
        self.capture_thread.stop()
        self.statusBar().showMessage("Capture stopped")

    def packet_callback(self, packet):
        """
        Processes each captured packet and updates the graph.
        """
        try:
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            print(f"Packet: {src_ip} -> {dst_ip}")  # Debug output

            if not self.network_graph.has_edge(src_ip, dst_ip):
                self.network_graph.add_edge(src_ip, dst_ip)
                self.graph_canvas.draw_graph(self.network_graph)
        except AttributeError:
            pass
