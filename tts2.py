import streamlit as st
import base64
from gtts import gTTS

class TTS2:
    def __init__(self,text):
        self.text=text

    def autoplay_audio(self,file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <div class="hidden-audio">
                    <audio autoplay="true">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                </div>
            """
            st.markdown(md, unsafe_allow_html=True)
            

        # Link the CSS file
            
#autoplay_audio("local_audio.mp3")
# if text:
    def play_text(self):
        speech=gTTS(text=self.text, lang="en",slow=False,tld="co.in")
        speech.save("newtts.mp3")
        audio_file = open('newtts.mp3', 'rb')
        

        return self.autoplay_audio("newtts.mp3")


# st.write("# Auto-playing Audio!")
    
# speech=gTTS(text=text, lang="en",slow=False,tld="co.in")
# speech.save("newtts.mp3")
# audio_file = open('newtts.mp3', 'rb')


# if text:
#     autoplay_audio("newtts.mp3")