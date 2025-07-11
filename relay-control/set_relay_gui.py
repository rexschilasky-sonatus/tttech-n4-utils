import tkinter as tk
from tkinter import ttk
import relay_help as rh

# Relay names
RELAY_NAMES = {
    1: "S23 Download Mode",
    2: "PMIC Debug Mode",
    3: "S32 JTAG Enable",
    4: "-",
    5: "KL30",
    6: "KL15",
    7: "-",
    8: "-"
}

# Find devices at startup
devices = rh.find_relay_devices()
if not devices:
    print("No relay devices found.")
    exit(1)

device_map = {}
for dev in devices:
    manufacturer = dev.get('manufacturer_string', '')
    if manufacturer == 'www.dcttech.com':
        for r in range(1, 5):
            device_map[r] = dev
    elif manufacturer == 'SNT-PWR':
        for r in range(5, 9):
            device_map[r] = dev

def get_all_states():
    states = {}
    for relay_num, dev_info in device_map.items():
        status = rh.get_relay_state(dev_info)
        if status:
            states[relay_num] = status[relay_num-1]
    return states

def toggle_relay(relay_num):
    current_state = relay_states.get(relay_num, False)
    new_state = not current_state
    dev_info = device_map.get(relay_num)
    if dev_info:
        rh.set_relay_state(dev_info, new_state, relay_num)
    update_states()

def update_states():
    global relay_states
    relay_states = get_all_states()
    for i in range(1, 9):
        state = relay_states.get(i, False)
        color = "green" if state else "gray"
        led_labels[i-1].config(background=color)

# Tkinter GUI
root = tk.Tk()
root.title("TTTech Relais Control")
#root.minsize(width=280, height=0)

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0)
mainframe.columnconfigure(0, pad=100)

# Buttons and LEDs
buttons = []
led_labels = []

for i in range(8):
    relay_num = i + 1
    name = RELAY_NAMES.get(relay_num, f"Relay {relay_num}")
    btn = ttk.Button(mainframe, text=name, command=lambda r=relay_num: toggle_relay(r))
    btn.grid(row=i, column=0, sticky="w", padx=5, pady=2)
    buttons.append(btn)

    led = tk.Label(mainframe, width=2, background="gray", relief="sunken")
    led.grid(row=i, column=1, padx=10)
    led_labels.append(led)

relay_states = {}
update_states()

root.mainloop()
