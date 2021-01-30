import React from 'react';

import './transcript.css';

const Transcript = ({ transcript, isLoading }) => {
    return (
        <div className='transcript-container'>
            <h4 className='transcript-title'>Transcription</h4>
            { isLoading ? <div className='loading-icon' /> : <p className='transcription'>{transcript}</p> }
        </div>
    );
}

export default Transcript;