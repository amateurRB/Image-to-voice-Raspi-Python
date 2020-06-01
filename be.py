#from PIL import Image
import cv2 
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.font as font

import time  # Used for time stamp on audio file
from gtts import gTTS  # Google Text To Speech
from gtts import lang  # Languages available in gtts
from playsound import playsound  # To play the audio
from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
tessdata_dir_config ="C:\Program Files (x86)\Tesseract-OCR\tessdata"
#text = pytesseract.image_to_string(Image.open(filename))
#self.textbox.append(text)


#lang = get_key(seleced_language)

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
text=''
while True:
    try:
        check, frame = webcam.read()
        
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'): 
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()
            im = Image.open('saved_img.jpg')
            
            text= pytesseract.image_to_string(im,lang = 'eng', config=tessdata_dir_config)
            
            break
        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
        
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

def readFimage():
    #text = pytesseract.image_to_string(im, lang = 'mar', config=tessdata_dir_config)
    ResultTextBox.delete('1.0',END)
    ResultTextBox.insert(END,text)
def get_key(val):
    for key, value in languages.items():
        if val == value:
            return key

    return "Key doesn't exist"
def convert_to_speech():
    seleced_language = defaultSelect.get()

    lang = get_key(seleced_language) # For different accent audio
    #if (seleced_language=="English"):
    #text= pytesseract.image_to_string(im,lang = lang, config=tessdata_dir_config)
    #else:
        #text= pytesseract.image_to_string(im,lang = lang, config=tessdata_dir_config)
    try:
        speech = gTTS(text=text, lang=lang)
    except AssertionError as e:
        print("NO")

    time_stamp = time.strftime("%Y%m%d_%H%M%S")
    # Make sure audio folder is already present or else it will give error
    generate_file_name = f'./audio/audio_{lang}_{time_stamp}.mp3'
    try:
        speech.save(generate_file_name)
        playsound(generate_file_name)
    except UnboundLocalError as e:
        print("TEXT!!!")

    



root = Tk()
root.geometry("700x800")
defaultSelect = StringVar()
seleced_language= StringVar()

root.configure(bg="purple")
Title = root.title( "Image Reader!")
#path = StringVar()
myFont = font.Font(family='Courier', size=10, weight='bold')

HeadLabel1 = Label(root,text="Image ")
HeadLabel1.grid(row = 1,column = 1,sticky=(E))
HeadLabel2 = Label(root,text=" Reader")
HeadLabel2.grid(row = 1,column = 2,sticky=(W))

#InputLabel = Label(root,text = "INPUT IMAGE:")
#InputLabel.grid(row=2,column = 1)

ReadButton = Button(root,text="READ FROM IMAGE",command = readFimage,bg='#b19cd9')
ReadButton.grid(row = 2,column = 0)


languages = lang.tts_langs()

defaultSelect.set(languages['en'])
options = languages.values()
dropdown = OptionMenu(root,defaultSelect, *options)
dropdown.grid(row=6, column=0)

button = Button(root, text="HEAR THE TEXT", command=convert_to_speech,bg='#b19cd9')
button.grid(row=10, column=0)


ReadButton['font'] = myFont
button['font'] = myFont


DataLabel = Label(root,text = "DATA IN IMAGE:")
DataLabel.grid(row = 6,column=1,sticky=(W))

ResultTextBox = Text(root,height = 16)
ResultTextBox.grid(row = 7,column = 1,columnspan=2)



root.mainloop()
