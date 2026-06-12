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

import json
import evdev
import select

from wdi_report import *

from abc import ABC, abstractmethod

class Remapper(ABC):
    def __init__(self, device, state, settings_path):
        self.fd = open('/dev/hidg0', 'rb+')

        self.device = evdev.InputDevice(device)
        self.state = state
        self.current_STATE = state.STATE
        self.settings_path = settings_path
        self.buttons = []

        self.write_report(get_wdi_report(["Enable Device Control"]))
        self.write_report(bytes([0x00]) * 8)

        with open(self.settings_path, 'r') as f:
            self.remapping_dict = json.load(f)
            self.input = self.remapping_dict["input"]
        self.get_dicts()

    def __del__(self):
        if hasattr(self, 'fd'):
            self.fd.close()

    def write_report(self, report):
        self.fd.write(report)

    def CONFIGURE(self):
        r, _, _ = select.select([self.device], [], [], 1)
        if r:
            self.device.read()

    @abstractmethod
    def get_dicts(self):
        pass

    @abstractmethod
    def RUN(self):
        pass