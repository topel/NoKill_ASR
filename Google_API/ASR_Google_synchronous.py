# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:48:54 2019
@author: erwan Gateau-Magdeleine

Scrip permettant la reconnaissance automatique de parole en utilisant l'API google pour des fichiers courts (<1min)
Le fihier doit être au format .wav. La transcription est automatiquement ecrite dans un fichier texte.

utilisation :
python3 ASR_synchronous.py <file_name> <out_path> <transcription name>

"""
import os
import sys
import io
from pydub import AudioSegment
import wave



def frame_rate_channel(audio_file_name):
    # Récupere la frequence d'echantillonage et le nombre de canaux
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
    return frame_rate,channels

def stereo_to_mono(audio_file_name):
    # Transforme un son stereo en un son mono
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")
  
def transcribe_file_multiple_speakers(speech_file):
    '''
    Permet la transcription d'un fichier audio en texte en utilisant un process synchrone
    Le fichier doit être < 1min
    '''
    trans = ''
    conf = []
    frame_rate,channels = frame_rate_channel(speech_file)
    
    # Si plus de 1 cannal dans le fichier audio
    if channels > 1:
        stereo_to_mono(speech_file)
        
    #from google.cloud import speech
    #from google.cloud.speech import enums
    #from google.cloud.speech import types
    
    from google.cloud import speech_v1p1beta1 as speech
    
    client = speech.SpeechClient()
    
    with io.open(speech_file,'rb') as audio_file:
         content = audio_file.read() #permet d'avoir un fichier binaire en bytes
         
    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        enable_speaker_diarization=True, # Permet d'activer l'option de plusieurs speakers
        diarization_speaker_count=2, # donne le nombre de sources differentes
        #enable_automatic_punctuation=True, # Active la ponctuation automatique : ne fonctionne pas!!
        language_code='fr-FR')
    
    response = client.recognize(config, audio)
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        trans += result.alternatives[0].transcript
        conf.append(result.alternatives[0].confidence)
    
    words_info = result.alternatives[0].words
    for word_info in words_info:
        print("word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag))
    
    return trans,conf

def transcribe_file_simple_speaker(speech_file):
    '''
    Permet la transcription d'un fichier audio en texte en utilisant un process synchrone
    Le fichier audio doit être < 1min
    '''
    trans = ''
    conf = []
    frame_rate,channels = frame_rate_channel(speech_file)
    
    # Si plus de 1 cannal dans le fichier audio
    if channels > 1:
        stereo_to_mono(speech_file)
        
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
        
    client = speech.SpeechClient()
    
    with io.open(speech_file,'rb') as audio_file:
         content = audio_file.read() #permet d'avoir un fichier binaire en bytes
         
    audio = speech.types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        use_enhanced = True, 
        #enable_automatic_punctuation=True, # Active la ponctuation automatique : ne fonctionne pas en français!!
        language_code='fr-FR',
        #use_enhanced=True,
        #model = 'command_and_search'
        #speech_contexts=[speech.types.SpeechContext(phrases=['quel sens l''IA va bouleverser','liés aux progrès de L''IA à envisager','Turing','Test'])]
	)
    
    response = client.recognize(config, audio)
    
    #response = operation.result()
    
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        trans += result.alternatives[0].transcript
        conf.append(result.alternatives[0].confidence)
    
    return trans,conf

def ecriture_transcription(trans_filename,trans):
    f= open(trans_filename,"w+")
    f.write(trans)
    f.close()
    
    
if len(sys.argv) != 4:
    print("mauvaise utilisation !!")
    print("utilisation :")
    print("python3 ASR_synchronous.py <file_name> <out_path> <transcription name>")
    sys.exit()
else:
    file_name = sys.argv[1]
    print(file_name)
    output_path =sys.argv[2]
    trans_name=sys.argv[3]

# Definition de la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=<LINK YOUR JSON HERE>

# Transcription du texte en utilisant l'API GOOGLE
transcription,confidence = transcribe_file_simple_speaker(file_name)

# Ecriture de la transcription dans un fichier

ecriture_transcription(output_path+trans_name,transcription)

# Affichage de la transcription
print(transcription)

