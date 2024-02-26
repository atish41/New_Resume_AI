import base64
import streamlit as st
from gtts import gTTS
language='en'
text= '''Welcome to an AI assisted interview. 
Our AI would narrate the question and then let you answer it, 
after 5 seconds of silence the AI would move on to the next question.'''
# def autoplay_audio(file_path: str):
#     with open(file_path, "rb") as f:
#         data = f.read()
#         b64 = base64.b64encode(data).decode()
#         md = f"""
#             <audio controls autoplay="true">
#             <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#             </audio>
#             """
#         st.markdown(
#             md,
#             unsafe_allow_html=True,
#         )
class TTS:
    def __init__(self,text):
        self.text=text

    def autoplay_audio(self,file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            audio_base64 = base64.b64encode(data).decode('utf-8')
            audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
            st.markdown(audio_tag, unsafe_allow_html=True)


#autoplay_audio("local_audio.mp3")
# if text:
    def play_text(self):
        speech=gTTS(text=self.text, lang=language,slow=False,tld="co.in")
        speech.save("tts.mp3")
        audio_file = open('tts.mp3', 'rb')
        

        return self.autoplay_audio("tts.mp3")