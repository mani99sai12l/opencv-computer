import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
import time
import os
from PIL import Image, ImageDraw, ImageFont
# Creating object of tk class
root = Tk()

C = Canvas(root, bg="blue")
width, height = 640, 480
root.cap = cv2.VideoCapture(0)

root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root.title("Pycam")
root.geometry("2680x1400")
root.resizable(True, True)

filename = ImageTk.PhotoImage(Image.open("w2.jpeg"))
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


# Defining CreateWidgets() function to create necessary tkinter widgets
def createwidgets():
    #root.feedlabel = Label(root, bg="steelblue", fg="white", text="WEBCAM FEED", font=('Monotype Corsiva',20))
    root.feedlabel = Label(root, bg="DodgerBlue2", fg="white", text="WEBCAM FEED", font=('Monotype Corsiva',20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
    root.cameraLabel = Label(root, bg="gray14", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
    root.saveLocationEntry = Entry(root, width=50, textvariable=destPath)
    root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)
    root.browseButton = Button(root, width=10, text="BROWSE", command=destBrowse,bg='chocolate1')
    root.browseButton.grid(row=3, column=2, padx=10, pady=10)
    root.captureBTN = Button(root, text="capture", command=Capture, bg="aquamarine", font=('Segoe Script',15), width=20)
    root.captureBTN.grid(row=4, column=1, padx=10, pady=10)
    root.CAMBTN = Button(root, text="stop camera", command=StopCAM, bg="aquamarine", font=('Segoe Script',15), width=13)
    root.CAMBTN.grid(row=4, column=3)
    root.previewlabel = Label(root, bg="DodgerBlue2", fg="white", text="IMAGE PREVIEW", font=('Monotype Corsiva',20))
    root.previewlabel.grid(row=1, column=3, padx=10, pady=10, columnspan=2)
    root.imageLabel = Label(root, bg="gray14", borderwidth=2, relief="groove")
    root.imageLabel.grid(row=2, column=3, padx=5, pady=5, columnspan=2)
    root.openImageEntry = Entry(root, width=50, textvariable=imagePath)
    root.openImageEntry.grid(row=3, column=3, padx=10, pady=10)
    root.openImageButton = Button(root, width=10, text="BROWSE", command=imageBrowse,bg='chocolate1')
    root.openImageButton.grid(row=3, column=4, padx=10, pady=10)
    root.drop1 = OptionMenu(root,click, *optionlist, command=selection)
    root.drop1.config(width=8, font=('Segoe Script',15),bg='aquamarine')
    root.drop1.grid(row=4, column=2, padx=5, pady=5)
    root.drop = OptionMenu(root,clicked, *options, command=selected)
    root.drop.config(width=8, font=('Segoe Script',15),bg='aquamarine')
    root.drop.grid(row=1, column=2,padx=5,pady=5)



    # Calling ShowFeed() function
    ShowFeed()
# Defining ShowFeed() function to display webcam feed in the cameraLabel;
def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()
    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)
        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
        # Changing the frame color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)
        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image = videoImg)
        # Configuring the label to display the frame
        root.cameraLabel.configure(image=imgtk)
        # Keeping a reference
        root.cameraLabel.imgtk = imgtk
        # Calling the function after 10 milliseconds
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame
        root.cameraLabel.configure(image='')
def destBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    # Displaying the directory in the directory textbox
    destPath.set(destDirectory)
def imageBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    openDirectory = filedialog.askopenfilename(initialdir=r"C:\Users\manisailakshmi.k\Desktop\project\images")
    # Displaying the directory in the directory textbox
    imagePath.set(openDirectory)
    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    imageView = Image.open(openDirectory)
    # Resizing the image using Image.resize()
    imageResize = imageView.resize((640, 480), Image.ANTIALIAS)
    # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageResize)
    # Configuring the label to display the frame
    root.imageLabel.config(image=imageDisplay)
    # Keeping a reference
    root.imageLabel.photo = imageDisplay
# Defining Capture() to capture and save the image and display the image in the imageLabel
def Capture():
    # Storing the date in the mentioned format in the image_name variable
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    # If the user has selected the destination directory, then get the directory and save it in image_path
    if destPath.get() != '':
        image_path = destPath.get()
    # If the user has not selected any destination directory, then set the image_path to default directory
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")
    # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
    imgName = image_path + '/' + image_name + ".jpg"
    # Capturing the frame
    ret, frame = root.cap.read()
    # Displaying date and time on the frame
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)
    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)
    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image)
    # Configuring the label to display the frame
    root.imageLabel.config(image=saved_image)
    # Keeping a reference
    root.imageLabel.photo = saved_image
    # Displaying messagebox
    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)
# Defining StopCAM() to stop WEBCAM Preview
def StopCAM():
    # Stopping the camera using release() method of cv2.VideoCapture()
    root.cap.release()
    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="START CAMERA", command=StartCAM)
    # Displaying text message in the camera label
    root.cameraLabel.config(text="OFF CAM", font=('Comic Sans MS',70))

