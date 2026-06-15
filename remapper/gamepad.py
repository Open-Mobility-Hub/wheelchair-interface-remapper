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

import evdev
import select

from remapper import Remapper
from wdi_report import *


class Gamepad(Remapper):

    def RUN(self):
        r, _, _ = select.select([self.device], [], [], 0.1)
        if r:
            for event in self.device.read():
                if event.type == evdev.ecodes.EV_KEY and event.code in gp_evdev:
                    btn = gp_evdev[event.code]
                    if event.value == 1:
                        self.buttons.add(btn)
                    elif event.value == 0:
                        self.buttons.discard(btn)
                elif event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_HAT0X:
                        if event.value == -1:
                            self.buttons.add("DPAD_LEFT")
                        elif event.value == 1:
                            self.buttons.add("DPAD_RIGHT")
                        elif event.value == 0:
                            self.buttons.discard("DPAD_LEFT")
                            self.buttons.discard("DPAD_RIGHT")
                    elif event.code == evdev.ecodes.ABS_HAT0Y:
                        if event.value == -1:
                            self.buttons.add("DPAD_UP")
                        elif event.value == 1:
                            self.buttons.add("DPAD_DOWN")
                        elif event.value == 0:
                            self.buttons.discard("DPAD_UP")
                            self.buttons.discard("DPAD_DOWN")
                    elif event.code in JOYSTICK_AXES:
                        pos, neg = JOYSTICK_AXES[event.code]
                        if event.value > 0:
                            self.buttons.add(pos)
                            self.buttons.discard(neg)
                            self.axis_values[pos] = abs(
                                event.value) / self.abs_max[event.code] * 100
                            self.axis_values.pop(neg, None)
                        elif event.value < 0:
                            self.buttons.add(neg)
                            self.buttons.discard(pos)
                            self.axis_values[neg] = abs(
                                event.value) / self.abs_min[event.code] * 100
                            self.axis_values.pop(pos, None)
                        else:
                            self.buttons.discard(pos)
                            self.buttons.discard(neg)
                            self.axis_values.pop(pos, None)
                            self.axis_values.pop(neg, None)

            actions = []
            consumed = set()
            self.fb = 0
            self.lr = 0
            for mapping_key, wdi_action in self.remapping_dict.items():
                if "+" in mapping_key:
                    keys = mapping_key.split("+", 1)
                    if keys[0] in self.buttons and keys[1] in self.buttons:
                        actions.append(wdi_action)
                        consumed.add(keys[0])
                        consumed.add(keys[1])
            for mapping_key, wdi_action in self.remapping_dict.items():
                if "+" not in mapping_key:
                    if mapping_key in self.buttons and mapping_key not in consumed:
                        if wdi_action in drive_map:
                            fb, lr = drive_map[wdi_action]
                            if fb != 0:
                                self.fb += fb * self.axis_values.get(mapping_key, self.fwd_back_scale)
                            if lr != 0:
                                self.lr += lr * self.axis_values.get(mapping_key, self.left_right_scale)
                        else:
                            actions.append(wdi_action)

            self.write_report(get_wdi_report(self.fb, self.lr, actions))

    def get_dicts(self):
        self.fb = 0
        self.lr = 0
        self.fwd_back_scale = self.state.settings['Speed']["Forward Backward Speed"]
        self.left_right_scale = self.state.settings['Speed']["Left Right Speed"]

        self.axis_values = {}

        self.abs_max = {}
        self.abs_min = {}
        for axis in JOYSTICK_AXES:
            try:
                abs_info = self.device.absinfo(axis)
                self.abs_max[axis] = abs_info.max
                self.abs_min[axis] = abs(abs_info.min)
            except:
                pass

gp_evdev = {
    evdev.ecodes.BTN_C: 'BTN_C',
    evdev.ecodes.BTN_NORTH: 'BTN_NORTH',
    evdev.ecodes.BTN_SOUTH: 'BTN_SOUTH',
    evdev.ecodes.BTN_EAST: 'BTN_EAST',
    evdev.ecodes.BTN_WEST: 'BTN_WEST',
    evdev.ecodes.BTN_START: 'BTN_START',
    evdev.ecodes.BTN_SELECT: 'BTN_SELECT',
    evdev.ecodes.BTN_MODE: 'BTN_MODE',
    evdev.ecodes.BTN_TL: 'BTN_TL',
    evdev.ecodes.BTN_TR: 'BTN_TR',
    evdev.ecodes.BTN_TL2: 'BTN_TL2',
    evdev.ecodes.BTN_TR2: 'BTN_TR2',
    evdev.ecodes.BTN_THUMBL: 'BTN_THUMBL',
    evdev.ecodes.BTN_THUMBR: 'BTN_THUMBR',
    evdev.ecodes.BTN_TRIGGER_HAPPY1: 'BTN_TRIGGER_HAPPY1',
    evdev.ecodes.BTN_TRIGGER_HAPPY2: 'BTN_TRIGGER_HAPPY2',
    evdev.ecodes.BTN_TRIGGER_HAPPY3: 'BTN_TRIGGER_HAPPY3',
    evdev.ecodes.BTN_TRIGGER_HAPPY4: 'BTN_TRIGGER_HAPPY4',
    evdev.ecodes.BTN_TRIGGER_HAPPY5: 'BTN_TRIGGER_HAPPY5',
    evdev.ecodes.BTN_TRIGGER_HAPPY6: 'BTN_TRIGGER_HAPPY6',
    evdev.ecodes.BTN_TRIGGER_HAPPY7: 'BTN_TRIGGER_HAPPY7',
    evdev.ecodes.BTN_TRIGGER_HAPPY8: 'BTN_TRIGGER_HAPPY8',
    evdev.ecodes.BTN_TRIGGER_HAPPY9: 'BTN_TRIGGER_HAPPY9',
    evdev.ecodes.BTN_TRIGGER_HAPPY10: 'BTN_TRIGGER_HAPPY10',
    evdev.ecodes.BTN_TRIGGER_HAPPY11: 'BTN_TRIGGER_HAPPY11',
    evdev.ecodes.BTN_TRIGGER_HAPPY12: 'BTN_TRIGGER_HAPPY12',
    evdev.ecodes.BTN_TRIGGER_HAPPY13: 'BTN_TRIGGER_HAPPY13',
    evdev.ecodes.BTN_TRIGGER_HAPPY14: 'BTN_TRIGGER_HAPPY14',
    evdev.ecodes.BTN_TRIGGER_HAPPY15: 'BTN_TRIGGER_HAPPY15',
    evdev.ecodes.BTN_TRIGGER_HAPPY16: 'BTN_TRIGGER_HAPPY16',
}

JOYSTICK_AXES = {
    evdev.ecodes.ABS_X: ("POS_ABS_X", "NEG_ABS_X"),
    evdev.ecodes.ABS_Y: ("POS_ABS_Y", "NEG_ABS_Y"),
    evdev.ecodes.ABS_RX: ("POS_ABS_RX", "NEG_ABS_RX"),
    evdev.ecodes.ABS_RY: ("POS_ABS_RY", "NEG_ABS_RY"),
}