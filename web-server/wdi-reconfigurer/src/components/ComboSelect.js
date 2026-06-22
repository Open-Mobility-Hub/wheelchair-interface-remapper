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

import React from 'react';

const MODIFIER_EXCLUDED = (opt) =>
    opt.startsWith("POS_ABS_") ||
    opt.startsWith("NEG_ABS_") ||
    opt.startsWith("DPAD_");

const ComboSelect = ({ value, name, inputOptions, onChange }) => {
    const [modifier, key] = value && value.includes('+')
        ? value.split('+', 2)
        : ['', value || ''];

    const modifierOptions = inputOptions.filter(opt => !MODIFIER_EXCLUDED(opt));

    const handleChange = (newModifier, newKey) => {
        const newValue = newModifier ? `${newModifier}+${newKey}` : newKey;
        onChange({ target: { name, value: newValue } });
    };

    return (
        <div className="combo-select">
            <select
                className="select"
                value={modifier}
                onChange={(e) => handleChange(e.target.value, key)}
            >
                <option value="">--None--</option>
                {modifierOptions.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                ))}
            </select>
            <span>+</span>
            <select
                className="select"
                value={key}
                onChange={(e) => handleChange(modifier, e.target.value)}
            >
                <option value="">--Default--</option>
                {inputOptions.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                ))}
            </select>
        </div>
    );
};

export default ComboSelect;