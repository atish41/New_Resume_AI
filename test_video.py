import cv2
import numpy as np
import streamlit as st
from deepface import DeepFace
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class FaceEmotionDetection(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            emotions = DeepFace.analyze(img[y:y + h, x:x + w], actions=["emotion"])
            emotion = max(emotions['emotion'], key=emotions['emotion'].get)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 2)
            cv2.putText(img, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        return img

def main():
    st.title("Face Emotion Detection")
    webrtc_streamer(key="example", video_transformer_factory=FaceEmotionDetection)

if __name__ == "__main__":
    main()