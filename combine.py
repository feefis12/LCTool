from pydub import AudioSegment
import moviepy.editor as mpy
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
import glob
import threading
import os
import time
import subprocess
import datetime
from pathlib import Path

def choosesfile():
    root.filename = filedialog.askdirectory(initialdir="C://Users//Felix//Desktop/", title="Select Songs")
    if oneF.get() == 0:
        wavAsker()
    else:
        lambda: Video_thread(None)


def wavAsker():
    global pop
    pop = Toplevel(root)
    pop.geometry("200x100+865+350")
    pop.wm_iconbitmap('lakeaffected.ico')
    pop.title("WAV Convert")
    popLabel = Label(pop, text="Convert to WAV?")
    popButton = Button(pop,text= "Yes", padx=50, command=lambda: convert_thread(None))
    popButton2 = Button(pop,text= "No", padx=50, command=lambda: combine_thread(None))
    popLabel.pack()
    popButton.pack()
    popButton2.pack()
    pop.resizable(False, False)

def combine_thread(event):
    pop.destroy()
    global combine_t
    combine_t = threading.Thread(target=combine)
    combine_t.daemon = True
    progbar.start()
    combine_t.start()

def Video_thread(event):
    global video_t
    video_t = threading.Thread(target=GenVideo)
    video_t.daemon = True
    video_t.start()
    progbar.start()

def convert_thread(event):
    pop.destroy()
    global convert_t
    convert_t = threading.Thread(target=convert_to_wav)
    convert_t.daemon = True
    convert_t.start()
    progbar.start()


def convert_to_wav():
    for file_path in os.listdir(root.filename):
        if file_path.split('.')[-1] != "wav" and file_path.split('.')[-1] != "png":
            read_file = AudioSegment.from_file(os.path.join(root.filename, file_path), file_path.split('.')[-1])
            os.remove(os.path.join(root.filename, file_path))
            base_name = file_path.split('.')[:-1]
            read_file.export(os.path.join(root.filename, f"{base_name[0]}.wav"), format="wav")

    progbar.stop()
    combine_thread(None)


def combine():
    s =[]
    p = []
    title = os.path.basename(root.filename)
    titlebox.insert(END, title)
    os.chdir(root.filename)
    fileName = glob.glob("*wav")
    x=0
    for files in fileName:

        filePath = os.path.abspath(os.path.join(root.filename, files))
        name = Path(fileName[x]).stem
        s.append(filePath)
        p.append(name)
        x+=1

    global songNames
    songNames = s
    songs = [AudioSegment.from_wav(name) for name in s]
    timestamps = ["0:00"]
    for song in songs:
        sec = (len(song) / 1000.0)
        ty_res = time.gmtime(sec)
        res = time.strftime("%M:%S", ty_res)
        timestamps.append(res)
    nextStamp = datetime.timedelta()
    timestampsEND = ["0:00:00"]
    i = 1
    while i < len(timestamps):
        (m, s) = timestamps[i].split(':')
        d = datetime.timedelta(minutes=int(m), seconds=int(s))
        nextStamp += d
        timestampsEND.append(str(nextStamp))
        i+=1

    t = 0
    timestampsEND.pop()

    stamps = open('descriptions.txt', 'w')
    stamps.write(title + "\n" + "\n")

    while t < len(timestampsEND):

        timebox.insert(END, p[t] + " - " + timestampsEND[t][2:7] + "\n")
        stamps.write(p[t] + " - " + timestampsEND[t][2:7] + "\n")
        t+=1

    timebox.insert(END, "\n" + "\n" + "Released:" + "\n")
    stamps.write("\n" + "\n" + "Released:" + "\n")
    timebox.insert(END, "////////Find the Artist////////////" + "\n" + "bandcamp:" + "\n" + "soundcloud:" + "\n")
    stamps.write("////////Find the Artist////////////" + "\n" + "bandcamp:" + "\n" + "soundcloud:" + "\n")
    stamps.close()
    progbar.stop()


def GenVideo():

    songs = [AudioSegment.from_wav(name) for name in songNames]
    combined = AudioSegment.empty()
    for sg in songs:
        combined += sg
    combined.export("album.wav", format="wav")
    pngfile = glob.glob("*png")
    myclip = mpy.ImageClip(pngfile[0])
    albums = mpy.AudioFileClip("album.wav")
    dur = albums.duration
    new_audioclip = mpy.CompositeAudioClip([albums])
    myclip.audio = new_audioclip
    myclip.duration = dur
    # final = myclip.set_duration(dur)
    # myclip = mpy.VideoClip()
    myclip = mpy.vfx.fadein(myclip,1,None)

    return myclip.write_videofile("album.mp4", fps=24)




def copyB():
    root.clipboard_clear()
    root.clipboard_append(timebox.get("1.0", END))

songNames = []

root = Tk()
root.title('Video Tool')
root.filename = str
root.geometry("300x250+800+300")
oneF = IntVar()
fileButton = Button(root, text='Choose Songs', padx=50, command=choosesfile)
# getAlbum = Button(root, text='Show Description', padx=50, command=lambda: combine_thread(None))
getVideo = Button(root, text='Get Video', padx=50, command=lambda: Video_thread(None))
# convertFiles = Button(root,text="Covert to WAV", command=convert_to_wav)
copyButton = Button(root,text="Copy All", padx=50, command=copyB)
oneFile = Checkbutton(root,text="Single File", variable=oneF,padx=0)
titlebox = Text(root, width=30, height=1, padx=10)
titlebox.configure(bg="grey")
timebox = Text(root, width=50, height=7)
progbar = Progressbar(root,mode='determinate',length=200)
progbar.pack()

root.wm_iconbitmap('lakeaffected.ico')
titlebox.pack()
timebox.pack()
fileButton.pack()

# convertFiles.pack()
# getAlbum.pack()
getVideo.pack()
copyButton.pack()
oneFile.pack(side=RIGHT)
# copyButton.pack()
root.resizable(False, False)

root.mainloop()