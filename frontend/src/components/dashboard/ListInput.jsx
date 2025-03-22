import React, { useState } from 'react';
import { Input, Button } from 'rsuite';

const ListInput = ({ title, field }) => {
  const [inputValue, setInputValue] = useState(field || ''); // Fix: Initialize from 'field'

  console.log("title:", title); // Debugging

  // Capture input change
  const handleChange = (value) => {
    setInputValue(value);
  };

  // Handle submit button click
  const handleSubmit = () => {
    alert(`Submitted value: ${title} ${inputValue}`);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>{title}</h3>
      <Input placeholder="Enter text..." value={inputValue} onChange={handleChange} />
      <Button appearance="primary" onClick={handleSubmit} style={{ marginTop: '10px' }}>
        Submit
      </Button>
    </div>
  );
};

export default ListInput;
