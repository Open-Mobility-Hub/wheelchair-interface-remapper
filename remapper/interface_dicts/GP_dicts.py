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

from collections import OrderedDict

GP_Speed_settings = {
    "Forward Backward Speed": 60,
    "Left Right Speed": 75
}

GP_Drive_settings = {
    "Drive Forward": "NEG_ABS_Y",
    "Drive Backward": "POS_ABS_Y",
    "Drive Left": "NEG_ABS_X",
    "Drive Right": "POS_ABS_X",
    "Emergency Stop": "BTN_SOUTH",
    "Device Control Toggle": "BTN_START",
    "Enable Device Control": "BTN_C",
    "Disable Device Control": "BTN_MODE"
}

GP_Chair_settings = {
    "Power/Sleep Toggle": "N/A",
    "Open/Close User Menu": "BTN_SELECT",
    "Switch Mode": "DPAD_DOWN",
    "Headlight Toggle": "BTN_THUMBL",
    "Hazard Lights": "BTN_WEST",
    "Left Blinker": "DPAD_LEFT",
    "Right Blinker": "DPAD_RIGHT",
    "Horn": "BTN_THUMBR"
}

GP_Profile_settings = {
    "Increase Speed": "BTN_TR",
    "Decrease Speed": "BTN_TL",
    "Speed 1": "N/A",
    "Speed 2": "N/A",
    "Speed 3": "N/A",
    "Speed 4": "N/A",
    "Speed 5": "N/A",
    "Increase Profile": "DPAD_UP",
    "Decrease Profile": "N/A"
}

GP_Memory_settings = {
    "Memory Seating 1": "BTN_TRIGGER_HAPPY1",
    "Memory Seating 2": "BTN_TRIGGER_HAPPY2",
    "Memory Seating 3": "BTN_TRIGGER_HAPPY3",
    "Memory Seating 4": "BTN_TRIGGER_HAPPY4",
    "Memory Seating 5": "BTN_TRIGGER_HAPPY5",
    "Memory Seating 6": "BTN_TRIGGER_HAPPY6",
    "Memory Seating Home": "BTN_TRIGGER_HAPPY7"
}

GP_Seating_settings = {
    "Tilt Forward": "BTN_TRIGGER_HAPPY9",
    "Tilt Backward": "BTN_TRIGGER_HAPPY8+BTN_TRIGGER_HAPPY9",
    "Recline Forward": "BTN_TRIGGER_HAPPY10",
    "Recline Backward": "BTN_TRIGGER_HAPPY8+BTN_TRIGGER_HAPPY10",
    "Legrest Up": "BTN_TRIGGER_HAPPY11",
    "Legrest Down": "BTN_TRIGGER_HAPPY8+BTN_TRIGGER_HAPPY11",
    "Elevate Up": "BTN_TRIGGER_HAPPY12",
    "Elevate Down": "BTN_TRIGGER_HAPPY8+BTN_TRIGGER_HAPPY12",
    "Footplates Up": "BTN_TRIGGER_HAPPY13",
    "Footplates Down": "BTN_TRIGGER_HAPPY8+BTN_TRIGGER_HAPPY13",
    "Stand Up": "BTN_TRIGGER_HAPPY14",
    "Stand Down": "BTN_TRIGGER_HAPPY8+BTN_TRIGGER_HAPPY14"
}