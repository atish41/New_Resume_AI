import whisper

class transcriber:
    def __init__(self,file_path):
        self.file_path=file_path

    def transcribe(self):
        model = whisper.load_model("tiny.en")
        result = model.transcribe(self.file_path,fp16=False)
        return result
    def audio_length(self,result):
        result=self.transcribe()
        return result['segments'][0]['end']-result['segments'][0]['start']
    def audio_text(self):
        result=self.transcribe()
        return result['text']
    def wpm(self):
        result=self.transcribe()
        words_in_text=result['text'].split()
        word_count=len(words_in_text)
        wpm=(word_count/self.audio_length(result))*60
        return wpm