#!/usr/bin/env python
import tkinter as tk
from tkinter import filedialog
import pygame.mixer as mix
import wave
import os
from  wavconverter import to_wav
from generate_music import MusicGenerator
from keras.models import load_model

model_path = "saved_models/153-1.5443.h5"
model = load_model(model_path)
class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.to_wav = to_wav
        self.model = model
        mix.init()
        mix.music.load("MIDI_sample.mid")
        mix.music.play(0)
        mix.music.pause()
        if not os.path.exists("GeneratedMusic"):
            os.makedirs("GeneratedMusic")

    def createWidgets(self):
        self.uploadButton = tk.Button(self, text="Upload", command=self.upload)
        self.uploadButton.grid()
        self.uploadedFile = tk.Label(self, text="")
        self.uploadedFile.grid()
        self.playButton = tk.Button(self, text='Play', command=self.play)
        self.playButton.grid(column="0", row="2")
        self.pauseButton = tk.Button(self, text='Pause', command=self.pause)
        self.pauseButton.grid(column="1", row="2")
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column="1", row="0")

    def play(self):
        mix.music.unpause()

    def pause(self):
        mix.music.pause()

    def rewind(self):
        mix.music.rewind()

    def upload(self):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("abc files","*.abc"),("all files","*.*")))
        self.to_wav(filename)
        CHANNELS = 1
        swidth = 2
        Change_RATE = 2

        self.uploadedFile = tk.Label(self, text=filename.split("/")[-1])
        self.uploadedFile.grid()

        spf = wave.open('out.wav', 'rb')
        RATE=spf.getframerate()
        signal = spf.readframes(-1)

        name = "GeneratedMusic/" + filename.split("/")[-1].split(".")[0] + ".wav"

        wf = wave.open(name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(swidth)
        wf.setframerate(RATE*Change_RATE)
        wf.writeframes(signal)
        wf.close()

        mix.music.load(name)
        mix.music.play()

    #When this function is called it automatically synthesizes some music
    def synthesize(self):



app = Application()
app.master.title('Music Player')
app.mainloop()