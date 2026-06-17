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

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { ip } from '../App';

import '../general.css';

const SNP = () => {
  const [driveSettings, setDriveSettings] = useState([]);

  useEffect(() => { document.title = "SNP Settings | WIR"; }, []);

  useEffect(() => {
    const getSettings = async () => {
      const response = await fetch(ip.concat('/getDriveSettings'));

      if (!response.ok) {
        console.error(`Error Get Drive Settings: ${response.status}`);
      }

      const result = await response.json();
      const settings = Object.keys(result).map(key => ({ setting: key, value: result[key] }));
      console.log(settings);
      setDriveSettings(settings);
    };

    getSettings();
  }, []);

  const changeSettings = async (event) => {
    const updatedSettings = [...driveSettings];
    for (let i = 0; i < updatedSettings.length; i++) {
      if (updatedSettings[i].setting === event.target.name) {
        updatedSettings[i].value = event.target.value
      }
    }
    setDriveSettings(updatedSettings)
    const response = await fetch(ip.concat('/changeSettings'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mode: 'Drive',
        setting: event.target.name,
        value: event.target.value
      }),
    });
    if (!response.ok) {
      console.error(`Error Updating Drive Settings: ${response.status}`);
    }
  };


  return (
    <div className="page">
      <h1>SNP</h1>

      {driveSettings.map((s, index) => (
        <div key={index} className="settings-row">
          <label className="settings-label">{s.setting}</label>
          <input
            type="number"
            name={s.setting}
            className="number-input"
            min={-100}
            max={100}
            value={s.value}
            onChange={changeSettings}
          />
        </div>
      ))}
      <Link to="/" className="button">Home</Link>
    </div>
  );
};

export default SNP;