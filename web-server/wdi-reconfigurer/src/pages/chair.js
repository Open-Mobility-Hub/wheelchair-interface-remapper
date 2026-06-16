/*
 * Copyright 2024-2026 Joel Goh
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { useState, useEffect, useContext } from 'react';
import { Link } from "react-router-dom";
import { WDIContext, ip } from '../App';
import ComboSelect from '../components/ComboSelect';

import '../general.css';

const Chair = () => {
  const { chosenInput } = useContext(WDIContext);
  const [inputOptions, setInputOptions] = useState([]);
  const [chairSettings, setChairSettings] = useState([]);
  const [errorSetting, setErrorSetting] = useState(null);
  const [layer, setLayer] = useState(0);
  const [numLayers, setNumLayers] = useState(0);

  useEffect(() => {
    const getOptions = async () => {
      const response = await fetch(ip.concat('/getOptions'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(chosenInput),
      });

      if (!response.ok) {
        console.error(`Error Get Options: ${response.status}`);
      }

      const result = await response.json();
      setInputOptions(result);
    };

    const getLayer = async () => {
      const response = await fetch(ip.concat('/getLayers'));

      if (!response.ok) {
        console.error(`Error Get Layer: ${response.status}`);
      }
      const result = await response.json();
      setNumLayers(result.count);
    };

    getLayer();
    getOptions();
  }, [chosenInput]);

  useEffect(() => {
    getSettings();
    setErrorSetting(null);
  }, [layer]);

  const getSettings = async () => {
    const response = await fetch(ip.concat(`/getChairSettings?layer=${layer}`));

    if (!response.ok) {
      console.error(`Error Get Chair Settings: ${response.status}`);
    }

    const result = await response.json();
    const settings = Object.keys(result).map(key => ({ setting: key, value: result[key] }));
    setChairSettings(settings);
  };

  const changeSettings = async (event) => {
    setErrorSetting(null);
    const updatedSettings = [...chairSettings];
    for (let i = 0; i < updatedSettings.length; i++) {
      if (updatedSettings[i].setting === event.target.name) {
        updatedSettings[i].value = event.target.value;
      }
    }
    const response = await fetch(ip.concat('/changeSettings'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mode: 'Chair',
        layer: layer,
        setting: event.target.name,
        value: event.target.value
      }),
    });
    setChairSettings(updatedSettings);

    const result = await response.json();
    if (result.changed_setting !== null) {
      setErrorSetting([event.target.name, result.changed_setting]);
    } else {
      setErrorSetting(null);
    }
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Chair Settings</h1>

      <select value={layer} onChange={(e) => setLayer(parseInt(e.target.value))} style={{ fontSize: '20px', marginBottom: '40px' }}>
        {Array.from({ length: numLayers }, (_, i) => (
          <option key={i} value={i}>
            Layer {i}
          </option>
        ))}
      </select>

      {chairSettings.map((s, index) => (
        <div key={index} style={{ marginBottom: '40px', display: 'grid' }}>
          <label style={{ fontSize: '25px', fontWeight: 'bold' }}>{s.setting}</label>
          <ComboSelect
            name={s.setting}
            value={s.value}
            inputOptions={inputOptions}
            onChange={changeSettings}
          />
          {errorSetting && errorSetting[0] === s.setting && <p style={{ color: 'red' }}>
            {errorSetting[1][1]} ({errorSetting[1][0]}) set to "N/A"</p>}
        </div>
      ))}

      <Link to="/">
        <button className='button'>Home</button>
      </Link>
    </div>
  );
};

export default Chair;
