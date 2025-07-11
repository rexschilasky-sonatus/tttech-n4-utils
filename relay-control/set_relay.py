import sys
import hid
import relay_help as rh

def main():
    if len(sys.argv) != 3:
        print("Usage: python relay_control.py <ON/OFF> <relay_num>")
        sys.exit(1)

    action = sys.argv[1].upper()
    try:
        relay_num = int(sys.argv[2])
    except ValueError:
        print("Relay number must be an integer.")
        sys.exit(1)

    if not (1 <= relay_num <= 8):
        print("Relay number must be between 1 and 8.")
        sys.exit(1)

    print("")
    devices = rh.find_relay_devices()
    if not devices:
        print("No relay devices found.")
        sys.exit(1)

    print("")
    print("-----------------")
    print("Set Relais State:")
    print("-----------------")
    is_on = (action == "ON")
    for dev_info in devices:
        if not ((dev_info['manufacturer_string'] == 'SNT-PWR' and relay_num < 5) or (dev_info['manufacturer_string'] == 'www.dcttech.com' and relay_num > 4)):
            rh.set_relay_state(dev_info, is_on, relay_num)

    print("")
    print("-----------------")
    print("Get Relais State:")
    print("-----------------")
    relay_names_dict= {
        1: "S23 Download Mode",
        2: "PMIC Debug Mode",
        3: "S32 JTAG Enable",
        4: "-",
        5: "KL30",
        6: "KL15",
        7: "-",
        8: "-",
        }
    for dev_info in devices:
        manufacturer = dev_info.get('manufacturer_string', '')
        if manufacturer == 'www.dcttech.com':
            rh.print_relay_states(dev_info, relays_to_show=range(1, 5), relay_names=relay_names_dict)
        elif manufacturer == 'SNT-PWR':
            rh.     print_relay_states(dev_info, relays_to_show=range(5, 9), relay_names=relay_names_dict)
        else:
            print(f"Unknown manufacturer: {manufacturer}")
    
if __name__ == "__main__":
    main()
