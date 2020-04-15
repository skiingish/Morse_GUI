# import all required
from time import sleep
from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)


## -- Hardware -- ##
outputLED = LED(23) # gpio 23

## -- Morse Code Dictionary -- ## 
# Dictionary representing the morse code chart 
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'} 
  

## -- GUI -- ##

win = Tk()
win.title("Morse Code Converter Blinker") # title
#win.geometry("200x200") # window size 
myFont = tkinter.font.Font(family = 'Helvetica', size = 16, weight = "bold") # font 

labelText = StringVar()

#### -- FUNCTIONS -- #### 

# shutdown the program 
def close():
    RPi.GPIO.cleanup()
    win.destroy()

# Function to convertToMorseCode the string 
# according to the morse code chart 
def convertToMorseCode(message): 
    cipher = '' 
    for letter in message: 
        if letter != ' ': 
  
            # Looks up the dictionary and adds the 
            # correspponding morse code 
            # along with a space to separate 
            # morse codes for different characters 
            cipher += MORSE_CODE_DICT[letter] + ' '
        else: 
            # 1 space indicates different characters 
            # and 2 indicates different words 
            cipher += ' '
  
    return cipher  

#get input from textbox
def retrieve_input():
    input = entryBox.get()
    return input

# function to take the input list of the morse code and 
# for each item to print and blink the LED to the correct item
def blinkThatWordYo(wordToBlink):
    for i in wordToBlink:
        if i == '.':
            print("dot")
            dotLEDOutput() 
        elif i == '-':
            print("dash")
            dashLEDOutput()
        elif i == ' ':
            print("space")
            spaceLEDOutput()
        else:
            print("Error!")

# - Functions that control LED output - # 
# dot led output
def dotLEDOutput():
    outputLED.on()
    sleep(0.5)
    outputLED.off()
    sleep(0.5)
# dash led output
def dashLEDOutput():
    outputLED.on()
    sleep(1.5)
    outputLED.off()
    sleep(0.5)
# sleep output
def spaceLEDOutput():
    sleep(2)

# - Main function - #
def main():
    inputText = retrieve_input() # get user input from text box
    if len(inputText) >= 12: #if the text is longer the 16 then exit and don't output
        print("The text can't be longer then 12 chars")
        entryBox.delete(0,END) #delete text
        return # Exit if user entered to bigger text
    
    print(inputText) # print plain text to console
    result = convertToMorseCode(inputText.upper()) # convert the capital input of the usertext to morse code
    print("Text in Morse Code: " + result) # print to morse code to console
    blinkThatWordYo(list(result)) # convert morse code to list and output each item to led
    entryBox.delete(0,END) #delete text once printed

## -- Widgets -- ##

entryBoxLabel = Label(win, textvariable=labelText)
labelText.set("Text to convert (max 12 chars)")
entryBoxLabel.grid(row=0, column=1, padx=40, pady=2)

entryBox = Entry(win)
entryBox.grid(row=1, column=1, padx=40, pady=2)

#Convert Button
exitButton = Button(win, text='Convert', font=myFont, command=main, bg='green', height=1, width=10)
exitButton.grid(row=2, column=1, padx=40, pady=10)


#Exit Button
exitButton = Button(win, text='Exit', font=myFont, command=close, bg='red', height=1, width=10)
exitButton.grid(row=4, column=1, padx=40, pady=10)


win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO as window closes 
win.mainloop() # Loops forever
