# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:31:35 2019

@author: erwan
"""


import re
import sys
import os
import pyaudio
import webrtcvad
from six.moves import queue
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

#Recording parameters
RATE = 16000
CHUNK = int(RATE / 33.33)  # 30ms


def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)


class Audiostream(object):
    def __init__(self,SAMPLING_RATE,CHUNK):
        self.sample_rate=SAMPLING_RATE
        self.chunk=CHUNK
        # Creation dun buffer pour stocker les echantillons
        self.buff = queue.Queue()
        # Set d'une variable pour monitorer l'activation ou non du stream audio
        self.close = True
        
    def __exit__(self,type, value, traceback):
        self.stream.stop_stream()
        self.stream.close()
        
        self.buff.put(None)
        self.p.terminate()
        self.close = True
        
    def __enter__(self):
        self.p = pyaudio.PyAudio()
        
        self.stream = self.p.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                output=True,
                frames_per_buffer=self.chunk,
                stream_callback=self.callback)
        self.close = False
        
        self.stream.start_stream()
        
        return self
        
    def callback(self,in_data, frame_count, time_info, flag):
        if self.VAD.is_speech(in_data,RATE):
            self.buff.put(in_data)
            return in_data, pyaudio.paContinue
        else:
            return in_data, pyaudio.paContinue
    
    def generateur(self):
        while not self.close:
            #recuperation d'un echantillon
            chunk=self.buff.get()

            
            #quitter la fonction si il n'y a pas d'échantillon
            if chunk is None:
                return
            
            data=[chunk]
            
            #on récupère tous les échantillons possible si ils sont disponibles (sans bloquer)
            #sinon on arrête la prediction
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
                
            yield b''.join(data)
                        
            
def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars,'\n')

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(quitter|quitté)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0

            
        

####### MAIN #######

# Initialisation Google API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= <LINK YOUR JSON FILE HERE>

client = speech.SpeechClient()

config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='fr-FR')

streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)



with Audiostream(RATE,CHUNK) as stre:
        audio_gen =  stre.generateur()

        requests = (types.StreamingRecognizeRequest(audio_content=content)
                  for content in audio_gen)
        
        responses = client.streaming_recognize(streaming_config, requests)
        
        listen_print_loop(responses)

print("exited")
