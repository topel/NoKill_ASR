#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# example program for kaldi live nnet3 chain online decoding
#
# configured for embedded systems (e.g. an rpi3) with models
# installed in /opt/kaldi/model/
#

import traceback
import logging
import datetime

import webrtcvad
from time                  import time
from nltools               import misc
from nltools.pulserecorder import PulseRecorder
from nltools.vad           import VAD, BUFFER_DURATION
from nltools.asr           import ASR, ASR_ENGINE_NNET3
from optparse              import OptionParser
import sys
import io
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
PROC_TITLE                       = 'kaldi_live_demo'

DEFAULT_VOLUME                   = 150
DEFAULT_AGGRESSIVENESS           = 1

# DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-de-tdnn_250'
#DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-en-tdnn_250'

DEFAULT_MODEL_DIR                = '/home/pellegri/tools/ASR_DEMO_SAMOVA/DEMO_MEETUP/model'
DEFAULT_ACOUSTIC_SCALE           = 1.0
DEFAULT_BEAM                     = 7.0
DEFAULT_FRAME_SUBSAMPLING_FACTOR = 3

STREAM_ID                        = 'mic'

#
# init
#


if len(sys.argv) !=2:
    print "mauvais usage : "
    print "python file_kaldi_decode_live.py <file_name>"
    sys.exit()
misc.init_app(PROC_TITLE)

print "Kaldi live demo V0.2"

#
# cmdline, logging
#

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-a", "--aggressiveness", dest="aggressiveness", type = "int", default=DEFAULT_AGGRESSIVENESS,
                   help="VAD aggressiveness, default: %d" % DEFAULT_AGGRESSIVENESS)

parser.add_option ("-m", "--model-dir", dest="model_dir", type = "string", default=DEFAULT_MODEL_DIR,
                   help="kaldi model directory, default: %s" % DEFAULT_MODEL_DIR)

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

parser.add_option ("-s", "--source", dest="source", type = "string", default=None,
                   help="pulseaudio source, default: auto-detect mic")

parser.add_option ("-V", "--volume", dest="volume", type = "int", default=DEFAULT_VOLUME,
                   help="broker port, default: %d" % DEFAULT_VOLUME)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

source         = options.source
volume         = options.volume
aggressiveness = options.aggressiveness
model_dir      = options.model_dir

#
# pulseaudio recorder
#

#rec = PulseRecorder (source_name=source, volume=volume)

#
# VAD
#

vad = VAD(aggressiveness=aggressiveness)

#
# ASR


print "Loading model from %s ..." % model_dir

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = model_dir,
          kaldi_beam = DEFAULT_BEAM, kaldi_acoustic_scale = DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor = DEFAULT_FRAME_SUBSAMPLING_FACTOR)


#
# main
#


finalize=False
stream_file = sys.argv[1]

audio_content = AudioSegment.from_wav(stream_file)
audio_content = audio_content.set_channels(1) # Stereo to mono

chunks_length_ms = 30

chunks = make_chunks(audio_content, chunks_length_ms)

for samples in chunks:
    sample = samples.get_array_of_samples()
    sample = np.int16(sample)

    if len(sample) < 480 :
	add = np.zeros((480-len(sample),))
        add=np.int16(add)
	sample = np.concatenate((sample,add))

    #audio, finalize = vad.process_audio(sample)
    #if not audio:
    #    continue
    logging.debug ('decoding audio len=%d finalize=%s audio=%s' % (len(sample), repr(finalize), sample[0].__class__))
    
    user_utt, confidence = asr.decode(sample, finalize, stream_id=STREAM_ID)
    
    #print "\r%s                     " % user_utt,
    print "\r%s                     " % user_utt,
    if finalize:
        print "\r%s                     " % user_utt,
        print "New Utterance\n"
        vad = VAD(aggressiveness=aggressiveness)

print user_utt

