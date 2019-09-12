# Microphone Speech To Text
# You need to install pyaudio to run this example
# pip install pyaudio

# When using a microphone, the AudioSource `input` parameter would be
# initialised as a queue. The pyaudio stream would be continuosly adding
# recordings to the queue, and the websocket client would be sending the
# recordings to the speech to text service

from __future__ import print_function
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from Queue import Queue, Full  # if this doesn't work, try "from queue import Queue, Full"
from naoqi import ALProxy
import STTS
import NaoRobot
import time

###############################################
#### Initalize queue to store the recordings ##
###############################################
CHUNK = 1024
# Note: It will discard if the websocket client can't consumme fast enough
# So, increase the max size as per your choice
BUF_MAX_SIZE = CHUNK * 10
# Buffer to store audio
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

# Create an instance of AudioSource
audio_source = AudioSource(q, True, True)

###############################################
#### Prepare Speech to Text Service ########
###############################################

# initialize speech to text service
speech_to_text = SpeechToTextV1(
    iam_apikey='IOccrNutMkQ80aoLNy2kePYfyPAmKoZDj_B9Wa1pI-CJ',
    url='https://gateway-lon.watsonplatform.net/speech-to-text/api')


# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.motionProxy, self.postureProxy, self.trackerProxy = vrep_connect(57449)
        # Create the Robot
        self.Neo = NaoRobot.NaoRobot(self.motionProxy, self.postureProxy)
        self.standing = False
        self.pointing = False

    def on_transcription(self, transcript):
        heard = transcript[0]['transcript'].encode('ascii', 'ignore')
        if "hello" in heard or "hey" in heard or "hi" in heard:
            # Stand up
            posture = 'Stand'
            self.Neo.stand(posture)
            self.standing = True
            STTS.speak("Hello my name is - Neo. Can I help you?")

        elif "comics" in heard:
            if not self.pointing:
                talk = Thread(target=STTS.speak("Comics, what a great choice. You'll find them in that section in the first shelf."), args=())
                talk.start()
                self.Neo.point(self.trackerProxy, -1.9750, 4.9000, 0.8550, 50, pointframe="Robot")
                self.pointing = True
            STTS.speak("Is there anything else I can help you with?")

        elif "romance" in heard:
            if not self.pointing:
                talk = Thread(target=STTS.speak("Romance, ooohhhh. Our best romance books are in that section over there in the second shelf."), args=())
                talk.start()
                self.Neo.point(self.trackerProxy, -1.9750, 4.9000, 0.8550, 50, pointframe="Robot")
                self.pointing = True
            STTS.speak("Is there anything else I can help you with?")

        elif "fiction" in heard:
            if not self.pointing:
                talk = Thread(target=STTS.speak("Fiction! That's always an interesting read. The latest fiction books are in that corner in the "
                       "third shelf"), args=())
                talk.start()
                self.Neo.point(self.trackerProxy, -1.9750, 4.9000, 0.8550, 50, pointframe="Robot")
                self.pointing = True
            STTS.speak("Is there anything else I can help you with?")

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        pass

    def on_data(self, data):
        pass

    def on_close(self):
        STTS.speak("Connection closed")


# this function will initiate the recognize service and pass in the AudioSource
def recognize_using_weboscket(*args):
    mycallback = MyRecognizeCallback()
    speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             interim_results=True)


###############################################
### Prepare the for recording using Pyaudio ###
###############################################

# Variables for recording the speech
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


# define callback for pyaudio to store the recording in queue
def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass  # discard
    return (None, pyaudio.paContinue)


# instantiate pyaudio
audio = pyaudio.PyAudio()

# open stream using callback
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=pyaudio_callback,
    start=False
)


def start_listening():
    #########################################################################
    #### Start the recording and start service to recognize the stream ######
    #########################################################################

    print("Enter CTRL+C to end recording...")
    stream.start_stream()

    try:
        recognize_thread = Thread(target=recognize_using_weboscket, args=())
        recognize_thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        # stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_source.completed_recording()


def vrep_connect(naoPort):
    print("================ Choregraphe's Initialization ================")
    naoIP = '127.0.0.1'
    # Go to Choregraphe, click on edit->Preferences->Virtual bot tab.
    # Your bot's port is at the bottom of the window in green text.
    # The port number changes for a new virtual bot connection.
    return ALProxy("ALMotion", naoIP, naoPort), ALProxy("ALRobotPosture", naoIP, naoPort), ALProxy("ALTracker", naoIP, naoPort)


if __name__ == "__main__":
    start_listening()
