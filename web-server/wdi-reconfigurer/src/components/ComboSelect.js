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
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
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
            {modifier && <span>+</span>}
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