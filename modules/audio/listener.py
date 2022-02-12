# noinspection PyUnresolvedReferences
"""Module for speech recognition listener.

>>> Listener

"""

import sys
from threading import Thread

from playsound import playsound
from speech_recognition import (Microphone, Recognizer, RequestError,
                                UnknownValueError, WaitTimeoutError)

recognizer = Recognizer()  # initiates recognizer that uses google's translation
microphone = Microphone()  # initiates microphone as a source for audio


def listen(timeout: int, phrase_limit: int, sound: bool = True) -> str:
    """Function to activate listener, this function will be called by most upcoming functions to listen to user input.

    Args:
        timeout: Time in seconds for the overall listener to be active.
        phrase_limit: Time in seconds for the listener to actively listen to a sound.
        sound: Flag whether to play the listener indicator sound. Defaults to True unless set to False.

    Returns:
        str:
         - On success, returns recognized statement from the microphone.
         - On failure, returns ``SR_ERROR`` as a string which is conditioned to respond appropriately.
    """
    with microphone as source:
        ambient_noise_suppressor = Thread(target=recognizer.adjust_for_ambient_noise, args=[source])
        ambient_noise_suppressor.start()
        try:
            sys.stdout.write("\rListener activated..")

            if sound:
                playsound('indicators/start.mp3', block=False)

            listened = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

            if sound:
                playsound('indicators/end.mp3', block=False)

            return_val = recognizer.recognize_google(listened)
            sys.stdout.write(f'\r{return_val}')

            ambient_noise_suppressor.join(timeout=.5)
        except (UnknownValueError, RequestError, WaitTimeoutError):
            return_val = 'SR_ERROR'

    return return_val