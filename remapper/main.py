# Copyright 2024-2026 Joel Goh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import threading
import evdev
import json

from remapper import Remapper
from keyboard import *
from touchpad import *
from gamepad import *
from wdi_report import *

from API import create_app, load_state_from_settings

class AppState():
    def __init__(self):
        self.STATE = 1
        self.devices = []
        self.inputs = {'NONE': 1,
                       'Keyboard': 0,
                       'GP': 0,
                       'Sip-n-Puff': 0}

        self.input_options = {
            'NONE': [],
            'Keyboard': [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/', '`',
                'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                'up', 'down', 'left', 'right',
                'space', 'enter', 'backspace', 'tab', 'esc', 'caps',
                'delete', 'insert', 'home', 'end', 'page up', 'page down',
                'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9',
                'num enter', 'num plus', 'num minus', 'num multiply', 'num divide', 'num dot', 'num comma', 'num equal', 'num lock',
                'left shift', 'right shift', 'left ctrl', 'right ctrl', 'left alt', 'right alt', 'left meta', 'right meta'
            ],
            'GP': ['BTN_NORTH', 'BTN_SOUTH', 'BTN_EAST', 'BTN_WEST', "BTN_START", "BTN_SELECT", "BTN_MODE",
                    "BTN_TL", "BTN_TR", "BTN_TL2", "BTN_TR2",
                    "POS_ABS_X", "POS_ABS_Y", "POS_ABS_RX", "POS_ABS_RY",
                    "NEG_ABS_X", "NEG_ABS_Y", "NEG_ABS_RX", "NEG_ABS_RY",
                    "DPAD_UP", "DPAD_DOWN", "DPAD_LEFT", "DPAD_RIGHT", "BTN_THUMBL", "BTN_THUMBR",
                    "BTN_TRIGGER_HAPPY1", "BTN_TRIGGER_HAPPY2", "BTN_TRIGGER_HAPPY3", "BTN_TRIGGER_HAPPY4",
                    "BTN_TRIGGER_HAPPY5", "BTN_TRIGGER_HAPPY6", "BTN_TRIGGER_HAPPY7", "BTN_TRIGGER_HAPPY8",
                    "BTN_TRIGGER_HAPPY9", "BTN_TRIGGER_HAPPY10", "BTN_TRIGGER_HAPPY11", "BTN_TRIGGER_HAPPY12",
                    "BTN_TRIGGER_HAPPY13", "BTN_TRIGGER_HAPPY14", "BTN_TRIGGER_HAPPY15", "BTN_TRIGGER_HAPPY16",
                    ],
            'Sip-n-Puff': ["Soft Sip", "Hard Sip", "Soft Puff", "Hard Puff"]
        }
        self.settings = {
            'Drive': None,
            'Chair': None,
            'Profile': None,
            'Memory': None,
            'Seating': None
        }

def list_devices(state):
    state.devices = []
    for path in evdev.list_devices():
        d = evdev.InputDevice(path)
        state.devices.append([d.name, d.path, 0])
        d.close()

def create_remapper(state, settings_path):
    device = None
    for d in state.devices:
        if d[2] == 1:
            device = d[1]
            break
    if device is not None:
        return make_remapper(device, state, settings_path)
    else:
        raise ValueError("No active device found")

def make_remapper(device_id, state, settings_path):
    input = [k for k, v in state.inputs.items() if v == 1][0]
    if input == "Keyboard":
        return Keyboard(device_id, state, settings_path)
    elif input == "GP":
        return Gamepad(device_id, state, settings_path)
    elif input == "Sip-n-Puff":
        return Touchpad(device_id, state, settings_path)
    else:
        raise ValueError("Invalid input type")
    
if __name__ == "__main__":
    state = AppState()
    list_devices(state)

    try:
        load_state_from_settings(state, "settings.json")
    except FileNotFoundError:
        pass
    app = create_app(state, "settings.json")

    host = os.environ.get("REMAPPER_HOST", "0.0.0.0")
    port = int(os.environ.get("REMAPPER_PORT", "5000"))
    flask_thread = threading.Thread(target=lambda: app.run(
        host=host, port=port, debug=False, use_reloader=False, threaded=True),
        daemon=True)

    flask_thread.start()

    r = None
    while True:
        STATE = state.STATE
        # No Transition
        if r is None:
            if STATE == 1:
                active = [k for k, v in state.inputs.items() if v == 1][0]
                if active != "NONE":
                    if any(d[2] == 1 for d in state.devices):
                        try:
                            print(f"Initializing {active} Remapper...")
                            r = create_remapper(state, "settings.json")
                        except ValueError as e:
                            print(f"Error creating remapper: {e}")
                            r = None
            continue

        if r.current_STATE == STATE:
            if STATE == 1:
                r.RUN()
            elif STATE == 0:
                r.CONFIGURE()

        else:
            if r.current_STATE == 1 and STATE == 0:
                print("RUNNING --> CONFIGURING")
                r.write_report(get_wdi_report(["Disable Device Control"]))
                r.write_report(bytes([0x00]) * 8)

                selected_device = next((d for d in state.devices if d[2] == 1), None)
                if selected_device is None:
                    selected_device = ['No Device Selected', '', 0]
                list_devices(state)
                for d in state.devices:
                    if selected_device[0] == d[0]:
                        d[2] = 1
                        break

            elif r.current_STATE == 0 and STATE == 1:
                print("CONFIGURING --> RUNNING")
                try:
                    r = create_remapper(state, "settings.json")
                except ValueError as e:
                    print(f"Error creating remapper: {e}")
                    r = None

            if r is not None:
                r.current_STATE = STATE
