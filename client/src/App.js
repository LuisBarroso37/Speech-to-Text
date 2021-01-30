import React, { useState } from 'react';

import './App.css';

import Form from './components/form/form';
import Transcript from './components/transcript/transcript';

const App = () => {
  const [ transcript, setTranscript ] = useState('');
  const [ disabled, setDisabled ] = useState(false);
  const [ isLoading, setIsLoading ] = useState(false);
  const [ file, setFile ] = useState(null);

  const onTranscribe = () => {
    setDisabled(true);
    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    fetch('https://speech-to-text-ewyii4zxzq-ew.a.run.app/transcribe', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      for (let key in data) {
        setTranscript(data[key]);
      }
      
      setDisabled(false);
      setIsLoading(false);
      setFile(null);
    })
    .catch(err => console.log('error:', err));
  }

  return (
    <div className='app-container'>
      <div>
        <h1 className='title'>Speech To Text</h1>
      </div>
      <Form 
        onTranscribe={onTranscribe}
        disabled={disabled}
        file={file}
        setFile={setFile}
      />
      <Transcript 
        transcript={transcript}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
