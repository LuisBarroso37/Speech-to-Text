import React, { useRef, useState } from 'react';

import './form.css'

import uploadIcon from '../../assets/cloud_upload-24px.svg';

const Form = ({ onTranscribe, disabled, file, setFile }) => {
    const fileInputRef = useRef(null);
    const [ highlight, setHighlight ] = useState(false);
    
    const openFileFolder = () => {
        if (disabled) return;
        fileInputRef.current.click();
    }

    const onDragOver = (event) => {
        event.stopPropagation();
        event.preventDefault();

        if (disabled) return;
        setHighlight(true);
    }

    const onDragLeave = () => {
        setHighlight(false);
    }

    const onDrop = (event) => {
        event.preventDefault();
        
        if (disabled) return;
        setFile(event.dataTransfer.files[0]);
        setHighlight(false);
    }

    const onChange = (event) => {
        event.preventDefault();
        setFile(event.target.files[0]);
    }

    const handleUpload = (event) => {
        event.preventDefault();
        onTranscribe();
    }

    return (
        <div className='upload-form-container'>
            <form className='upload-form' encType='multipart/form-data'>
                <div 
                    className={`dropzone ${highlight ? 'highlight' : ''}`} 
                    onClick={() => openFileFolder()}
                    onDragOver={onDragOver}
                    onDragLeave={onDragLeave}
                    onDrop={onDrop}
                >
                    <img
                        alt='Upload icon'
                        className='upload-icon'
                        src={uploadIcon}
                    />
                    <input
                        ref={fileInputRef}
                        className='file-input'
                        type='file'
                        accept = '.wav'
                        onChange={onChange}
                        disabled={disabled}
                    />
                    <span className='upload-file-text'>{file ? file.name : 'Upload file'}</span>
                </div>
                <input 
                    className='transcribe-button' 
                    type='submit' 
                    value='Transcribe'
                    onClick={handleUpload}
                    disabled={disabled}
                />
            </form>
        </div>
    );
}

export default Form;