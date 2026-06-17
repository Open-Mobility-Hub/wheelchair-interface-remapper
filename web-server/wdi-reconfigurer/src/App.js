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

import React, { useState, createContext } from 'react';

import {
  BrowserRouter as Router, Routes, Route
} from "react-router-dom";
import Home from "./pages/home";
import Drive from "./pages/drive";
import Chair from "./pages/chair";
import Profile from "./pages/profile";
import Memory from "./pages/memory";
import Seating from "./pages/seating";
import Upload from "./pages/upload";

export const WDIContext = createContext();
export const ip = process.env.REACT_APP_API_URL || "http://localhost:5000";

function App() {

  const [chosenInput, setChosenInput] = useState('NONE');

  return (
    <WDIContext.Provider value={{ chosenInput, setChosenInput }}>
      <Router>
        <Routes>
          <Route path='/' element={<Home />}></Route>
          <Route path='/drive' element={<Drive />}></Route>
          <Route path='/chair' element={<Chair />}></Route>
          <Route path='/profile' element={<Profile />}></Route>
          <Route path='/memory' element={<Memory />}></Route>
          <Route path='/seating' element={<Seating />}></Route>
          <Route path='/upload' element={<Upload />}></Route>
        </Routes>
      </Router>
    </WDIContext.Provider>
  );
}

export default App;