options=["Emboss",
        "Filter 2D",
        "Blur image",
        "Bilateral blur image",
        "Red",
        "Sepia",
        "Cartoon",
        "Gray"
]
def selected(event):
    if clicked.get()=='Emboss':
        import cv2
        from matplotlib import pyplot as plt
        import numpy as np

        cap=cv2.VideoCapture(0)

        def apply_emboss(frame):
            kernel = np.array([[0,-1,-1],[1,0,-1],[1,1,0]])
            blur = cv2.filter2D(frame, -1, kernel)
            frame=cv2.cvtColor(blur,cv2.COLOR_BGRA2BGR)
            return frame

        while True:

            (ret,frame) = cap.read()

            gblur=apply_emboss(frame)
            cv2.imshow('Blur',gblur)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera.jpg',gblur)

        cap.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Filter 2D':
        import cv2
        from matplotlib import pyplot as plt
        import numpy as np

        cap=cv2.VideoCapture(0)

        def apply_fil(frame):
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            blur = cv2.filter2D(frame, -1, kernel)
            frame=cv2.cvtColor(blur,cv2.COLOR_BGRA2BGR)
            return frame

        while True:

            (ret,frame) = cap.read()

            filter1=apply_fil(frame)
            cv2.imshow('Filter2D Frame',filter1)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera2.jpg',filter1)

        cap.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Blur image':
        import cv2
        from matplotlib import pyplot as plt
        import numpy as np

        cap=cv2.VideoCapture(0)

        def apply_guassian_blur(frame):
            blur = cv2.GaussianBlur(frame, (35, 35), 0)
            frame=cv2.cvtColor(blur,cv2.COLOR_BGRA2BGR)
            return frame

        while True:

            (ret,frame) = cap.read()

            gblur=apply_guassian_blur(frame)
            cv2.imshow('Blur',gblur)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera3.jpg',gblur)

        cap.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Bilateral blur image':
        import cv2

        cap=cv2.VideoCapture(0)

        def apply_bil(frame):
            blur = cv2.bilateralFilter(frame,9,75,75)
            frame=cv2.cvtColor(blur,cv2.COLOR_BGRA2BGR)
            return frame

        while True:

            (ret,frame) = cap.read()

            bilat=apply_bil(frame)
            cv2.imshow('Bilateral Frame',bilat)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera4.jpg',bilat)

        cap.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Red':
        import cv2
        import glob
        import math
        import numpy as np

        capture = cv2.VideoCapture(0)

        def verify_alpha_channel(frame):
            try:
                frame.shape[3]
            except IndexError:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            return frame

        def apply_color_overlay(frame,intensity=0.2,blue=0,green=0,red=0):
            frame=verify_alpha_channel(frame)
            frame_h,frame_w,frame_c=frame.shape
            color_bgra=(blue,green,red,1)
            overlay=np.full((frame_h, frame_w, 4),color_bgra,dtype='uint8')
            cv2.addWeighted(overlay,intensity,frame,1.0,0,frame)
            frame=cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
            return frame

        while (True):

            (ret, frame) = capture.read()

            reddish_color=apply_color_overlay(frame.copy(), intensity=0.5,red=230,blue=220,green=200)
            cv2.imshow('reddish_color',reddish_color)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera5.jpg',reddish_color)

        capture.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Sepia':
        import cv2
        import glob
        import math
        import numpy as np

        capture = cv2.VideoCapture(0)

        def verify_alpha_channel(frame):
            try:
                frame.shape[3]
            except IndexError:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            return frame

        def apply_color_overlay(frame,intensity=0.2,blue=0,green=0,red=0):
            frame=verify_alpha_channel(frame)
            frame_h,frame_w,frame_c=frame.shape
            color_bgra=(blue,green,red,1)
            overlay=np.full((frame_h, frame_w, 4),color_bgra,dtype='uint8')
            cv2.addWeighted(overlay,intensity,frame,1.0,0,frame)
            frame=cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
            return frame

        def apply_sepia(frame,intensity=0.5):
            blue=20
            green=66
            red=112
            frame = apply_color_overlay(frame,intensity=intensity,blue=blue,green=green,red=red)
            return frame

        while (True):

            (ret, frame) = capture.read()

            sepia = apply_sepia(frame.copy())
            cv2.imshow('sepia',sepia)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera6.jpg',sepia)

        capture.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Cartoon':
        import cv2

        video=cv2.VideoCapture(0)

        while True:
            ret,img=video.read()

            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            gray=cv2.medianBlur(gray,5)

            edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)

            color=cv2.bilateralFilter(img,9,300,300)

            cartoon=cv2.bitwise_and(color,color,mask=edges)

            cv2.imshow("Cartoon",cartoon)

            k = cv2.waitKey(1)
            if k==ord('q'):
                break

            cv2.imwrite('camera7.jpg',cartoon)

        video.release()
        cv2.destroyAllWindows()
    elif clicked.get()=='Gray':
        import cv2

        capture = cv2.VideoCapture(0)

        while (True):

            (ret, frame) = capture.read()

            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Gray', grayFrame)

            if cv2.waitKey(1) == 27:
                break

            cv2.imwrite('camera8.jpg',grayFrame)

        capture.release()
        cv2.destroyAllWindows()

    else:
        myLabel=Label(root,text="hii").pack()


