import logging
import logging.handlers
import queue
import threading
import time
import urllib.request
import os
from collections import deque
from pathlib import Path
from typing import List

import whisper

import av
import numpy as np
from pydub import AudioSegment, effects
import streamlit as st
from twilio.rest import Client

from streamlit_webrtc import WebRtcMode, webrtc_streamer

class SpeechToTextWithVideo:
    def __init__(self,playing,record_audio):
        self.frames_deque = deque()
        self.frames_deque_lock = threading.Lock()
        self.model = None  # Load the model only when needed
        self.playing=playing
        self.record_audio=record_audio
        self.silence_counter = 0

    async def queued_audio_frames_callback(self, frames: List[av.AudioFrame]) -> av.AudioFrame:
        with self.frames_deque_lock:
            self.frames_deque.extend(frames)

        # Return empty frames to be silent.
        new_frames = []
        for frame in frames:
            input_array = frame.to_ndarray()
            new_frame = av.AudioFrame.from_ndarray(
                np.zeros(input_array.shape, dtype=input_array.dtype),
                layout=frame.layout.name,
            )
            new_frame.sample_rate = frame.sample_rate
            new_frames.append(new_frame)

        return new_frames

    #here enter the session state variable for transcribed text
    if "transcribed_text" not in st.session_state:
        st.session_state["transcribed_text"] = ""
    

    def app_sst_with_video(self):
        status_indicator = st.empty()
        text_output = st.empty()

        # Load model only when needed
        if self.model is None:
            self.model = whisper.load_model('base.en')

        webrtc_ctx = webrtc_streamer(
            key="speech-to-text-w-video",
            mode=WebRtcMode.SENDRECV,
            queued_audio_frames_callback=self.queued_audio_frames_callback,
            media_stream_constraints={"video": True, "audio": self.record_audio},
            desired_playing_state=self.playing,
            rtc_configuration={"iceServers":[{"urls": ["stun:stun.l.google.com:19302"]}]},
            
        )

        status_indicator.write("Loading...")

        while webrtc_ctx.state.playing:
            sound_chunk = AudioSegment.empty()

            audio_frames = []
            with self.frames_deque_lock:
                while len(self.frames_deque) > 0:
                    frame = self.frames_deque.popleft()
                    audio_frames.append(frame)

            if len(audio_frames) == 0:
                time.sleep(0.1)
                status_indicator.write("No frame arrived.")
                continue

            status_indicator.write("Running. Say something!")

            for audio_frame in audio_frames:
                sound = AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                sound_chunk += sound

            if len(sound_chunk) > 0:
                sound_chunk = sound_chunk.set_channels(1).set_frame_rate(16000)
                buffer = np.array(sound_chunk.get_array_of_samples())
                buffer = buffer / np.max(np.abs(buffer))
                buffer = buffer.astype(np.float32)  # Convert NumPy array to 32-bit floats
                result = self.model.transcribe(buffer,fp16=False)

                text = result['text']
                st.session_state["transcribed_text"] = text  # Update session state

                text_output.markdown(f"**Live Text** {text}")
                self.silence_counter = 0
            else:
                self.silence_counter += 1
                print('Hearing has stopped')
                status_indicator.write("Stopped.")
                if self.silence_counter >= 5:  # Stop streaming after 5 seconds of silence
                    print('5 seconds of silence detected. Stopping stream.')
                    status_indicator.write("Stopped due to silence.")
                    self.playing=False
                    break

        transcribed_text = st.session_state["transcribed_text"]  # Retrieve final text
        st.session_state["transcribed_text"] = ""  # Clear session
        return transcribed_text
        
        