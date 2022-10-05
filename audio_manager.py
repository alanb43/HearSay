from time import sleep
import speech_recognition as sr

class AudioManager:
    """Turns utterances into text and text into speech."""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def mic_to_text(self):
        """Turns spoken utterances from device's main mic into text."""
        audio_data = self._get_microphone_input()
        response = self._recognize_audio_content(audio_data)
        # still need to build digestible representation of audio content
        # from response data

    def text_to_audio(self):
        """Reads text as auditory output."""

    def _get_microphone_input(self):
        """
        Gathers device's main microphone input, until silence is detected. 
        Has a 0.5s ambient noise adjustment period upon invocation.
        """
        with self.microphone as audio_input:
            self.recognizer.adjust_for_ambient_noise(audio_input)
            sleep(0.5)
            print("begin talking!")
            audio_data = self.recognizer.listen(audio_input)
            return audio_data

    def _recognize_audio_content(self, audio):
        """
        Transcribes audio input data to find content of utterance.

        :input "audio": an sr.AudioFile, made from micrphone input
        
        :returns "dict": response object for audio content.
            attributes:
                - "success": bool, whether content was transcribed
                - "error": str, an error message populated when error occurs
                - "transcription": 
        """
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            # Change to google cloud speech, need to create account to do so.
            response["transcription"] = self.recognizer.recognize_google(audio)

        except sr.UnknownValueError:
            # The audio input wasn't parsable by the recognizable. Jibberish.
            response["success"] = False
            response["error"] = "I wasn't able to understand that, please try again."

        except sr.RequestError:
            # Google Cloud Speech API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"

        except Exception:
            # Unknown exception occurred
            response["success"] = False
            response["error"] = "Unknown exception occurred"

        return response

