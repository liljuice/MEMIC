from django.shortcuts import render, redirect, HttpResponse
from .forms import FileUploadForm
from .models import FileUpload
from pytube import *
import librosa
import soundfile
from pydub import AudioSegment
import os
from django.contrib import messages
from wsgiref.util import FileWrapper
from django.core.files.storage import default_storage
from django.http import HttpResponse
from storages.backends.s3boto3 import S3Boto3Storage
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from .forms import DocumentForm
import boto3
from botocore.exceptions import NoCredentialsError
def upload_to_s3(local_file_path, s3_file_path):
    """
    Uploads a file to an S3 bucket
    """
    access_key = 'access key'
    secret_key = 'secret key'
    bucket_name = 'memicbucket'

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def fileUpload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.cleaned_data['audiofile']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            y, sr = librosa.load(audio_file)
            y = y[start * sr:end * sr]
            current_directory = os.path.dirname(os.path.abspath(__file__))
            processed_file_path = os.path.join(current_directory, 'processed_audio.wav')
            soundfile.write(processed_file_path, y, sr)
            s3_file_path = 'MyFile/' + os.path.basename(processed_file_path)
            upload_to_s3(processed_file_path, s3_file_path)
            return HttpResponse('Audio processing complete. Processed file saved at {}'.format(processed_file_path))
            # try:
            #     y, sr = librosa.load(audio_file)
            #     y = y[int(start * sr):int(end * sr)]
            #     current_directory = os.path.dirname(os.path.abspath(__file__))
            #     processed_file_path = os.path.join(current_directory, 'processed_audio.wav')
            #     soundfile.write(processed_file_path, y, sr)
            #     return HttpResponse('Audio processing complete. Processed file saved at {}'.format(processed_file_path))
            # except Exception as e:
            #     # Handle exceptions, e.g., if librosa fails to load the file
            #     return HttpResponse(f'Error processing audio dsfsdfsdfsdf: {str(e)}', status=500)
    else:
        form = FileUploadForm()

    return render(request, 'fileupload.html', {'form': form})
def youtube(request):
    # checking whether request.method is post or not
    if request.method == 'POST':
        # getting link from frontend
        link = request.POST['link']
        start = request.POST['start']
        end = request.POST['end']
        video = YouTube(link)

        # downloading video -> wav
        audio = video.streams.filter(only_audio=True).first()
        downloaded_file = audio.download()
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.wav'
        os.rename(downloaded_file, new_file)
        # cutting audio
        y, sr = librosa.load(new_file)
        print(sr)
        print(start)
        print(sr*int(start))
        start = (int(start) * int(sr))
        end = (int(end) * int(sr))
        y = y[start:end]
        soundfile.write(new_file, y, sr)

        # extracting voice and accompaniment
        path = os.path.dirname(new_file)
        file_name = os.path.basename(new_file)
        #stems = str(input('stems 선택 : 2, 4, 5 >>> '))

        stems = '2'

        nsfile_name = file_name.replace(' ', '_')
        try:
            os.rename(new_file, path + '/' + nsfile_name)
            # os.rename(path + file_name, path + nsfile_name)
        except FileNotFoundError:
            pass

        s3_file_path = 'MyFile/' + os.path.basename(new_file)
        upload_to_s3(path + '/' + nsfile_name, s3_file_path)
        print('기다려주세요.')
        spl = r'spleeter separate -p spleeter:' + \
              str(stems) + r'stems -o output ' + nsfile_name
        os.system(spl)

        # converting wav -> mp3
        # returning HTML page
        return render(request, 'youtube.html')

    return render(request, 'youtube.html')