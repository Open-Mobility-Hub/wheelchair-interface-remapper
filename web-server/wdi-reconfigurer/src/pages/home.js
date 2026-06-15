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

import '../general.css';

const Home = () => {
  const { chosenInput, setChosenInput } = useContext(WDIContext);
  const [inputs, setInputs] = useState([]);
  const [inputDevice, setInputDevice] = useState('');
  const [devices, setDevices] = useState([]);
  const [numLayers, setNumLayers] = useState(0);
  const [layer, setLayer] = useState(0);
  const [layerKey, setLayerKey] = useState('');
  const [inputOptions, setInputOptions] = useState([]);
  const [errorSetting, setErrorSetting] = useState(null);

  useEffect(() => {
    const getInputs = async () => {
      const response = await fetch(ip.concat('/getInputs'));
      if (!response.ok) {
        console.error(`Error Get Inputs: ${response.status}`);
        return;
      }
      const result = await response.json();
      const inputTypes = Object.keys(result).map(key => ({ type: key, value: result[key] }));
      setInputs(inputTypes);
      inputTypes.forEach((i) => {
        if (i.value === 1) {
          setChosenInput(i.type);
          return;
        }
      });
    };

    const getDevices = async () => {
      const response = await fetch(ip.concat('/getDevices'));
      if (!response.ok) {
        console.error(`Error Get Devices: ${response.status}`);
        return;
      }
      const result = await response.json();
      setDevices(result);
      const selected = result.find(d => d[2] === 1);
      if (selected) {
        setInputDevice(selected[1]);
      }
    };

    getInputs();
    getDevices();
  }, []);

  useEffect(() => {
    const getLayer = async () => {
      const response = await fetch(ip.concat('/getLayers'));
      if (!response.ok) {
        console.error(`Error Get Layer: ${response.status}`);
        return;
      }
      const result = await response.json();
      setNumLayers(result.count);
    };

    const getLayerKey = async () => {
      const response = await fetch(ip.concat('/getLayerKey'));
      if (!response.ok) {
        console.error(`Error Get Layer Key: ${response.status}`);
        return;
      }
      const result = await response.json();
      setLayerKey(result.layer_key ?? '');
    };

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
        return;
      }
      const result = await response.json();
      setInputOptions(result);
    };

    getLayer();
    getLayerKey();
    getOptions();
  }, [chosenInput]);



  const changeInput = async (event) => {
    const value = event.target.value;
    const response = await fetch(ip.concat('/changeInput'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event.target.value),
    });

    if (!response.ok) {
      console.error(`Error Change Input: ${response.status}`);
    } else {
      setChosenInput(value);
    }
  };

  const changeDevice = async (event) => {
    setInputDevice(event.target.value);
    const response = await fetch(ip.concat('/selectDevice'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event.target.value),
    });

    if (!response.ok) {
      console.error(`Error Change Device: ${response.status}`);
    }
  };

  const addLayer = async () => {
    const response = await fetch(ip.concat('/addLayer'), {
      method: 'POST',
    });

    if (!response.ok) {
      console.error(`Error Add Layer: ${response.status}`);
    } else {
      setNumLayers(numLayers + 1);
    }
  };

  const deleteLayer = async () => {
    const response = await fetch(ip.concat('/deleteLayer'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(layer),
    });

    if (!response.ok) {
      console.error(`Error Delete Layer: ${response.status}`);
    } else {
      setNumLayers(numLayers - 1);
      setLayer(0);
    }
  };

  const changeLayerKey = async (event) => {
    const value = event.target.value;
    const response = await fetch(ip.concat('/changeLayerKey'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event.target.value),
    });

    if (!response.ok) {
      console.error(`Error Change Layer Key: ${response.status}`);
      return
    }

    const result = await response.json();
    if (result.changed_settings.length > 0) {
      setErrorSetting(result.changed_settings);
    } else {
      setErrorSetting(null);
    }
    setLayerKey(value);
  };

  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>Wheelchair Interface Remapper</h1>

      <div style={{ textAlign: 'center' }}>
        <form>
          <label style={{ fontSize: '25px' }}>Chosen Input: </label>
          <select name="input" className="select" value={chosenInput} onChange={changeInput}>
            {inputs.map((option) => (
              <option key={option.type} value={option.type}>
                {option.type}
              </option>
            ))}
          </select>
        </form>
      </div>

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <form>
          <label style={{ fontSize: '25px' }}>Input Device: </label>
          <select name="device" className="select" value={inputDevice} onChange={changeDevice}>
            <option value="">NONE</option>
            {devices.map((option) => (
              <option key={option[1]} value={option[1]}>
                {option[0]}
              </option>
            ))}
          </select>
        </form>
      </div>

      <hr style={{ borderTopWidth: '3px' }} />

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <p style={{ textAlign: 'center', fontSize: '25px' }}>Number of Layers: {numLayers}</p>
        {numLayers < 3 ?
          <button className="button" onClick={addLayer}>
            Add Layer
          </button>
          : <button className="button" disabled>
            Max Layers Reached
          </button>}
        <select
          value={layer}
          onChange={(e) => setLayer(parseInt(e.target.value))}
          className="select" style={{ marginLeft: '20px', marginRight: '20px' }}>
          {Array.from({ length: numLayers }, (_, i) => (
            <option key={i} value={i}>
              Layer {i + 1}
            </option>
          ))}
        </select>
        {numLayers > 1 ?
          <button className="button" onClick={deleteLayer}>
            Delete Layer
          </button>
          : <button className="button" disabled>
            Need At Least 1 Layer
          </button>
        }
      </div>

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <form>
          <label style={{ fontSize: '25px' }}>Layer Key: </label>
          <select name="layerKey" className="select" value={layerKey} onChange={changeLayerKey}>
            <option value="">--None--</option>
            {inputOptions.map(opt => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        </form>
      </div>

      {errorSetting && errorSetting.map((s, index) => (
        <p key={index} style={{ color: 'red', textAlign: 'center' }}>
          Layer: {s[0]}, Setting {s[2]} in mode {s[1]} set to "N/A"</p>
      ))}

      <hr style={{ borderTopWidth: '3px' }} />

      {chosenInput !== 'Sip-n-Puff' ?
        (
          <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column' }}>
            <Link to="/drive">
              <button className="button"
                style={{ marginBottom: '20px', marginTop: '10px' }}>Drive Settings
              </button>
            </Link>
            <Link to="/chair">
              <button className="button"
                style={{ marginBottom: '20px' }}>Chair Settings
              </button>
            </Link>
            <Link to="/profile">
              <button className="button"
                style={{ marginBottom: '20px' }}>Profile Settings
              </button>
            </Link>
            <Link to="/memory">
              <button className="button"
                style={{ marginBottom: '20px' }}>Memory Settings
              </button>
            </Link>
            <Link to="/seating">
              <button className="button"
                style={{ marginBottom: '10px' }}>Seating Settings
              </button>
            </Link>
          </div>
        ) :
        (<div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column' }}>
          <Link to="/snp">
            <button className="button"
              style={{ marginBottom: '10px', marginTop: '10px' }}>SNP Settings
            </button>
          </Link>
        </div>
        )}

      <hr style={{ borderTopWidth: '3px' }} />

      {inputDevice ? (
        <div style={{ textAlign: 'center' }}>
          <Link to="/upload">
            <button className="button"
              style={{ marginBottom: '20px', marginTop: '20px' }}>Upload Settings
            </button>
          </Link>
        </div>
      ) :
        <div style={{ textAlign: 'center' }}>
          <button className="button" disabled
            style={{ marginBottom: '20px', marginTop: '20px' }}>Select device to upload.
          </button>
        </div>
      }

    </div>
  );
};

export default Home;