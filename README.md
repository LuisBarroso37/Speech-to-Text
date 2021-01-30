### Speech-To-Text

This repository includes both the front-end and back-end of the application. 
The API is deployed on Cloud Run at [https://speech-to-text-ewyii4zxzq-ew.a.run.app](https://speech-to-text-ewyii4zxzq-ew.a.run.app). The endpoint to perform the transcription of the audio file is `/transcribe`.
The user interface is deployed on App Engine at [https://ml6-full-stack-challenge.ew.r.appspot.com](https://ml6-full-stack-challenge.ew.r.appspot.com).


The back-end is a wrapper around the Speech-To-Text API from Google Cloud. The API receives an uploaded .wav file, saves it in the Google Cloud Storage and then transcribes it. If the audio file is stereo or has a sample rate smaller than 16000Hz then it is converted into a mono audio file with 16000Hz. The API can be easily run locally by running docker. It is built using Flask and ffmpeg to convert audio files.

The front-end was created using React. It is a simple interface that allows users to upload a .wav file and get the transcription of the audio.

### Instructions
To run this the app locally:
  - Clone the repo

API:
  - Go into the API folder
  - Add your own service_account.json file from Google Cloud
  - Open the terminal and run `docker build -t [name-of-container] .`
  - Finally run `docker run -it speech`
 
Front-end:
  - Go into the client folder
  - Open the terminal and run `npm install` to install the dependencies
  - Finnaly run `npm start`

### Screenshots:

![screencapture-ml6-full-stack-challenge-ew-r-appspot-2021-01-30-11_45_45](https://user-images.githubusercontent.com/58770446/106354271-c44d3780-62f0-11eb-811f-3a6f5468bea6.png)