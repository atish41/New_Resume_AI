from sentence_transformers import SentenceTransformer, util
import streamlit as st
import tensorflow as tf
import numpy as np
from transformers import pipeline
import hydralit_components as hc

st.markdown("<style>.my-title{font-family:'serif';}</style>",unsafe_allow_html=True,)
st.markdown(f'<h1 class="my-title">Interview Report</h1>',unsafe_allow_html=True)


Ques=st.session_state['question']
ideal_ans=st.session_state['ideal_ans']
answer=st.session_state['answer_text']
wpm=st.session_state['wpm']
Pace =round(wpm,2)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
ideal_ans_embed=model.encode(ideal_ans)
candidate_ans_embed=model.encode(answer)
cos_sim = util.cos_sim(ideal_ans_embed, candidate_ans_embed)
x=tf.cast(cos_sim[0][0]*100, tf.float64)
score_value=np.round(x.numpy(),2)
#st.write("Score of Candidate's answer ",score_value)

st.write("**Question Asked:**",Ques)
st.divider()
st.write("**Ideal Ans:**",ideal_ans)
st.divider()
st.write("**Candidate's Answer:**",answer)
st.divider()
#st.write("Pace (wpm)",round(wpm,2))


#can apply customisation to almost all the properties of the card, including the progress bar
theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}

cc = st.columns(3)

with cc[0]:
    if score_value>50:
        sentiment='good'
    else:
       sentiment='bad'

 # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
    hc.info_card(title='Answer Score', content=f'{score_value}%', sentiment=sentiment,bar_value=score_value)

with cc[1]:
    if 120<Pace<=150:
        comment="Perfect Pace"
        sentiment='good'
    elif Pace<=120:
        comment='Too slow'
        sentiment='bad'
    else:
        comment='Too fast'
        sentiment='bad'

    hc.info_card(title='Speaking Pace', content=f'{Pace} wpm {comment}',bar_value=Pace,sentiment=sentiment)

# with cc[2]:
#  hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral',bar_value=55)

# with cc[3]:
#  #customise the the theming for a neutral content
#  hc.info_card(title='Some NEURAL',content='Maybe...',key='sec',bar_value=5,theme_override=theme_neutral)
    


# Emotion Recognition
st.markdown("<style>.my-title{font-family:'serif'}</style>",unsafe_allow_html=True,)
st.markdown('<h3 class="my-title">Emotion Recognition</h3>',unsafe_allow_html=True)

if st.button("Recognize Emotion"):
    try:
        pipe = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
        response = pipe("temp.wav")

        st.write("Emotion:", response[0]["label"])
        st.write("Emotion Score:",f"{(round(response[0]['score'],4)*100)} %")

    except Exception as e:
        st.error(f"An error occurred: {e}")





option_data = [
   {'icon': "bi bi-hand-thumbs-up", 'label':"Yes"},
   {'icon': "bi bi-arrow-down-square", 'label':"Downvote"},
   {'icon':"bi bi-arrow-up-square",'label':"Upvote"},
   
]

# override the theme, else it will use the Streamlit applied theme
over_theme = {'txc_inactive': 'white','menu_background':'#FEE1C7','txc_active':'#F44174','option_active':'#B5A886'}
font_fmt = {'font-class':'h2','font-size':'150%'}

op2 = hc.option_bar(option_definition=option_data,title='Is the Scoring Apt?',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)