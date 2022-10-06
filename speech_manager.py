from dataclasses import dataclass
from time import sleep
import speech_recognition as sr
import pyttsx3

@dataclass
class Response:
    success: bool = True
    error: str = None
    content: str = None

class SpeechManager:
    """Turns utterances into text and text into speech."""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def speech_to_text(self):
        """Turns spoken utterances from device's main mic into text."""
        audio_data = self._get_microphone_input()
        response = self._recognize_audio_content(audio_data)
        print(response)
        return response.content if response.success else response.error

    def text_to_speech(self, text: str):
        """Reads text as auditory output."""
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def _get_microphone_input(self):
        """
        Gathers device's main microphone input, until silence is detected. 
        Has a 0.5s ambient noise adjustment period upon invocation.
        """
        with self.microphone as audio_input:
            self.recognizer.adjust_for_ambient_noise(audio_input)
            sleep(0.5)
            print("Begin talking!")
            audio_data = self.recognizer.listen(source=audio_input)
            return audio_data
    
    def _recognize_audio_content(self, audio):
        """
        Transcribes audio input data to find content of utterance.

        :input "audio": an sr.AudioFile, made from micrphone input
        
        :returns "dict": response object for audio content.
            attributes:
                - "success": bool, whether content was transcribed
                - "error": str, an error message populated when error occurs
                - "transcription": str, the transcribed content from input
        """
        response = Response()
        try:
            # Change to google cloud speech, need to create account to do so.
            response.content = self.recognizer.recognize_google(audio)

        except sr.UnknownValueError:
            # The audio input wasn't parsable by the recognizable. Jibberish.
            response.success = False
            response.error = "I wasn't able to understand that, please try again."

        except sr.RequestError:
            # Google Cloud Speech API was unreachable or unresponsive
            response.success = False
            response.error = "API unavailable, try again later."

        except Exception:
            # Unknown exception occurred
            response.success = False
            response.error = "Unknown error occurred, please try again."

        return response
