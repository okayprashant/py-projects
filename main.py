import pygame
from pygame import mixer
from tkinter import *
import os
import time
import threading


song_path_map = {}

# === SONG TIME TRACKER THREAD ===
def update_song_time():
    while True:
        try:
            if mixer.music.get_busy():
                current_time = mixer.music.get_pos() // 1000
                if current_time < 0:
                    current_time = 0
                time_label.config(text=f"Time: {current_time}s")
            else:
                time_label.config(text="Time: 0s")
            time.sleep(1)
        except Exception as e:
            print(f"[Time Update Error] {e}")

# === PLAYER CONTROLS ===
def playsong():
    currentsong = playlist.get(ACTIVE)
    full_path = song_path_map.get(currentsong)

    try:
        mixer.music.load(full_path)
        mixer.music.play()
        songstatus.set(f"Playing: {os.path.basename(full_path)}")
    except Exception as e:
        songstatus.set(f"Error: {e}")

def pausesong():
    songstatus.set("Paused")
    mixer.music.pause()

def stopsong():
    songstatus.set("Stopped")
    mixer.music.stop()

def resumesong():
    songstatus.set("Resuming")
    mixer.music.unpause()

def nextsong():
    idx = playlist.curselection()
    if idx:
        next_idx = (idx[0] + 1) % playlist.size()
        playlist.selection_clear(0, END)
        playlist.activate(next_idx)
        playlist.selection_set(next_idx)
        playsong()

def prevsong():
    idx = playlist.curselection()
    if idx:
        prev_idx = (idx[0] - 1) % playlist.size()
        playlist.selection_clear(0, END)
        playlist.activate(prev_idx)
        playlist.selection_set(prev_idx)
        playsong()

# === GUI SETUP ===
root = Tk()
root.title('Music Player :PK')
root.configure(bg="#222831")

mixer.init()
mixer.music.set_volume(0.5)
songstatus = StringVar()
songstatus.set("Choosing...")

muted = False
prev_volume = 0.5

playlist = Listbox(root, selectmode=SINGLE, bg="#393E46", fg="white", font=('arial', 13), width=48)
playlist.grid(row=0, column=0, columnspan=6, pady=10)

os.chdir(r'E:\RAHUL\Musics') 
songs = [s for s in os.listdir() if s.endswith(('.mp3', '.wav'))]
for s in songs:
    full_path = os.path.abspath(s)
    song_path_map[s] = full_path
    playlist.insert(END, s)  


# === Buttons Row ===
Button(root, text="Previous", command=prevsong, font=('arial', 12), bg="#00ADB5", fg="white").grid(row=1, column=4, padx=5)
Button(root, text="Play", command=playsong, font=('arial', 12), bg="#00ADB5", fg="white").grid(row=1, column=0, padx=5)
Button(root, text="Pause", command=pausesong, font=('arial', 12), bg="#00ADB5", fg="white").grid(row=1, column=1, padx=5)
Button(root, text="Resume", command=resumesong, font=('arial', 12), bg="#00ADB5", fg="white").grid(row=1, column=3, padx=5)
Button(root, text="Next", command=nextsong, font=('arial', 12), bg="#00ADB5", fg="white").grid(row=1, column=5, padx=5)

time_label = Label(root, text="Time: 0s", font=('arial', 11), bg="#222831", fg="white")
time_label.grid(row=3, column=4, columnspan=2)


threading.Thread(target=update_song_time, daemon=True).start()

root.mainloop()
