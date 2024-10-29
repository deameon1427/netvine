import pyshark
import subprocess
import re

def get_windows_interfaces():
    """
    Uses netsh to retrieve available network interfaces on Windows.
    """
    interfaces = []
    try:
        # Run netsh command to get network interface list
        output = subprocess.check_output("netsh interface show interface", shell=True, text=True)
        
        # Regex to capture interface names from the output
        matches = re.findall(r'^\s*Enabled\s+\S+\s+\S+\s+(.*)$', output, re.MULTILINE)
        interfaces = [match.strip() for match in matches]
    except Exception as e:
        print(f"Failed to retrieve interfaces with netsh: {e}")
    
    return interfaces

def get_available_interfaces():
    """
    Retrieves a list of available network interfaces for capturing.
    """
    interfaces = get_windows_interfaces()
    if not interfaces:
        # Fallback to pyshark if netsh fails
        try:
            capture = pyshark.LiveCapture()
            interfaces = capture.interfaces
        except Exception as e:
            print(f"Error retrieving interfaces: {e}")
    
    return interfaces

def start_capture(interface, protocol, packet_callback):
    """
    Starts a network capture on the specified interface with the given protocol.
    Calls packet_callback for each packet captured.
    """
    try:
        capture = pyshark.LiveCapture(interface=interface, bpf_filter=protocol)
        print(f"Starting capture on interface: {interface} with protocol: {protocol}")
        
        # Capture packets in real time and invoke callback
        for packet in capture.sniff_continuously():
            packet_callback(packet)

    except pyshark.capture.live_capture.UnknownInterfaceException:
        print(f"Interface '{interface}' does not exist or lacks permissions.")
    except Exception as e:
        print(f"An error occurred during capture: {e}")
