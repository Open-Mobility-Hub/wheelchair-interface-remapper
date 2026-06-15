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

class Keyboard(Remapper):
    def RUN(self):
        r, _, _ = select.select([self.device], [], [], 0.1)
        if r:
            event = self.device.read_one()
            if event.type == evdev.ecodes.EV_KEY and event.code in self.evdev:
                if event.value == 1:
                    self.buttons.add(self.evdev[event.code])

                elif event.value == 0:
                    self.buttons.discard(self.evdev[event.code])

            actions = []
            consumed = set()
            if self.remapping_dict["layer_key"] in self.buttons:
                self.layer = (self.layer + 1) % len(self.layers)
                self.buttons.clear()

            for mapping_key, wdi_action in self.layers[self.layer].items():
                if "+" in mapping_key:
                    keys = mapping_key.split("+", 1)
                    if keys[0] in self.buttons and keys[1] in self.buttons:
                        actions.append(wdi_action)
                        consumed.add(keys[0])
                        consumed.add(keys[1])
            
            for mapping_key, wdi_action in self.layers[self.layer].items():
                if "+" not in mapping_key:
                    if mapping_key in self.buttons and mapping_key not in consumed:
                        actions.append(wdi_action)

            self.fb = 0
            self.lr = 0
            for drive_cmd in drive_map.keys():
                if drive_cmd in actions:
                    fb, lr = drive_map[drive_cmd]
                    self.fb += fb
                    self.lr += lr
            self.fb *= self.fwd_back_scale
            self.lr *= self.left_right_scale

            self.write_report(get_wdi_report(self.fb, self.lr, actions))

    def get_dicts(self):
        self.evdev = kb_evdev

        self.fwd_back_scale = self.state.settings['Speed']["Forward Backward Speed"]
        self.left_right_scale = self.state.settings['Speed']["Left Right Speed"]

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
    evdev.ecodes.KEY_SPACE: 'space',
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
    evdev.ecodes.KEY_LEFTSHIFT: 'left shift',
    evdev.ecodes.KEY_RIGHTSHIFT: 'right shift',
    evdev.ecodes.KEY_LEFTCTRL: 'left ctrl',
    evdev.ecodes.KEY_RIGHTCTRL: 'right ctrl',
    evdev.ecodes.KEY_LEFTALT: 'left alt',
    evdev.ecodes.KEY_RIGHTALT: 'right alt',
    evdev.ecodes.KEY_LEFTMETA: 'left meta',
    evdev.ecodes.KEY_RIGHTMETA: 'right meta',
    evdev.ecodes.KEY_UP: 'up',
    evdev.ecodes.KEY_DOWN: 'down',
    evdev.ecodes.KEY_LEFT: 'left',
    evdev.ecodes.KEY_RIGHT: 'right',
    evdev.ecodes.KEY_DELETE: 'delete',
    evdev.ecodes.KEY_INSERT: 'insert',
    evdev.ecodes.KEY_HOME: 'home',
    evdev.ecodes.KEY_END: 'end',
    evdev.ecodes.KEY_PAGEUP: 'page up',
    evdev.ecodes.KEY_PAGEDOWN: 'page down',
    evdev.ecodes.KEY_KP0: 'num0',
    evdev.ecodes.KEY_KP1: 'num1',
    evdev.ecodes.KEY_KP2: 'num2',
    evdev.ecodes.KEY_KP3: 'num3',
    evdev.ecodes.KEY_KP4: 'num4',
    evdev.ecodes.KEY_KP5: 'num5',
    evdev.ecodes.KEY_KP6: 'num6',
    evdev.ecodes.KEY_KP7: 'num7',
    evdev.ecodes.KEY_KP8: 'num8',
    evdev.ecodes.KEY_KP9: 'num9',
    evdev.ecodes.KEY_KPENTER: 'num enter',
    evdev.ecodes.KEY_KPMINUS: 'num minus',
    evdev.ecodes.KEY_KPPLUS: 'num plus',
    evdev.ecodes.KEY_KPASTERISK: 'num multiply',
    evdev.ecodes.KEY_KPSLASH: 'num divide',
    evdev.ecodes.KEY_KPDOT: 'num dot',
    evdev.ecodes.KEY_KPCOMMA: 'num comma',
    evdev.ecodes.KEY_KPEQUAL: 'num equal',
    evdev.ecodes.KEY_NUMLOCK: 'num lock',
}