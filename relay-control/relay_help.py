import sys
import hid

def find_relay_devices():
    """Find USB relay devices matching common VID/PID"""
    devices = []
    for d in hid.enumerate():
        if d['vendor_id'] == 0x16C0 and d['product_id'] == 0x05DF:
            print(f"Found: {d['product_string']} (Serial: {d['serial_number']})")
            devices.append(d)
    return devices

def set_relay_state(device_info, is_on, relay_num):
    try:
        dev = hid.device()
        dev.open_path(device_info['path'])

        report = [0x00] * 9  # Report ID + 8 data bytes
        if 1 <= relay_num <= 8:
            if is_on:
                report[1] = 0xFF
            else:
                report[1] = 0xFD
            report[2] = relay_num
        else:
            print("Relay number must be 1-8")
            return

        bytes_written = dev.send_feature_report(report)
        print(f"Sent feature report: {report}, bytes written: {bytes_written}")

        dev.close()
    except Exception as e:
        print(f"Error sending relay command: {e}")

def get_relay_state(device_info):
    """
    Reads the current status of the relays (bitmask).
    Returns a list of bools, one per relay (True = on, False = off).
    """
    try:
        dev = hid.device()
        dev.open_path(device_info['path'])

        # Read a 9-byte Feature Report (Report ID 0x00)
        report = dev.get_feature_report(0x00, 9)
        dev.close()

        #print(f"Raw feature report: {list(report)}")

        if not report or len(report) < 3:
            print("Invalid status response from device.")
            return None

        # report[8] contains the relay status bitmask
        bitmask = report[8]

        status = []
        for i in range(8):
            status.append(bool(bitmask & (1 << i)))

        return status

    except Exception as e:
        print(f"Error while reading relay status: {e}")
        return None

def print_relay_states(device_info, relays_to_show=None, relay_names=None):
    """
    Prints the relay states of the specified device.
    Optionally only prints specified relay numbers.
    """
    status = get_relay_state(device_info)
    if status is None:
        print(f"Could not read status from device: {device_info['product_string']} ({device_info['serial_number']})")
        return

    print(f"Device: {device_info['product_string']} ({device_info['serial_number']})")
    relays_to_show = relays_to_show or range(1, 9)
    for i in relays_to_show:
        state_str = "ON" if status[i-1] else "OFF"
        name_str = f"\t{relay_names[i]}" if relay_names and i in relay_names else ""
        print(f"  Relay {i}: {state_str}{name_str}")
