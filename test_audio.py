from transformers import pipeline

try:
    pipe = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
    response = pipe("temp.wav")
    # print(response)
    # lst = []
    # for i in range(0,len(response)):
    #     lst.append(response[i]["score"])
    # # print(lst)
    # for j in range(0,len(response)):
    #     if response[j]["score"] == max(lst) :
    #         print("Emotion : ",response[j]["label"])
    #         print("Emotion Score : ",response[j]["score"])
    print("Emotion : ",response[0]["label"])
    print("Emotion Score : ",response[0]["score"])

except Exception as e:
    print("error:",e)
