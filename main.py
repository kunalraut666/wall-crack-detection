from tkinter import font
import numpy as np
import cv2
import crackconcrete as cr
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image,ImageTk
import winsound as ws

def crackDetect(pic):
    graywall = cv2.imread(pic)

    global wallrgb
    wallrgb = cv2.cvtColor(graywall,cv2.COLOR_BGR2RGB)
    copyrgb = np.copy(wallrgb)

    pr = cr.image_preprocessor(graywall)
    lb = cr.label_preprocessor(graywall)

    res = cv2.subtract(pr,lb)
    rescopy = np.copy(res)

    dil = cv2.dilate(rescopy,np.ones((3,3)),iterations=3)
    erodil = cv2.erode(dil,np.ones((3,3)),iterations=3)

    cnt,hr = cv2.findContours(erodil,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnt)):
        cv2.drawContours(wallrgb,cnt,i,thickness=5,color=(255,0,0))

            
    ca = 0
    cp = 0
    for p in range(len(cnt)):
        perimeter = cv2.arcLength(cnt[p],False)
        cp = cp+round(perimeter,0)
        area = cv2.contourArea(cnt[p])
        ca = ca+round(area,0)

    f = ('Times New Roman',16) 
    global labelD
    labelD = tk.Label(win,bg='#101820',fg='#F2AA4C',text=f"Results: \nThe red color area shows the detected crack.\nCrack Parimeter :{cp} \nCrack Area :{ca}",font=f)
    labelD.place(x=590,y=550)

    im = Image.fromarray(wallrgb)
    imcpy = im
    imcpy.thumbnail((500,500))
    imcpy = ImageTk.PhotoImage(imcpy)
    label1.configure(image=imcpy)
    label1.image = imcpy
    
def browseImage():
    global imgFile
    imgFile = filedialog.askopenfilename(initialdir='E:\Concrete\Crack Images', title='Select Image',filetypes=(('PNG File','*.png'),('JPG File','*.jpg'),('All Files','*')))
    img = Image.open(imgFile)
    imgcpy = img
    imgcpy.thumbnail((500,500))
    imgcpy = ImageTk.PhotoImage(imgcpy)
    label0.configure(image=imgcpy)
    label0.image = imgcpy

def detect():
    if len(label0['image'])>0:
        crackDetect(imgFile)
    else:
        ws.PlaySound("SystemExit", ws.SND_ALIAS)
        label0['text'] = 'No image selected'

def saveImage():
    if len(label1['image'])>0:
        filename = filedialog.asksaveasfile(mode='w', initialdir='E:\\', title='Save Image',defaultextension=".jpg")
        saveFile = Image.fromarray(wallrgb)
        saveFile.save(filename)
    else:
        ws.PlaySound("SystemExit", ws.SND_ALIAS)
        label1['text'] = 'No image detected'    

def onEnterBtn0(e):
    btn0.config(background='blue4', foreground= "snow")
def onLeaveBtn0(e):
    btn0.config(background= 'SystemButtonFace', foreground= 'black')

def onEnterBtn1(e):
    btn1.config(background='blue4', foreground= "snow")
def onLeaveBtn1(e):
    btn1.config(background= 'SystemButtonFace', foreground= 'black')

def onEnterBtn2(e):
    btn2.config(background='blue4', foreground= "snow")
def onLeaveBtn2(e):
    btn2.config(background= 'SystemButtonFace', foreground= 'black')

def onEnterResetBtn(e):
    resetBtn.config(background='blue4')
def onLeaveResetBtn(e):
    resetBtn.config(background= 'SystemButtonFace')
    
def resetAll():
    label0['image'] = ''
    label1['image'] = ''
    labelD['text'] = ''
    label0['text'] = 'Your selected Image will be shown here'
    label1['text'] = 'Your result will be shown here'
    

win = tk.Tk()
win.geometry('1920x1080')
win.title('Wall Crack Detector')
win.iconbitmap('Crackicon.ico')

wallpaper = tk.PhotoImage(file='wallpaper1.png')
backLabel = tk.Label(win, image=wallpaper)
backLabel.place(x=0,y=0)

fH = ('Harlow Solid Italic',50,'bold')
label = tk.Label(win,fg='#EC4D37',bg='#1D1B1B',text='Wall Crack Detector',font=fH)
label.pack()

f = ('Lucida Calligraphy',15)
label0 = tk.Label(win,fg='#EE4E34',bg='#FCEDDA',text='Your selected Image will be shown here',font=f)
label0.pack(side=tk.LEFT,padx=50)

label1 = tk.Label(win,fg='#EE4E34',bg='#FCEDDA',text='Your result will be shown here',font=f)
label1.pack(side=tk.RIGHT,padx=50)

fbtn = ('Script Mt Bold',20)

browseIcon = tk.PhotoImage(file='browse.png')
browseIcon = browseIcon.subsample(10,10)
btn0 = tk.Button(win,bd=0,font=fbtn,text=' Browse Image ',cursor="hand2",command=browseImage,image=browseIcon,compound=tk.LEFT)
btn0.place(x=185,y=740)
btn0.bind('<Enter>', onEnterBtn0)
btn0.bind('<Leave>', onLeaveBtn0)

saveIcon = tk.PhotoImage(file='save.png')
saveIcon = saveIcon.subsample(10,10)
btn2 = tk.Button(win,bd=0,font=fbtn,text=' Save Image ',cursor="hand2",command=saveImage,image=saveIcon,compound=tk.RIGHT)
btn2.place(x=1170,y=740)
btn2.bind('<Enter>', onEnterBtn2)
btn2.bind('<Leave>', onLeaveBtn2)

rightIcon = tk.PhotoImage(file='right.png')
rightIcon = rightIcon.subsample(11,11)
btn1 = tk.Button(win,bd=0,font=fbtn,text=' Detect Crack ',cursor="hand2",command=detect,image=rightIcon,compound=tk.RIGHT)
btn1.place(x=690,y=400)
btn1.bind('<Enter>', onEnterBtn1)
btn1.bind('<Leave>', onLeaveBtn1)

resetIcon = tk.PhotoImage(file='reset.png')
resetIcon = resetIcon.subsample(5,5)
resetBtn = tk.Button(win,bd=0,font=fbtn,image=resetIcon,cursor="hand2",command=resetAll)
resetBtn.place(x=740,y=740)
resetBtn.bind('<Enter>', onEnterResetBtn)
resetBtn.bind('<Leave>', onLeaveResetBtn)


win.mainloop()