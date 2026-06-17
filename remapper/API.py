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

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from interface_dicts.KB_dicts import *
from interface_dicts.GP_dicts import *
def make_default_layer(input):
    if input == "Keyboard":
        return {
            "Drive": KB_Drive_settings.copy(),
            "Chair": KB_Chair_settings.copy(),
            "Profile": KB_Profile_settings.copy(),
            "Memory": KB_Memory_settings.copy(),
            "Seating": KB_Seating_settings.copy()
        }
    elif input == "GP":
        return {
            "Drive": GP_Drive_settings.copy(),
            "Chair": GP_Chair_settings.copy(),
            "Profile": GP_Profile_settings.copy(),
            "Memory": GP_Memory_settings.copy(),
            "Seating": GP_Seating_settings.copy()
        }
    else:
        return {
            "Drive": None,
            "Chair": None,
            "Profile": None,
            "Memory": None,
            "Seating": None
        }

def load_state_from_settings(state, settings_path):
    with open(settings_path, "r") as f:
        data = json.load(f)
    for key in state.inputs:
        state.inputs[key] = 0
    state.inputs[data["input"]] = 1

    active_input = next(key for key, value in state.inputs.items() if value == 1)

    state.layer_key = data.get("layer_key", None)

    state.settings['layers'] = []
    for layer_data in data.get("layers", []):
        layer = make_default_layer(active_input)
        action_to_key = {v: k for k, v in layer_data.items() if k != "disabled"}
        disabled_actions = layer_data.get("disabled", [])
        for key, d in layer.items():
            if d is not None:
                for action in d.keys():
                    if action in action_to_key:
                        d[action] = action_to_key[action]
                    elif action in disabled_actions:
                        d[action] = "N/A"
        state.settings['layers'].append(layer)

    if active_input == "Keyboard":
        state.settings['Speed'] = KB_Speed_settings.copy()
    elif active_input == "GP":
        state.settings['Speed'] = GP_Speed_settings.copy()

    for key in state.settings['Speed'].keys():
        if key in data:
            state.settings['Speed'][key] = data[key]

    for d in state.devices:
        if d[0] == data.get("device", ""):
            d[2] = 1
        else:
            d[2] = 0


