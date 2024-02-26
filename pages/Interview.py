from recorder import recorderwithvideo
from tts2 import TTS2
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from transcriber import transcriber


if 'answer_text' not in st.session_state:
    st.session_state['answer_text'] = "" 
if 'wpm' not in st.session_state:
    st.session_state['wpm'] =4 


#TO ACTUALLY TURN SPEAKER ON AND OFF , FIRST WE WOULD HAVE TO CHANGE THE DESIRED PLAYING STATE TO OFF
#THEN WE CAN CHANGE THE AUDIO MEDIA 
language='en'



instruction='''This is an AI conducted interview, The AI will narrate a set of questions ,
 which you can answer after the pause. Question 1 '''

question=st.session_state['question']

text_to_speak=instruction+question
play=st.toggle('Start/End Interview',value=False)
speech=TTS2(text_to_speak)
if play:
    speech.play_text()

audio=recorderwithvideo(play)
audio.record_with_video()

transcribed=transcriber("temp.wav")
answer=transcribed.audio_text()
wpm=transcribed.wpm()

st.session_state['answer_text'] = answer
st.session_state['wpm'] =wpm

report=st.button('Generate report')
if report:
    switch_page('Result')

# answers=[]
# for i in range(len(texttospeak)):
#     ques_narration=TTS(texttospeak[i])
#     ques_narration.play_text()
#     play_video=True
#     sttobj= SpeechToTextWithVideo(play_video,record_audio)
#     text=sttobj.app_sst_with_video()
#     #DETECT SILENCE FOR 5 SECONDS AND 
#     play_video=False
#     answers[i]=text

