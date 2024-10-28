# NetVine

This project is a scaffold for a basic EtherApe-like tool that uses Python and PyQt for network traffic visualization.

## Features
- Select network interface
- Choose protocols (IP, TCP, UDP, ALL)

## Setup

### Requirements
- Python 3.7+
- PyQt5
- pyshark
- **Wireshark with tshark**: Required for packet capture. Download Wireshark from [https://www.wireshark.org/download.html].

### Installation Instructions
1. **Install Python Packages**: Run the following to install required Python libraries.
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Wireshark**: During installation, make sure to select the option to add `tshark` to your PATH.

3. **Verify tshark Installation**:
   - Open a command prompt and type `tshark -v`. You should see version information if it’s correctly installed.
   - If `tshark` is installed in a custom path, you may need to specify it directly in `network_capture.py`.

4. **Running the Application**:
   - After installing the dependencies and verifying `tshark`, run the application with:
     ```bash
     python __main__.py
     ```

### Troubleshooting
- **TSharkNotFoundException**: If you receive this error, it means `tshark` was not found. Verify its PATH or specify its exact path in `network_capture.py`:
    ```python
    capture = pyshark.LiveCapture(interface=interface, display_filter=protocol.lower(), tshark_path="C:\Path\To\tshark.exe")
    ```

### Notes
- **PyQt5 GUI**: The GUI uses basic PyQt5 components with a `QGraphicsView` setup for future node-based visualization.

- **Project Layout**:
  - `__main__.py`: Main entry point for running the application.
  - `network_capture.py`: Placeholder for network capture functionality.
  - `ui_main.py`: Main GUI setup using PyQt.
  - `requirements.txt`: Python packages required for the project.
