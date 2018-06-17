#!/usr/bin/env python
import tkinter as tk
from tkinter import filedialog
import pygame.mixer as mix
import os
from generate_music import MusicGenerator
from keras.models import load_model
from music21 import *

model_path = r"C:\Users\Jason\PyCharmProjects\StuyHacks2018\saved_models\255-1.4700.h5"
model = load_model(model_path)
class Application(tk.Frame):

    def __init__(self, master=None, path_to_train=r"C:\Users\Jason\PyCharmProjects\StuyHacks2018\training_data.txt"):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.path = path_to_train

        def to_stream(fn):
            abc = converter.parse(fn)
            return abc

        self.to_stream = to_stream

        self.synth = MusicGenerator(model)

        mix.init()
        if not os.path.exists("GeneratedMusic"):
            os.makedirs("GeneratedMusic")

    def createWidgets(self):
        self.uploadButton = tk.Button(self, text="Upload", command=self.upload)
        self.uploadButton.grid()

        self.playButton = tk.Button(self, text="Play", command=self.play)
        self.playButton.grid()
        self.songIndex = tk.Entry(self)
        self.songIndex.grid()

        self.synthesizeButton = tk.Button(self, text="Synthesize", command=self.synthesize)
        self.synthesizeButton.grid()

        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column="1", row="0")

    def upload(self):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("abc files","*.abc"),("all files","*.*")))
        stream = self.to_stream(filename)
        self.uploadedFile = tk.Label(self, text=filename.split("/")[-1])
        self.playButton.grid()

        self.uploadedFile.grid()
        sp = midi.realtime.StreamPlayer(stream)
        sp.play()


    def play(self):
        index = int(self.songIndex.get())
        with open(self.path) as f:
            a = f.read()
        k = a.split('\n\n')
        v = k[index]
        z = [''] + v.split() + ['']
        q = self.synth.parse_generated(z)
        data = converter.parseData(q)
        sp = midi.realtime.StreamPlayer(data)
        sp.play()

    #When this function is called it automatically synthesizes some music
    def synthesize(self):
        try:
            abcstr = self.synth.get()
            data = converter.parseData(abcstr)
            sp = midi.realtime.StreamPlayer(data)
            sp.play()
        except:
            print('error thrown')
            self.synthesize()



app = Application()
app.master.title('Music Player')
app.mainloop()
