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

import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { WDIContext, ip } from '../App';
import ComboSelect from '../components/ComboSelect';

import '../general.css';

const Drive = () => {
  const { chosenInput } = useContext(WDIContext);
  const [inputOptions, setInputOptions] = useState([]);
  const [speedSettings, setSpeedSettings] = useState([]);
  const [driveSettings, setDriveSettings] = useState([]);
  const [errorSetting, setErrorSetting] = useState(null);
  const [layer, setLayer] = useState(0);
  const [numLayers, setNumLayers] = useState(0);

  useEffect(() => {
    const getOptions = async (event) => {
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

    const getLayer = async (event) => {
      const response = await fetch(ip.concat('/getLayers'));

      if (!response.ok) {
        console.error(`Error Get Layer: ${response.status}`);
      }
      const result = await response.json();
      setNumLayers(result.count);
    };

    const getSpeedSettings = async (event) => {
      const response = await fetch(ip.concat('/getSpeedSettings'));

      if (!response.ok) {
        console.error(`Error Get Speed Settings: ${response.status}`);
      }
      const result = await response.json();
      const settings = Object.keys(result).map(key => ({ setting: key, value: result[key] }));
      setSpeedSettings(settings);
    };

    getLayer();
    getOptions();
    getSpeedSettings();
  }, [chosenInput]);

  useEffect(() => {
    const getSettings = async (event) => {
      const response = await fetch(ip.concat(`/getDriveSettings?layer=${layer}`));

      if (!response.ok) {
        console.error(`Error Get Drive Settings: ${response.status}`);
      }

      const result = await response.json();
      const settings = Object.keys(result).map(key => ({ setting: key, value: result[key] }));
      setDriveSettings(settings);
    };

    getSettings();
    setErrorSetting(null);
  }
    , [layer]);

  const changeSettings = async (event) => {
    setErrorSetting(null);
    const updatedSettings = [...driveSettings];
    for (let i = 0; i < updatedSettings.length; i++) {
      if (updatedSettings[i].setting === event.target.name) {
        updatedSettings[i].value = event.target.value
      }
    }
    const response = await fetch(ip.concat('/changeSettings'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mode: 'Drive',
        layer: layer,
        setting: event.target.name,
        value: event.target.value
      }),
    });

    if (response.status === 409) {
      setErrorSetting([event.target.name, [], 409]);
      return;
    }

    setDriveSettings(updatedSettings);
    const result = await response.json();
    if (result.changed_setting !== null) {
      setErrorSetting([event.target.name, result.changed_setting, 200]);
      if (result.changed_setting[0] === 'Drive') {
        setDriveSettings(prevSettings => prevSettings.map(s =>
          s.setting === result.changed_setting[1] ? { ...s, value: 'N/A' } : s
        ));
      }
    } else {
      setErrorSetting(null);
    }
  };

  const changeSpeedSettings = async (event) => {
    setErrorSetting(null);
    const updatedSettings = [...speedSettings];
    for (let i = 0; i < updatedSettings.length; i++) {
      if (updatedSettings[i].setting === event.target.name) {
        updatedSettings[i].value = event.target.value
      }
    }
    const response = await fetch(ip.concat('/changeSpeedSettings'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        setting: event.target.name,
        value: parseInt(event.target.value)
      }),
    });
    if (!response.ok) {
      console.error(`Error Updating Speed Settings: ${response.status}`);
    } else {
      setSpeedSettings(updatedSettings)
    }
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Drive Settings</h1>

      <select className="select" value={layer} onChange={(e) => setLayer(parseInt(e.target.value))} style={{ fontSize: '20px', marginBottom: '40px' }}>
        {Array.from({ length: numLayers }, (_, i) => (
          <option key={i} value={i}>
            Layer {i + 1}
          </option>
        ))}
      </select>

      {speedSettings.map((s, index) => (
        <div key={index} style={{ marginBottom: '40px', display: 'grid' }}>
          <label style={{ fontSize: '25px', fontWeight: 'bold' }}>{s.setting}</label>
          <input
            type="number"
            name={s.setting}
            value={s.value}
            min={0}
            max={100}
            onChange={changeSpeedSettings}>
          </input>
        </div>
      ))}

      {driveSettings.map((s, index) => (
        <div key={index} style={{ marginBottom: '40px', display: 'grid' }}>
          <label style={{ fontSize: '25px', fontWeight: 'bold' }}>{s.setting}</label>
          <ComboSelect
            name={s.setting}
            value={s.value}
            inputOptions={inputOptions}
            onChange={changeSettings}
          />
          {errorSetting && errorSetting[0] === s.setting &&
            (errorSetting[2] === 409
            ? (<p style={{ color: 'red' }}>Can not set key as layer key.</p>)
            : (<p style={{ color: 'red' }}>{errorSetting[1][1]} ({errorSetting[1][0]}) set to "N/A"</p>)
            )}
        </div>
      ))}

      <Link to="/">
        <button className='button'>Home</button>
      </Link>
    </div>
  );
};

export default Drive;