from tkinter import *
import sys
import os
import cv2
from tkinter import *
from tkinter import filedialog
import PIL.Image
import PIL.ImageTk
import subprocess
import os


def videoCallback():
    root.destroy()
    subprocess.call('python combine.py',shell=True)


global R, B, G, X_pos, Y_pos, CLICKED

def destory_and_pick():
    destroy_pop()
    pickerC()


def AskPop(canvas):
    global pop
    pop = Toplevel(root)
    # pop.title("Options")
    pop.geometry("150x75+865+355")
    pop.wm_iconbitmap('lakeaffected.ico')
    pop.title('Options')
    pop_label = Label(pop,text="Save or Redo?")
    saveB = Button(pop,text="Save", padx=50, command=lambda: Saver(canvas))
    redoB = Button(pop,text="Redo", padx=50, command=destory_and_pick)
    pop_label.pack()
    pop.lift()
    pop.attributes('-topmost', True)
    pop.after_idle(root.attributes, '-topmost', False)
    saveB.pack()
    redoB.pack()
    pop.resizable(False, False)

def showPic(r,g,b,):
    fp = open(root.filename, "rb")
    size = (1920,1080);
    resized =(1080,1080);
    canvas = PIL.Image.new("RGB", size, color=(r,g,b))
    image = PIL.Image.open(fp)
    modifed = image.resize(resized,resample=3,box=None,)
    bg_w, bg_h = canvas.size
    img_w, img_h = modifed.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    canvas.paste(modifed,offset)
    canvas.show()
    AskPop(canvas)


def findFile():
    root.filename = filedialog.askopenfilename(initialdir="C://Users//Felix//Desktop/",
                                               title="Select Cover",
                                               filetypes=(("jpg files", "*.jpg"),("png files" ,"*.png"),))
    pickerC()


def pickerC():

    img = cv2.imread(root.filename)
    img = cv2.resize(img, (500, 500))
    cv2.imshow("image", img)
    cv2.resizeWindow("image", 500, 500)
    cv2.setMouseCallback("image", show_color)



def show_color(event, x, y, flags, param):
    img = cv2.imread(root.filename)
    img = cv2.resize(img, (500, 500))
    if event == cv2.EVENT_LBUTTONDOWN:

        CLICKED = True
        X_pos = x
        Y_pos = y
        B, G, R = img[Y_pos, X_pos]
        R = int(R)
        G = int(G)
        B = int(B)
        showPic(R,G,B)
        print(R, G, B)
        cv2.destroyAllWindows()


def destroy_pop():
    pop.destroy()

def Saver(pic):
    pop.destroy()
    base_name = root.filename.split('.')[:-1]
    pic.save((os.path.join(root.filename, f"{base_name[0]}.png")),"png")
    # os.system("python mainMenu.py")


root = Tk()

root.geometry("250x200+800+300")
root.title("Lake Affected")
root.wm_iconbitmap('lakeaffected.ico')
VideoB = Button(root,text="Video Tool",padx=100,pady=44, command=videoCallback)
BackB = Button(root,text="Cover Tool",padx=100,pady=40, command=findFile)
BackB.pack()
VideoB.pack()
root.resizable(False, False)
root.mainloop()