def create_app(state, settings_path):
    app = Flask(__name__)
    app.json.sort_keys = False
    cors_origins = [
        origin.strip()
        for origin in os.environ.get(
            "REMAPPER_CORS_ORIGINS", "http://localhost:3000"
        ).split(",")
        if origin.strip()
    ]
    CORS(app, origins=cors_origins)


    @app.route('/STATE')
    def get_state():
        return jsonify(state.STATE)
    
    @app.route("/getDevices", methods=['GET'])
    def get_devices():
        response = jsonify(state.devices)
        return response
    
    @app.route("/selectDevice", methods=['POST'])
    def select_device():
        device_name = request.get_json()
        for d in state.devices:
            d[2] = 1 if d[1] == device_name else 0
        return jsonify({'message': 'Device selected successfully'}), 200

    @app.route("/getInputs")
    def input():
        state.STATE = 0
        response = jsonify(state.inputs)
        return response


    @app.route("/changeInput", methods=['POST'])
    def change_input():
        input = request.get_json()

        if input == "Keyboard":
            state.layer_key = None
            state.settings['Speed'] = KB_Speed_settings.copy()
            state.settings['layers'] = [make_default_layer("Keyboard")]
        elif input == "GP":
            state.layer_key = None
            state.settings['Speed'] = GP_Speed_settings.copy()
            state.settings['layers'] = [make_default_layer("GP")]

        for key in state.inputs.keys():
            if key == input:
                state.inputs[key] = 1
            else:
                state.inputs[key] = 0

        return jsonify({'message': 'Input updated successfully'}), 200

    @app.route("/getOptions", methods=['POST'])
    def get_options():
        options = state.input_options[request.get_json()]
        response = jsonify(options)
        return response

    @app.route("/getSpeedSettings")
    def get_speed_settings():
        response = jsonify(state.settings['Speed'])
        return response

    @app.route("/getSettings")
    def get_settings():
        mode = request.args.get('mode')
        layer = int(request.args.get('layer', 0))
        return jsonify(state.settings['layers'][layer][mode])

    @app.route("/changeSettings", methods=['POST'])
    def change_settings():
        newSetting = request.get_json()

        if newSetting['value'] == state.layer_key:
            return jsonify({'message': 'Cannot assign layer key to a setting'}), 409

        layer_setting = state.settings['layers'][newSetting['layer']]
        
        changed_setting = None
        for mode, d in layer_setting.items():
            if d is not None:
                for key in d.keys():
                    if d[key] == newSetting['value'] and key != newSetting['setting']:
                        d[key] = "N/A"
                        changed_setting = [mode, key]
                        break
        state.settings['layers'][newSetting['layer']][newSetting['mode']][newSetting['setting']] = newSetting['value']
        return jsonify({'message': 'Setting updated successfully', 'changed_setting': changed_setting}), 200

    @app.route("/changeSpeedSettings", methods=['POST'])
    def change_speed_settings():
        newSetting = request.get_json()

        if not isinstance(newSetting['value'], int):
            return jsonify({'message': 'Speed setting value must be an integer'}), 409
        if newSetting['value'] < 0 or newSetting['value'] > 100:
            return jsonify({'message': 'Speed setting value must be between 0 and 100'}), 409
        state.settings['Speed'][newSetting['setting']] = newSetting['value']

        return jsonify({'message': 'Speed setting updated successfully'}), 200
    
    @app.route("/getLayers")
    def get_layers():
        return jsonify({'count': len(state.settings['layers'])})
    
    @app.route("/addLayer", methods=['POST'])
    def add_layer():
        if len(state.settings['layers']) >= 3:
            return jsonify({'message': 'Maximum number of layers reached'}), 409
        active_input = next(key for key, value in state.inputs.items() if value == 1)
        state.settings['layers'].append(make_default_layer(active_input))
        return jsonify({'message': 'Layer added successfully'}), 200
    
    @app.route("/deleteLayer", methods=['POST'])
    def delete_layer():
        layer = int(request.get_json())
        if layer < 0 or layer >= len(state.settings['layers']):
            return jsonify({'message': 'Invalid layer index'}), 409
        if len(state.settings['layers']) == 1:
            return jsonify({'message': 'Cannot delete the last layer'}), 409
        state.settings['layers'].pop(layer)
        return jsonify({'message': 'Layer deleted successfully'}), 200

    @app.route("/getLayerKey")
    def get_layer_key():
        return jsonify({'layer_key': state.layer_key})
    
    @app.route("/changeLayerKey", methods=['POST'])
    def change_layer_key():
        new_key = request.get_json()
        active_input = next(key for key, value in state.inputs.items() if value == 1)
        if new_key not in state.input_options[active_input]:
            return jsonify({'message': 'Invalid layer key'}), 409
        
        changed_settings = []
        for i, l in enumerate(state.settings['layers']):
            for mode, d in l.items():
                if d is not None:
                    for setting, value in d.items():
                        if '+' in value:
                            keys = value.split('+', 1)
                            if new_key in keys:
                                d[setting] = "N/A"
                                changed_settings.append([i, mode, setting])
                        else:
                            if value == new_key:
                                d[setting] = "N/A"
                                changed_settings.append([i, mode, setting])
        state.layer_key = new_key
        return jsonify({'message': 'Layer key updated successfully', 'changed_settings': changed_settings}), 200

    @app.route("/upload")
    def upload():
        for key in state.inputs.keys():
            if state.inputs[key] == 1:
                chosen_input = key
        input_dict = {"input": chosen_input}
        selected_device = {"device": d[0] for d in state.devices if d[2] == 1}

        layers_list = []
        for l in state.settings['layers']:
            combined_settings = {k: v for key, d in l.items() if d is not None for k, v in d.items()}
            reversed_settings = {v: k for k, v in combined_settings.items() if v != "N/A"}
            disabled = [k for k, v in combined_settings.items() if v == "N/A"]
            layers_list.append({
                **reversed_settings,
                "disabled": disabled
            })
        
        settings_dictionary = {
            **input_dict,
            **selected_device,
            "layer_key": state.layer_key,
            **state.settings['Speed'],
            "layers": layers_list
        }

        with open(settings_path, "w") as outfile:
            json.dump(
                settings_dictionary,
                outfile,
                indent=2)
        state.STATE = 1
        return jsonify({'message': 'Uploaded successfully'}), 200

    return app