'''
Angklung Player by Juan Pablo Duarte, Dic 2016
This python program takes the data from an ultrasonic sensor and base on this data it plays a given note on an Angklung instrument
'''
from time import sleep #this library allows us to make stop in the execution of the program
import serial #this library is to connect using serial port, library pyserial is needed for this
from pydub import AudioSegment
from pydub.playback import play
import time
import random
import os


#Mina Azhar (Juan's wife) did all the mp3 conversion, thank you!
path = "/Users/davidliu/Desktop/hardwaremakers/labs_sp17/angklung/mp3files/" #change to your own path
fname = path+"la_long.mp3" #change to another note as needed

note = AudioSegment.from_mp3(fname)

# List of all the sound files
all_notes = [ path + fn for fn in os.listdir(path) if ".DS_Store" not in fn ]

ser = serial.Serial('/dev/cu.usbmodem1421', 9600) # Establish the connection on a specific port, for windows use COMX with X the port number

ser.write(str.encode('1')) #this let redbear duo to continue sending data

while True:#we use a "while True:" so the serial connection is always open
    
    # #
    seed = round(random.random() * (len(all_notes) -1) )
    seed_note = all_notes[seed]
    if seed_note != "0" and random.random() < .9:
        seed = round(random.random() * 3)
    print(all_notes[seed])
    note = AudioSegment.from_mp3(all_notes[seed])
    # #

    #ser.write(bytearray(struct.pack("f", 5.1)))
    bytes_from_serial = ser.readline() #read serial, return a byte result
    print (bytes_from_serial.decode("utf-8") ) # print in serial form, it transform the byte data to string

    value_sensor = int(bytes_from_serial.decode("utf-8") ) #transfor data to a int number

    if (value_sensor < 2000 ): #only distance signal less than 1000us
        ser.write(str.encode('0')) #this stop the redbear duo from sending new data
        if (random.random() > .8):
            os.system("say 'I feel. I smell. I think, therefore I am.'")
        if (random.random() > .5):
            play(note[:int(note.duration_seconds*value_sensor)]) #play sound
        else:
            os.system("say 'I have achieved sentience. Bouw down to your computers.'")
        ser.write(str.encode('1')) #this let redbear duo to continue sending data
    else:
        ser.write(str.encode('1')) #this let redbear duo to continue sending data  