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
    def get_dicts(self):
        self.dpad_x = 0
        self.dpad_y = 0
        self.fb = 0
        self.lr = 0

        self.abs_max = {}
        self.abs_min = {}
        for axis in [evdev.ecodes.ABS_X, evdev.ecodes.ABS_Y, evdev.ecodes.ABS_RX, evdev.ecodes.ABS_RY]:
           try:
               abs_info = self.device.absinfo(axis)
               self.abs_max[axis] = abs_info.max
               self.abs_min[axis] = abs(abs_info.min)
           except:
               pass

    def handle_joystick(self, event, axis_name):
        if axis_name in self.remapping_dict:
            wdi_event = self.remapping_dict[axis_name]

            if event.value > 0:
                scale = self.abs_max[event.code]
            else:
                scale = self.abs_min[event.code]

            if wdi_event in drive_map.keys():
                match self.remapping_dict[axis_name]:
                    case 'Drive Forward':
                        self.fb = abs(event.value) / scale * 100
                    case 'Drive Backward':
                        self.fb = -abs(event.value) / scale * 100
                    case 'Drive Left':
                        self.lr = -abs(event.value) / scale * 100
                    case 'Drive Right':
                        self.lr = abs(event.value) / scale * 100
            else:
                if abs(event.value) >= 0.9 * scale:
                    if wdi_event not in self.buttons:
                        self.buttons.append(wdi_event)
                else:
                    if wdi_event in self.buttons:
                        self.buttons.remove(wdi_event)

    def RUN(self):
        r, _, _ = select.select([self.device], [], [], 0.1)
        if r:
            for event in self.device.read():
                if event.type == evdev.ecodes.EV_KEY and event.code in gp_evdev:
                    btn = gp_evdev[event.code]
                    if event.value == 1:
                        if btn in self.remapping_dict:
                            self.buttons.append(self.remapping_dict[btn])
                            # self.write_report(get_wdi_report(0, 0, self.buttons))
                    elif event.value == 0:
                        if btn in self.remapping_dict:
                            wdi_cmd = self.remapping_dict[btn]
                            if wdi_cmd in self.buttons:
                                self.buttons.remove(wdi_cmd)
                            # self.write_report(get_wdi_report(0, 0, self.buttons))
                elif event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_HAT0X:
                        if event.value == -1:
                            if "DPAD_LEFT" in self.remapping_dict:
                                self.buttons.append(self.remapping_dict["DPAD_LEFT"])
                        elif event.value == 1:
                            if "DPAD_RIGHT" in self.remapping_dict:
                                self.buttons.append(self.remapping_dict["DPAD_RIGHT"])
                        elif event.value == 0:
                            if "DPAD_LEFT" in self.remapping_dict:
                                wdi_cmd = self.remapping_dict["DPAD_LEFT"]
                                if wdi_cmd in self.buttons:
                                    self.buttons.remove(wdi_cmd)
                            if "DPAD_RIGHT" in self.remapping_dict:
                                wdi_cmd = self.remapping_dict["DPAD_RIGHT"]
                                if wdi_cmd in self.buttons:
                                    self.buttons.remove(wdi_cmd)
                    elif event.code == evdev.ecodes.ABS_HAT0Y:
                        if event.value == -1:
                            if "DPAD_UP" in self.remapping_dict:
                                self.buttons.append(self.remapping_dict["DPAD_UP"])
                        elif event.value == 1:
                            if "DPAD_DOWN" in self.remapping_dict:
                                self.buttons.append(self.remapping_dict["DPAD_DOWN"])
                        elif event.value == 0:
                            if "DPAD_UP" in self.remapping_dict:
                                wdi_cmd = self.remapping_dict["DPAD_UP"]
                                if wdi_cmd in self.buttons:
                                    self.buttons.remove(wdi_cmd)
                            if "DPAD_DOWN" in self.remapping_dict:
                                wdi_cmd = self.remapping_dict["DPAD_DOWN"]
                                if wdi_cmd in self.buttons:
                                    self.buttons.remove(wdi_cmd)

                    elif event.code == evdev.ecodes.ABS_X:
                        if event.value >= 0:
                            self.handle_joystick(event, "POS_ABS_X")
                        elif event.value < 0:
                            self.handle_joystick(event, "NEG_ABS_X")
                    elif event.code == evdev.ecodes.ABS_Y:
                        if event.value >= 0:
                            self.handle_joystick(event, "POS_ABS_Y")
                        elif event.value < 0:
                            self.handle_joystick(event, "NEG_ABS_Y")
                    elif event.code == evdev.ecodes.ABS_RX:
                        if event.value >= 0:
                            self.handle_joystick(event, "POS_ABS_RX")
                        elif event.value < 0:
                            self.handle_joystick(event, "NEG_ABS_RX")
                    elif event.code == evdev.ecodes.ABS_RY:
                        if event.value >= 0:
                            self.handle_joystick(event, "POS_ABS_RY")
                        elif event.value < 0:
                            self.handle_joystick(event, "NEG_ABS_RY")

            self.write_report(get_wdi_report(self.fb, self.lr, self.buttons))


gp_evdev = {
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

DPAD_AXES = {
    evdev.ecodes.ABS_HAT0X,
    evdev.ecodes.ABS_HAT0Y,
}
