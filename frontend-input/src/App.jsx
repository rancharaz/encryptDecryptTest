import React, { useState } from 'react';

function EncryptForm() {
  const [data, setData] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [dataId, setDataId] = useState('');
  const [decryptedData, setDecryptedData] = useState('');

  // Handle input change for encryption
  const handleInputChange = (event) => {
    setData(event.target.value);
  };

 

  // Handle input change for decryption
  const handleDataIdChange = (event) => {
    setDataId(event.target.value);
  };

  // Handle encryption form submission
  const handleEncryptSubmit = async (event) => {
    event.preventDefault();

    // Send POST request to Flask backend for encryption
    const response = await fetch('http://localhost:5000/encrypt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data }),
    });

    const result = await response.json();
    if (response.ok) {
      setResponseMessage(result.message);
    } else {
      setResponseMessage(result.error);
    }
  };

  // Handle decryption form submission
  const handleDecryptSubmit = async (event) => {
    event.preventDefault();

    // Send GET request to Flask backend for decryption
    const response = await fetch(`http://localhost:5000/decrypt/${dataId}`);

    const result = await response.json();
    if (response.ok) {
      setDecryptedData(result.decrypted_data);
    } else {
      setDecryptedData(result.error);
    }
  };

  return (
    <div>
    <div className='bg-slate-600 h-screen '>
      <div className='mx-auto text-center bg-white w-[30rem] p-10 rounded-md drop-shadow-lg mt-12'>
        <h2>Encrypt Data</h2>
        <form onSubmit={handleEncryptSubmit}>
          <input
            className='border-1 p-2 rounded-md mr-8'
            type="text"
            value={data}
            onChange={handleInputChange}
            placeholder="Enter text to encrypt"
            required
          />
          <button className='bg-slate-400 p-2 rounded-md cursor-pointer hover:bg-slate-600 hover:text-white transition-all' type="submit">Submit</button>
          </form>
        <div>{responseMessage && <p>{responseMessage}</p>}</div>
        <div className="mb-5"></div>
        <h2>Decrypt Data</h2>
        <form onSubmit={handleDecryptSubmit}>
          <input
            className='border-1 p-2 rounded-md mr-8'
            type="number"
            value={dataId}
            onChange={handleDataIdChange}
            placeholder="Enter data ID to decrypt"
            required
          />
          <button className='bg-slate-400 p-2 rounded-md cursor-pointer hover:bg-slate-600 hover:text-white transition-all' type="submit">Decrypt</button>
          </form>
        <div>{decryptedData && <p>Decrypted Data: {decryptedData}</p>}</div>
      </div>
    </div>

    </div>

  );
}

export default EncryptForm;