clicked=tk.StringVar(root)
clicked.set("Filters")


optionlist=["Selfi by detect smile",
        "Video",
        "Set timer",
        "water mark"
]

def selection(event):
    if click.get()=='Video':
        filename = '60fpsvideo.mp4'

        frames_per_second = 60.0

        my_res = '480p'

        def change_res(cap, width, height):
                cap.set(3, width)
                cap.set(4, height)
        STD_DIMENSIONS = {

        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
        }

        def get_dims(cap, res='1080p'):

                width, height = STD_DIMENSIONS["480p"]
                if res in STD_DIMENSIONS:
                    width,height = STD_DIMENSIONS[res]
                change_res(cap, width, height)
                return width, height
        VIDEO_TYPE = {

        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        def get_video_type(filename):

                filename, ext = os.path.splitext(filename)
                if ext in VIDEO_TYPE:
                    return  VIDEO_TYPE[ext]
                return VIDEO_TYPE['avi']
        cap = cv2.VideoCapture(0)

        out = cv2.VideoWriter(filename, get_video_type(filename), 25,

        get_dims(cap, my_res))

        while True:

            ret, frame = cap.read()
            out.write(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
        cap.release()

        out.release()

        cv2.destroyAllWindows()

    elif click.get()=='Selfi by detect smile':
        video = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier("dataset/haarcascade_frontalface_default.xml")
        smileCascade = cv2.CascadeClassifier("dataset/haarcascade_smile.xml")

        while True:
            success,img = video.read()
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(grayImg,1.1,4)
            cnt=1
            keyPressed = cv2.waitKey(1)

            for x,y,w,h in faces:
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),3)
                smiles = smileCascade.detectMultiScale(grayImg,1.8,15)
                for x,y,w,h in smiles:
                    img = cv2.rectangle(img,(x,y),(x+w,y+h),(100,100,100),5)
                    print("Image "+str(cnt)+"Saved")
                    path=r'C:\Users\Mani Sai\OneDrive\Desktop\smileimages'+str(cnt)+'.jpg'
                    cv2.imwrite(path,img)
                    cnt +=1
                    if(cnt>=2):
                        break

            cv2.imshow('live video',img)
            if(keyPressed & 0xFF==ord('q')):
                break

        video.release()
        cv2.destroyAllWindows()

    elif click.get()=='Set timer':
        TIMER = int(5)

            # Open the camera
        cap = cv2.VideoCapture(0)


        while True:

            	# Read and display each frame
            ret, img = cap.read()
            cv2.imshow('a', img)

            	# check for the key pressed
            k = cv2.waitKey(125)

            	# set the key for the countdown
            	# to begin. Here we set q
            	# if key pressed is q
            if k == ord('q'):
            	    prev = time.time()

            	    while TIMER >= 0:
            		    ret, img = cap.read()

            			# Display countdown on each frame
            			# specify the font and draw the
            			# countdown using puttext
            		    font = cv2.FONT_HERSHEY_SIMPLEX
            		    cv2.putText(img, str(TIMER),
            					    (200, 250), font,
            					    7, (0, 255, 255),
            					    4, cv2.LINE_AA)
            		    cv2.imshow('a', img)
            		    cv2.waitKey(125)

            			# current time
            		    cur = time.time()

            			# Update and keep track of Countdown
            			# if time elapsed is one second
            			# than decrese the counter
            		    if cur-prev >= 1:
            			    prev = cur
            			    TIMER = TIMER-1

            	    else:
            		    ret, img = cap.read()

            			# Display the clicked frame for 2
            			# sec.You can increase time in
            			# waitKey also
            		    cv2.imshow('a', img)

            			# time for which image displayed
            		    cv2.waitKey(2000)

            			# Save the frame
            		    cv2.imwrite('camera.jpg', img)

            			# HERE we can reset the Countdown timer
            			# if we want more Capture without closing
            			# the camera

            	# Press Esc to exit
            elif k == 27:
            	    break

            # close the camera
        cap.release()

            # close all the opened windows
        cv2.destroyAllWindows()
    elif click.get()=='water mark':
        im = Image.open('camera.jpg')
        width, height = im.size

        draw = ImageDraw.Draw(im)
        text = "MBAT"

        font = ImageFont.truetype('arial.ttf', 70)
        textwidth, textheight = draw.textsize(text, font)

        # calculate the x,y coordinates of the text
        margin = 100
        x = width - textwidth - margin
        y = height - textheight - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), text, font=font)
        im.show()

        #Save watermarked image
        im.save('watermark1.jpg')


    else:
        myLabel=Label(root,text="hii").pack()

click=tk.StringVar(root)
click.set("Options")


def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0)
    # Setting width and height
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)
    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)
    # Removing text message from the camera label
    root.cameraLabel.config(text="")
    # Calling the ShowFeed() Function
    ShowFeed()

# Creating tkinter variables
destPath = StringVar()
imagePath = StringVar()

createwidgets()
root.mainloop()
root.mainloop()
