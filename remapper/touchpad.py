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

class Touchpad(Remapper):
    def RUN(self):
        r, _, _ = select.select([self.device], [], [], 0.1)
        if r:
            event = self.device.read_one()
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == 0:
                    # Current cmd
                    if event.value >= self.sp_min and event.value <= self.sp_max:
                        current_cmd = 'Soft Puff'
                    elif event.value >= self.hp_min:
                        current_cmd = 'Hard Puff'
                    elif event.value <= self.ss_min and event.value >= self.ss_max:
                        current_cmd = 'Soft Sip'
                    elif event.value <= self.hs_min:
                        current_cmd = 'Hard Sip'
                    else:
                        current_cmd = 'Dead'

                    if self.last_cmd != current_cmd:
                        print(f'current_cmd: {current_cmd}')
                        match current_cmd:
                            case 'Hard Puff':
                                if self.fb < 0:
                                    self.fb = 0
                                elif self.fb == 0:
                                    self.fb = self.fwd_back_scale
                                self.lr = 0
                            case 'Hard Sip':
                                if self.fb > 0:
                                    self.fb = 0
                                elif self.fb == 0:
                                    self.fb = -self.fwd_back_scale
                                self.lr = 0
                            case 'Soft Puff':
                                self.count = 0
                            case 'Soft Sip':
                                self.count = 0
                            case 'Dead':
                                self.lr = 0
                    else:
                        if current_cmd == 'Soft Puff':
                            self.count += 1
                            if self.count > self.hold_length:
                                self.lr = self.left_right_scale
                        elif current_cmd == 'Soft Sip':
                            self.count += 1
                            if self.count > self.hold_length:
                                self.lr = -self.left_right_scale

                    self.last_cmd = current_cmd
                print(f'fb: {self.fb}, lr: {self.lr} value: {event.value} ')
        self.write_report(get_wdi_report(self.fb, self.lr, []))

    def get_dicts(self):
        self.fb = 0
        self.lr = 0
        self.fwd_back_scale = 75
        self.left_right_scale = 60
        self.last_cmd = 'Dead'
        self.count = 0

        self.sp_min = self.remapping_dict["Soft Puff Min"]
        self.sp_max = self.remapping_dict["Soft Puff Max"]
        self.hp_min = self.remapping_dict["Hard Puff Min"]
        self.hp_max = self.remapping_dict["Hard Puff Max"]
        self.ss_min = self.remapping_dict["Soft Sip Min"]
        self.ss_max = self.remapping_dict["Soft Sip Max"]
        self.hs_min = self.remapping_dict["Hard Sip Min"]
        self.hs_max = self.remapping_dict["Hard Sip Max"]
        self.hold_length = self.remapping_dict["Hold Length"]