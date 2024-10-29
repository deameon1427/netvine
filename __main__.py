from PyQt5.QtWidgets import QApplication, QDialog
from ui_main import MainWindow, StartupDialog
from network_capture import get_available_interfaces
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Get available interfaces and show the startup dialog
    interfaces = get_available_interfaces()
    dialog = StartupDialog(interfaces)
    if dialog.exec_() == QDialog.Accepted:
        selected_interface, selected_protocol = dialog.get_selections()
        
        # Pass the selected interface and protocol to the main window
        main_window = MainWindow(selected_interface, selected_protocol)
        main_window.show()
        
    sys.exit(app.exec_())
