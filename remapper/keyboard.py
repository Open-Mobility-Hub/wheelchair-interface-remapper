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
from enum import Enum
import select

from remapper import Remapper
from wdi_report import *

class Keyboard(Remapper):
    def RUN(self):
        r, _, _ = select.select([self.device], [], [], 0.1)
        if r:
            event = self.device.read_one()
            if event.type == evdev.ecodes.EV_KEY and event.code in self.evdev.keys():
                if event.value == 1:
                    if self.evdev[event.code] == 'shift':
                        self.modifier = modifier.SHIFT
                    elif self.evdev[event.code] == 'ctrl':
                        self.modifier = modifier.CTRL
                    elif self.evdev[event.code] == 'alt':
                        self.modifier = modifier.ALT

                    elif self.evdev[event.code] in self.remapping_dict.keys():
                        print(f"{self.evdev[event.code]} pressed")
                        self.buttons.append(
                            self.remapping_dict[self.evdev[event.code]])
                        # self.write_report(get_wdi_report(self.fb, self.lr, self.buttons))

                    elif self.evdev[event.code] == ' ':
                        self.buttons.append(self.remapping_dict['space'])

                elif event.value == 0:
                    if self.evdev[event.code] == 'shift' or self.evdev[event.code] == 'ctrl' or self.evdev[event.code] == 'alt':
                        self.modifier = modifier.NONE
                    elif self.evdev[event.code] in self.remapping_dict.keys():
                        self.buttons.remove(
                            self.remapping_dict[self.evdev[event.code]])
                        # self.write_report(get_wdi_report(self.fb, self.lr, self.buttons))
                # else:
                    # when keys are held
                    # if self.evdev[event.code] in self.remapping_dict.values():
                        # self.write_report(get_wdi_report(self.fb, self.lr, self.buttons))
            self.fb = 0
            self.lr = 0
            for drive_cmd in drive_map.keys():
                if drive_cmd in self.buttons:
                    self.fb, self.lr = drive_map[drive_cmd]
            self.fb *= self.fwd_back_scale
            self.lr *= self.left_right_scale

            self.write_report(get_wdi_report(self.fb, self.lr, self.buttons))

    def get_dicts(self):
        self.evdev = kb_evdev
        self.modifier = modifier.NONE

        self.fb = 0
        self.lr = 0
        self.fwd_back_scale = 75
        self.left_right_scale = 60

kb_evdev = {
    evdev.ecodes.KEY_A: 'a',
    evdev.ecodes.KEY_B: 'b',
    evdev.ecodes.KEY_C: 'c',
    evdev.ecodes.KEY_D: 'd',
    evdev.ecodes.KEY_E: 'e',
    evdev.ecodes.KEY_F: 'f',
    evdev.ecodes.KEY_G: 'g',
    evdev.ecodes.KEY_H: 'h',
    evdev.ecodes.KEY_I: 'i',
    evdev.ecodes.KEY_J: 'j',
    evdev.ecodes.KEY_K: 'k',
    evdev.ecodes.KEY_L: 'l',
    evdev.ecodes.KEY_M: 'm',
    evdev.ecodes.KEY_N: 'n',
    evdev.ecodes.KEY_O: 'o',
    evdev.ecodes.KEY_P: 'p',
    evdev.ecodes.KEY_Q: 'q',
    evdev.ecodes.KEY_R: 'r',
    evdev.ecodes.KEY_S: 's',
    evdev.ecodes.KEY_T: 't',
    evdev.ecodes.KEY_U: 'u',
    evdev.ecodes.KEY_V: 'v',
    evdev.ecodes.KEY_W: 'w',
    evdev.ecodes.KEY_X: 'x',
    evdev.ecodes.KEY_Y: 'y',
    evdev.ecodes.KEY_Z: 'z',
    evdev.ecodes.KEY_1: '1',
    evdev.ecodes.KEY_2: '2',
    evdev.ecodes.KEY_3: '3',
    evdev.ecodes.KEY_4: '4',
    evdev.ecodes.KEY_5: '5',
    evdev.ecodes.KEY_6: '6',
    evdev.ecodes.KEY_7: '7',
    evdev.ecodes.KEY_8: '8',
    evdev.ecodes.KEY_9: '9',
    evdev.ecodes.KEY_0: '0',
    evdev.ecodes.KEY_ENTER: 'enter',
    evdev.ecodes.KEY_ESC: 'esc',
    evdev.ecodes.KEY_BACKSPACE: 'backspace',
    evdev.ecodes.KEY_TAB: 'tab',
    evdev.ecodes.KEY_SPACE: ' ',
    evdev.ecodes.KEY_MINUS: '-',
    evdev.ecodes.KEY_EQUAL: '=',
    evdev.ecodes.KEY_LEFTBRACE: '[',
    evdev.ecodes.KEY_RIGHTBRACE: ']',
    evdev.ecodes.KEY_BACKSLASH: '\\',
    evdev.ecodes.KEY_SEMICOLON: ';',
    evdev.ecodes.KEY_APOSTROPHE: "'",
    evdev.ecodes.KEY_GRAVE: '`',
    evdev.ecodes.KEY_COMMA: ',',
    evdev.ecodes.KEY_DOT: '.',
    evdev.ecodes.KEY_SLASH: '/',
    evdev.ecodes.KEY_CAPSLOCK: 'caps',
    evdev.ecodes.KEY_F1: 'F1',
    evdev.ecodes.KEY_F2: 'F2',
    evdev.ecodes.KEY_F3: 'F3',
    evdev.ecodes.KEY_F4: 'F4',
    evdev.ecodes.KEY_F5: 'F5',
    evdev.ecodes.KEY_F6: 'F6',
    evdev.ecodes.KEY_F7: 'F7',
    evdev.ecodes.KEY_F8: 'F8',
    evdev.ecodes.KEY_F9: 'F9',
    evdev.ecodes.KEY_F10: 'F10',
    evdev.ecodes.KEY_F11: 'F11',
    evdev.ecodes.KEY_F12: 'F12',
    evdev.ecodes.KEY_LEFTSHIFT: 'shift',
    evdev.ecodes.KEY_RIGHTSHIFT: 'shift',
    evdev.ecodes.KEY_LEFTCTRL: 'ctrl',
    evdev.ecodes.KEY_RIGHTCTRL: 'ctrl',
    evdev.ecodes.KEY_LEFTALT: 'alt',
    evdev.ecodes.KEY_RIGHTALT: 'alt'
}

class modifier(Enum):
    NONE = 0
    SHIFT = 1
    CTRL = 2
    ALT = 3
