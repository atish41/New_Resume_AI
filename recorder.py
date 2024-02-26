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

import av
import numpy as np
from pydub import AudioSegment, effects
import streamlit as st
from twilio.rest import Client

from streamlit_webrtc import WebRtcMode, webrtc_streamer

class recorderwithvideo:
    def __init__(self,playing):
        self.playing=playing
        self.frames_deque = deque()
        self.frames_deque_lock = threading.Lock()

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

    def record_with_video(self):
        if "audio_buffer" not in st.session_state:
            st.session_state["audio_buffer"] = AudioSegment.empty()

        

        webrtc_ctx = webrtc_streamer(
            key="speech-to-text-w-video",
            desired_playing_state=self.playing,
            mode=WebRtcMode.SENDRECV,
            queued_audio_frames_callback=self.queued_audio_frames_callback,
            rtc_configuration={"iceServers":[{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": True}
        )

        status_indicator = st.empty()
        

        status_indicator.write("Loading, click on start toggle button...")

        while webrtc_ctx.state.playing:
            sound_chunk = AudioSegment.empty()

            audio_frames = []
            with self.frames_deque_lock:
                while len(self.frames_deque) > 0:
                    frame = self.frames_deque.popleft()
                    audio_frames.append(frame)

            if len(audio_frames) == 0:
                time.sleep(0.1)
                status_indicator.write("Unable to hear voice.")
                continue

            status_indicator.write("Running. You can answer after the question!")

            for audio_frame in audio_frames:
                sound = AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                sound_chunk += sound

            if len(sound_chunk) > 0:
                st.session_state["audio_buffer"] += sound_chunk
                

            else:
                
                status_indicator.write("Interview Stopped.")
                break

        audio_buffer = st.session_state["audio_buffer"]   

        if not webrtc_ctx.state.playing and len(audio_buffer) > 0:
            st.info("Saving answer")
            audio_buffer.export("temp.wav", format="wav")
            st.session_state["audio_buffer"] = AudioSegment.empty()

    