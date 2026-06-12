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

  useEffect(() => {
    const getInputs = async () => {
      const response = await fetch(ip.concat('/getInputs'))
      if (!response.ok) {
        console.error(`Error Change Input: ${response.status}`);
      }
      const result = await response.json();

      const inputDevices = Object.keys(result).map(key => ({ type: key, value: result[key] }));
      console.log(inputDevices);
      setInputs(inputDevices);

      inputDevices.forEach((i) => {
        if (i.value === 1) {
          setChosenInput(i.type)
          return;
        }
      });
    };

    getInputs();
  }, [setChosenInput]);



  const changeInput = async (event) => {
    setChosenInput(event.target.value);
    const response = await fetch(ip.concat('/changeInput'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event.target.value),
    });

    if (!response.ok) {
      console.error(`Error Change Input: ${response.status}`);
    }
  };

  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>WDI Remapper</h1>

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

      <div style={{ textAlign: 'center' }}>
        <Link to="/upload">
          <button className="button"
            style={{ marginBottom: '20px', marginTop: '20px' }}>Upload Settings
          </button>
        </Link>
      </div>

    </div>
  );
};

export default Home;