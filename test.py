from tkinter import *     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import cv2
import os
import numpy as np
import pickle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"images")
y_labels = []
x_train = []

def register(reg,name,dob,classID,stuID):
    faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')

    Tk().withdraw()
    filename = askopenfilename()

    img = cv2.imread(filename)
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    size_need = (width, height)
    img = cv2.resize(img,size_need)
    
    while (True):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,scaleFactor = 1.05,minNeighbors=5,minSize=(30,30))
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+h]
            roi_color = img[y:y+h, x:x+h]
            cv2.rectangle(img,(x,y),(x + w,y + h), (124,252,0),2)

        cv2.imshow('',img)
        keyCode = cv2.waitKey(1)
        if cv2.getWindowProperty('',cv2.WND_PROP_VISIBLE) <1:
            break

    defaultDir = "images_check/" + stuID
    if os.path.isdir(defaultDir):
        messagebox.showwarning("Warning","Student ID exists")
        return
    else: 
        saved_dir = "images_check/" + stuID
        os.mkdir(saved_dir)
    
    info = [name,dob,classID,stuID]
    with open(saved_dir+"/%s.txt" %stuID, "w") as f:
        f.writelines('\n'.join(info))

    cv2.imwrite(saved_dir+"/%s.png"%stuID,roi_gray)
    cv2.destroyAllWindows()
    return

def RegisterSucces(reg,saving_img,name,dob,classID,stuID):
    if name and dob and classID and stuID:
        messagebox.showinfo("Library Register","Register Successfull")
        
        reg.destroy()
    else: messagebox.showwarning("Warning","Please fulfil your information")
        

def RegisterTk():
    reg = Tk()
    name = StringVar()
    dob = StringVar()
    classID = StringVar()
    stuID = StringVar()
    reg.geometry('600x400')
    reg.title("Register Library Card")

    intro = Label(reg,text="Please provide us your information",font=("Arial",15,"bold"))
    intro.grid(row=0,column=1)

    Name = Label(reg,text="Your name: ",font=("Arial",14))
    Name.grid(row=1,column=0,padx=5,pady=10)
    inputName = Entry(reg,textvariable=name,font=("Arial",14))
    inputName.grid(row=1,column=1)

    DoB = Label(reg,text="Date of Birth: ",font=("Arial",14))
    DoB.grid(row=2,column=0,padx=5,pady=10)
    inputDoB = Entry(reg,textvariable=dob,font=("Arial",14)) 
    inputDoB.grid(row=2,column=1)

    ClassID = Label(reg,text="Class ID: ",font=("Arial",14))
    ClassID.grid(row=3,column=0,padx=5,pady=10)
    inputClassID = Entry(reg,textvariable=classID,font=("Arial",14)) 
    inputClassID.grid(row=3,column=1)

    StuID = Label(reg,text="Student ID: ",font=("Arial",14))
    StuID.grid(row=4,column=0,padx=5,pady=10)
    inputStuID = Entry(reg,textvariable=stuID,font=("Arial",14)) 
    inputStuID.grid(row=4,column=1)

    saving_img = ""
    capPic = Button(reg,text='Take Picture',font=('Arial',14),command=lambda:register(reg,inputName.get(),inputDoB.get(),inputClassID.get(),inputStuID.get()))
    capPic.grid(row=5,column=1,padx=5,pady=10)
    
    submit = Button(reg,text='Submit',font=('Arial',14),command=lambda:RegisterSucces(reg,saving_img,inputName.get(),inputDoB.get(),inputClassID.get(),inputStuID.get()))
    submit.grid(row=5,column=2)

    reg.mainloop()

def Login():
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
    check = False
    identifier = cv2.face_LBPHFaceRecognizer.create()
    identifier.read("faces_training.yml")
    assign_labels = {"id":1}
    with open("labels.pickle","rb") as f:
        labels_pickle = pickle.load(f)
        assign_labels = {v:k for k,v in labels_pickle.items()}
    cap = cv2.VideoCapture(0)
    while(True):
        ret,cam_check = cap.read()
        gray = cv2.cvtColor(cam_check,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor = 2,minNeighbors=5,minSize=(50,50))
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+h]
            roi_color = cam_check[y:y+h, x:x+h]
            
            id_,dist = identifier.predict(roi_gray)
            if dist >= 45 and dist <= 85:
                
                check = True
                print(assign_labels[id_])

            cv2.rectangle(cam_check,(x,y),(x + w,y + h), (124,252,0),2)
        cv2.imshow('Cam',cam_check)
        if cv2.waitKey(20) & 0xFF == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()
    if check:
        tk.destroy()
        log = Tk()
        log.title("Library")
        intro = Label(log,text="Welcome to the library",font=("Arial",15,"bold"))
        log.geometry('250x100')
        intro.pack()
        log.mainloop()

tk = Tk()
tk.title("Library Check In")
tk.geometry('300x200')
intro = Label(tk,text="Welcome to the library",font=("Arial",15,"bold"))
intro.grid(row=0,column=1,padx=5,pady=10)

btnRegister = Button(tk, text="Register",font=("Arial",15,"bold"),command=RegisterTk)
btnRegister.grid(row=1,column=1,padx=5,pady=10)

btnLogin = Button(tk, text="Login",font=("Arial",15,"bold"),command=Login)
btnLogin.grid(row=2,column=1,padx=5,pady=10)


tk.mainloop()

