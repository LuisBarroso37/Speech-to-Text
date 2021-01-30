# Importing libraries
from flask import Flask, request, jsonify
from google.cloud import speech
import os
from werkzeug.utils import secure_filename
from helper_functions import stereo_to_mono, upload_file_gcloud
from helper_functions import sample_rate_channel
from flask_cors import CORS

# Name of the bucket created
bucket_name = 'wavaudio'

# Filepath where audio files will be stored
filepath = './upload_folder/'

# Add environmental variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = set(['wav'])

app.config['UPLOAD_FOLDER'] = filepath


# Check if audio file extension is wav
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/transcribe", methods=["POST"])
def transcribeAudio():
    '''
    Uploads uploaded audio file to storage and transcribes it.
    Converts audio file to mono or to a higher sample rate if necessary.
    '''
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_location)
    else:
        return jsonify({'error': 'Could not save file'})

    # Get sample rate and number of channels of audio file
    sample_rate, channels = sample_rate_channel(file_location)

    # Convert stereo file into mono, if necessary
    if sample_rate < 16000 or channels > 1:
        new_filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], 'mono_' + filename)
        stereo_to_mono(file_location, new_filepath)
        upload_file_gcloud(bucket_name, new_filepath, filename)
    else:
        # Upload original file to google cloud storage bucket
        upload_file_gcloud(bucket_name, filepath, filename)

    # Instantiate the client
    client = speech.SpeechClient()

    # Get audio by using google cloud URI
    gsc_uri = 'gs://' + bucket_name + '/' + filename
    audio = speech.RecognitionAudio(uri=gsc_uri)

    # Configuration for audio file with .wav extension
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,
        use_enhanced=True,
        model="phone_call"
    )

    # Detect speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=10000)

    # Get transcription of audio file
    transcript = ''
    for result in response.results:
        print(result)
        transcript += result.alternatives[0].transcript

    # Remove files from upload_folder
    files = os.listdir(filepath)
    for f in files:
        os.unlink(os.path.join(filepath, f))
    print(transcript)
    return jsonify({'transcript': transcript})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
