import tkinter as tk
import pyaudio
import wave
from threading import Thread
import speech_recognition as sr
import socket               
from cryptography.fernet import Fernet

def encrypt(text):
    key = Fernet.generate_key()
    print ("Key:",key)
    print()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(text.encode())
    #plain_text = cipher_suite.decrypt(cipher_text)
    print("Cipher Text:",cipher_text)
    return key,cipher_text

AUDIO_FILE = ("file.wav") 
# use the audio file as the audio source 
r = sr.Recognizer()
text_to_send = ""
  


root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

recording_happening = False

def record():
    global recording_happening
    global text_to_send
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2,
                rate=44100, input=True,
                frames_per_buffer=1024)
    
    frames = []
 
    while recording_happening:
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open("file.wav", 'wb')
    waveFile.setnchannels(2)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(44100)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    with sr.AudioFile(AUDIO_FILE) as source: 
    #reads the audio file. Here we use record instead of 
    #listen 
        audio = r.record(source)   
        try:
            converted_text = r.recognize_google(audio)
            #print("The audio file contains: " + r.recognize_google(audio))
            #str = unicode(str, errors='replace')
            print("The audio file contains: " + converted_text)
            text_to_send = converted_text
            
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        except sr.RequestError as e: 
            print("Could not request results from Google Speech  Recognition service; {0}".format(e))   
        
def socket_thread():
    global text_to_send
    s = socket.socket()
    port = 12345
    s.bind(('', port))
    s.listen(5)

    while True:
        c,addr = s.accept()
        key, encrypted_text = encrypt(text_to_send)
        c.send(key+" ".encode()+encrypted_text)
        text_to_send=""
        c.close()

st = Thread(target=socket_thread);
st.start()
        
def startRecording():
    global recording_happening
    recording_happening=True

    t=Thread(target=record)
    t.start()

    print("start recording")


start_button = tk.Button(frame, text="start",command=startRecording)
start_button.pack(side=tk.LEFT)

def stopRecording():
    global recording_happening
    recording_happening=False
    print("stop recording")

stop_buttton = tk.Button(frame,text="stop",command=stopRecording)
stop_buttton.pack(side=tk.RIGHT)

root.mainloop()
