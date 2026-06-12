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
from interface_dicts.SNP_dicts import *


def load_state_from_settings(state, settings_path):
    with open(settings_path, "r") as f:
        data = json.load(f)
    for key in state.inputs:
        state.inputs[key] = 0
    state.inputs[data["input"]] = 1

    active_input = next(key for key, value in state.inputs.items() if value == 1)
    if active_input == "Keyboard":
        state.settings['Drive'] = KB_Drive_settings
        state.settings['Chair'] = KB_Chair_settings
        state.settings['Profile'] = KB_Profile_settings
        state.settings['Memory'] = KB_Memory_settings
        state.settings['Seating'] = KB_Seating_settings
    elif active_input == "GP":
        state.settings['Drive'] = GP_Drive_settings
        state.settings['Chair'] = GP_Chair_settings
        state.settings['Profile'] = GP_Profile_settings
        state.settings['Memory'] = GP_Memory_settings
        state.settings['Seating'] = GP_Seating_settings
    elif active_input == "Sip-n-Puff":
        state.settings['Drive'] = SNP_Drive_settings
        state.settings['Chair'] = None
        state.settings['Profile'] = None
        state.settings['Memory'] = None
        state.settings['Seating'] = None

    for d in state.settings.values():
        if d is not None:
            for key in d.keys():
                d[key] = data[key]

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


    @app.route("/getInputs")
    def input():
        state.STATE = 0
        response = jsonify(state.inputs)
        return response


    @app.route("/changeInput", methods=['POST'])
    def change_input():
        input = request.get_json()

        if input == "Keyboard":
            state.settings['Drive'] = KB_Drive_settings
            state.settings['Chair'] = KB_Chair_settings
            state.settings['Profile'] = KB_Profile_settings
            state.settings['Memory'] = KB_Memory_settings
            state.settings['Seating'] = KB_Seating_settings
        elif input == "GP":
            state.settings['Drive'] = GP_Drive_settings
            state.settings['Chair'] = GP_Chair_settings
            state.settings['Profile'] = GP_Profile_settings
            state.settings['Memory'] = GP_Memory_settings
            state.settings['Seating'] = GP_Seating_settings
        elif input == "Sip-n-Puff":
            state.settings['Drive'] = SNP_Drive_settings
            state.settings['Chair'] = None
            state.settings['Profile'] = None
            state.settings['Memory'] = None
            state.settings['Seating'] = None

        for key in state.inputs.keys():
            if key == input:
                state.inputs[key] = 1
            else:
                state.inputs[key] = 0

        print(f"Input changed to {input}")
        print(f"Drive settings is {state.settings['Drive']}")
        return jsonify({'message': 'Input updated successfully'}), 200

    @app.route("/getOptions", methods=['POST'])
    def get_options():
        print(f"The request is {request.get_json()}")
        options = state.input_options[request.get_json()]
        response = jsonify(options)
        return response

    # all of these functions below can be generalized
    @app.route("/getDriveSettings")
    def get_drive_settings():
        response = jsonify(state.settings['Drive'])
        return response

    @app.route("/getChairSettings")
    def get_chair_settings():
        response = jsonify(state.settings['Chair'])
        return response

    @app.route("/getProfileSettings")
    def get_profile_settings():
        response = jsonify(state.settings['Profile'])
        return response

    @app.route("/getMemorySettings")
    def get_memory_settings():
        response = jsonify(state.settings['Memory'])
        return response

    @app.route("/getSeatingSettings")
    def get_seating_settings():
        response = jsonify(state.settings['Seating'])
        return response

    @app.route("/changeSettings", methods=['POST'])
    def change_settings():
        newSetting = request.get_json()
        
        for d in state.settings.values():
            if d is not None:
                for key in d.keys():
                    if d[key] == newSetting['value'] and key != newSetting['setting']:
                        return jsonify({'message': 'Value already exists in settings'}), 409
        state.settings[newSetting['mode']][newSetting['setting']] = newSetting['value']

        return jsonify({'message': 'Setting updated successfully'}), 200

    @app.route("/upload")
    def upload():
        for key in state.inputs.keys():
            if state.inputs[key] == 1:
                chosen_input = key
        input_dict = {"input": chosen_input}

        if chosen_input == "Sip-n-Puff":
            for key in SNP_Drive_settings.keys():
                SNP_Drive_settings[key] = int(SNP_Drive_settings[key])
            settings_dictionary = {
                **input_dict,
                **state.settings['Drive']
            }
        else:
            combined_settings = {k: v for d in state.settings.values() if d is not None for k, v in d.items()}
            reversed_settings = {v: k for k, v in combined_settings.items()}
            settings_dictionary = {
                **input_dict,
                **reversed_settings
            }

        with open(settings_path, "w") as outfile:
            json.dump(
                settings_dictionary,
                outfile,
                indent=2)
        state.STATE = 1
        return jsonify({'message': 'Uploaded successfully'}), 200

    return app