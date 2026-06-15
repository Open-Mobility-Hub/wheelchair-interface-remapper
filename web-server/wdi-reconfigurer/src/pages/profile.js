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
import {Link} from "react-router-dom";
import { WDIContext, ip } from '../App';
import ComboSelect from '../components/ComboSelect';

import '../general.css';

const Profile = () => {
    const { chosenInput } = useContext(WDIContext);
  const [inputOptions, setInputOptions] = useState([]);
  const [profileSettings, setProfileSettings] = useState([]);
  const [errorSetting, setErrorSetting] = useState(null);

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

    const getSettings = async (event) => {
      const response = await fetch(ip.concat('/getProfileSettings'));

      if (!response.ok) {
        console.error(`Error Get Profile Settings: ${response.status}`);
      }

      const result = await response.json();
      const settings = Object.keys(result).map(key => ({ setting: key, value: result[key] }));
      setProfileSettings(settings);
    };

    getOptions();
    getSettings();
  }, [chosenInput]);

  const changeSettings = async (event) => {
    setErrorSetting(null);
    const updatedSettings = [...profileSettings];
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
        mode: 'Profile',
        setting: event.target.name,
        value: event.target.value}),
    });
    if (!response.ok) {
      if (response.status === 409) {
        setErrorSetting([event.target.name, event.target.value]);
      }
      console.error(`Error Updating Profile Settings: ${response.status}`);
    } else {
      setProfileSettings(updatedSettings)
    }
  };


  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Profile Settings</h1>

      {profileSettings.map((s, index) => (
        <div key={index} style={{marginBottom: '40px', display: 'grid'}}>
          <label style={{ fontSize: '25px', fontWeight: 'bold'}}>{s.setting}</label>
          <ComboSelect
            name={s.setting}
            value={s.value}
            inputOptions={inputOptions}
            onChange={changeSettings}
          />
          {errorSetting && errorSetting[0] === s.setting && <p style={{color: 'red'}}>{errorSetting[1]} is already in use.</p>}
        </div>
      ))}

      <Link to="/">
        <button className='button'>Home</button>
      </Link>
    </div>
  );
};

export default Profile;