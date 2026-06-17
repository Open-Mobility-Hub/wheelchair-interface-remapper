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


def drive_bytes(fb, lr):
    lr_value = round(lr / 100 * 127)
    if lr_value < 0:
        lr_value = 256 + lr_value  # two's complement
    report = bytes([lr_value])

    fb_value = round(fb / 100 * 127)
    if fb_value < 0:
        fb_value = 256 + fb_value  # two's complement
    report += bytes([fb_value])

    return report

drive_map = {
    'Drive Forward': (1, 0),
    'Drive Backward': (-1, 0),
    'Drive Left': (0, -1),
    'Drive Right': (0, 1),
}

button_map = {
    # ===== General Controls =====
    'Emergency Stop': [(2, 1 << 0)],              # BTN_SOUTH
    'Device Control Toggle': [(3, 1 << 3)],       # BTN_START
    'Enable Device Control': [(2, 1 << 2)],       # BTN_C
    'Disable Device Control': [(3, 1 << 4)],      # BTN_MODE
    'LUCI Button': [(2, 1 << 1)],                 # BTN_EAST

    # ===== Chair Control Actions =====
    'Power/Sleep Toggle': [(3, 1 << 2)],          # BTN_SELECT
    'Open/Close User Menu': [(3, 1 << 2)],        # BTN_SELECT

    'Increase Speed': [(2, 1 << 7)],              # TR
    'Decrease Speed': [(2, 1 << 6)],              # TL
            
    'Switch Mode': [(7, 4)],                   
    'Left Blinker': [(7, 6)],                  
    'Right Blinker': [(7, 2)],

    'Headlight Toggle': [(3, 1 << 5)],            # BTN_THUMBL
    'Hazard Lights': [(2, 1 << 4)],               # BTN_WEST
    'Horn': [(3, 1 << 6)],                        # BTN_THUMBR

    # ===== Memory Seating Presets =====
    'Memory Seating 1': [(4, 1 << 0)],            # BTN_TRIGGER_HAPPY1
    'Memory Seating 2': [(4, 1 << 1)],            # BTN_TRIGGER_HAPPY2
    'Memory Seating 3': [(4, 1 << 2)],            # BTN_TRIGGER_HAPPY3
    'Memory Seating 4': [(4, 1 << 3)],            # BTN_TRIGGER_HAPPY4
    'Memory Seating 5': [(4, 1 << 4)],            # BTN_TRIGGER_HAPPY5
    'Memory Seating 6': [(4, 1 << 5)],            # BTN_TRIGGER_HAPPY6
    'Memory Seating Home': [(4, 1 << 6)],         # BTN_TRIGGER_HAPPY7

    # ===== Manual Seating Adjustments =====
    'Tilt Forward': [(5, 1 << 0)],                # BTN_TRIGGER_HAPPY9
    'Tilt Backward': [(4, 1 << 7), (5, 1 << 0)],  # BTN_TRIGGER_HAPPY8 + 9

    'Recline Forward': [(5, 1 << 1)],             # BTN_TRIGGER_HAPPY10
    'Recline Backward': [(4, 1 << 7), (5, 1 << 1)], # BTN_TRIGGER_HAPPY8 + 10

    'Legrest Up': [(5, 1 << 2)],                  # BTN_TRIGGER_HAPPY11
    'Legrest Down': [(4, 1 << 7), (5, 1 << 2)],   # BTN_TRIGGER_HAPPY8 + 11

    'Elevate Up': [(5, 1 << 3)],                  # BTN_TRIGGER_HAPPY12
    'Elevate Down': [(4, 1 << 7), (5, 1 << 3)],   # BTN_TRIGGER_HAPPY8 + 12

    'Footplates Up': [(5, 1 << 4)],               # BTN_TRIGGER_HAPPY13
    'Footplates Down': [(4, 1 << 7), (5, 1 << 4)],# BTN_TRIGGER_HAPPY8 + 13

    'Stand Up': [(5, 1 << 5)],                    # BTN_TRIGGER_HAPPY14
    'Stand Down': [(4, 1 << 7), (5, 1 << 5)],     # BTN_TRIGGER_HAPPY8 + 14
}

key_map = {
    'Speed 1': 0x1E,                              # '1' key
    'Speed 2': 0x1F,                              # '2' key         
    'Speed 3': 0x20,                              # '3' key
    'Speed 4': 0x21,                              # '4' key    
    'Speed 5': 0x22,                              # '5' key
    'Increase Profile': 0x37,                     # '.' key
    'Decrease Profile': 0x36,                     # ',' key
}

def combine_hat_switch(current, new):
    diagonal_map = {
        frozenset([0, 2]): 1,
        frozenset([2, 4]): 3,
        frozenset([4, 6]): 5,
        frozenset([6, 0]): 7,
    }

    return diagonal_map.get(frozenset([current, new]), 15)

def get_wdi_report(fb, lr, buttons):
    report = bytes()
    byte_map = {}
    k_map = []

    for button in buttons:
        if button in button_map:
            for b in button_map[button]:
                byte_index, bit_value = b
                if byte_index in byte_map:
                    if byte_index == 7:
                        byte_map[byte_index] = combine_hat_switch(byte_map[byte_index], bit_value)
                    else:
                        byte_map[byte_index] |= bit_value  # Combine using OR if byte already exists
                else:
                    byte_map[byte_index] = bit_value
        if button in key_map:
            k_map.append(key_map[button])
    byte_map[8] = k_map[0] if len(k_map) > 0 else 0x00
    byte_map[9] = k_map[1] if len(k_map) > 1 else 0x00

    report = drive_bytes(fb, lr)
    for i in range(2, 10):
        if i in byte_map:
            report += bytes([byte_map[i]])
        else:
            if i == 7:
                report += bytes([0x08])
            else:
                report += bytes([0x00])

    return report
    
    