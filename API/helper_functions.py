# Importing libraries
import wave
from google.cloud import storage
import ffmpeg


def stereo_to_mono(file_location, new_filepath):
    '''
    Converts stereo audio files into mono audio files
    '''
    ffmpeg.input(file_location).output(new_filepath, ac=1, ar=16000).run(overwrite_output=True)


def sample_rate_channel(file_location):
    '''
    Returns the sample rate
    and the number of channels of the audio file
    '''
    with wave.open(file_location, 'rb') as wave_file:
        sample_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return sample_rate, channels


def upload_file_gcloud(bucket_name, source_filepath, file_name):
    '''
    Uploads a file to the google cloud storage bucket
    '''
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(source_filepath)
