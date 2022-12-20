#!/usr/bin/env python3
import cv2
from deepface import DeepFace
import numpy as np
import RPi.GPIO as GPIO
import time
import datetime
import pygame
from pygame.locals import*


servoPIN = 2 #nose
servoPIN2 = 3 #hat
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT) 
pwm = GPIO.PWM(servoPIN, 50) # GPIO 3 for PWM with  clock frequency 50Hz
pwm.start(0) #servo will always start with a 0 duty cycle
GPIO.setup(servoPIN2, GPIO.OUT) #uses GPIO.BCM mode set in neopixel library
pwm2 = GPIO.PWM(servoPIN2, 50) # GPIO 3 for PWM with  clock frequency 50Hz
pwm2.start(0) #servo will always start with a 0 duty cycle

rotation = 0

#for servos
def SetAngle(angle):
    duty = angle/18 +2
    GPIO.output(2,True) #turns on the pin for output
    pwm.ChangeDutyCycle(duty) #change the duty cycle to math the one we calculated
    time.sleep(1) #wait 1 second
    GPIO.output(2, False) #turns off the pin
    #servo.duty_cycle =0 #changes it back to 0
    pwm.ChangeDutyCycle(0)
    
def SetAngle2(angle):
    duty = angle/18 +2
    GPIO.output(3,True) #turns on the pin for output
    pwm2.ChangeDutyCycle(duty) #change the duty cycle to math the one we calculated
    time.sleep(1) #wait 1 second
    GPIO.output(3, False) #turns off the pin
    #servo.duty_cycle =0 #changes it back to 0
    pwm2.ChangeDutyCycle(0) #change the duty cycle to math the one we calculated
    
def media(sound):
    pygame.mixer.init()
    #pygame.display.set_mode((200,100))
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(1)
    time.sleep(8)
    pygame.mixer.quit()
#for servos    
def function1():
    def countdown(h, m, s):
        total_seconds = h*3600 + m*60 + s
    
        while total_seconds >0:
            timer = datetime.timedelta(seconds = total_seconds)
            print(timer, end= "\r")
            #time.sleep(1)
            SetAngle(0)
            SetAngle(179)
            SetAngle(90)
            total_seconds -= 1
        print("Bzzt! The countdown is at zero seconds!")
    i =0
    while True:
        countdown(0,0,2)   
        i+=1   
        if i ==1:
            break
    
def function2():
    def countdown(h, m, s):
        total_seconds = h*3600 + m*60 + s
    
        while total_seconds >0:
            timer = datetime.timedelta(seconds = total_seconds)
            print(timer, end= "\r")
            #time.sleep(1)
            SetAngle2(179)
            SetAngle2(0)
            SetAngle2(90)
            total_seconds -= 1
        print("Bzzt! The countdown is at zero seconds!")
    i =0
#goes from 90 degrees to 170 degrees 5 times like a toggle
    while True:
        countdown(0,0,2)   
        i+=1   
        if i ==1:
            break
    print("Inside The Function 1")
#For text on led panels
def function3(sound):
    print("Inside The Function 2")
    media(sound)

                

    


    
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('/home/pi4/Desktop/Pumpkin_1/bullshit/8f51e58ac0813cb695f3733926c77f52-07eed8d5486b1abff88d7e34891f1326a9b6a6f5/haarcascade_frontalface_default.xml')
    
    frame_num=0
    while(True):
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.4,5)
        #function3("annoying.wav")
        if(np.shape(faces)[0] == 1):
            for (x,y,w,h) in faces:
                img_crop = img[y:y+h, x:x+w]
            if(frame_num%10 == 0):
                predictions = DeepFace.analyze(img_crop, actions = ['emotion'], enforce_detection = False)
            if(predictions['dominant_emotion'] == 'sad'):
                print("face is sad")
                function1()
                media("sad.mp3")
            elif(predictions['dominant_emotion'] == 'happy'):
                print("face is happy")
                function1()
                function2()
                media("happy.mp3")
            elif(predictions['dominant_emotion'] == 'neutral'):
                print("face is neutral")
                function1()
                media("neutral.mp3")
            elif(predictions['dominant_emotion'] == 'fear'):
                print("face is fear")
                function2()
                media("fear.mp3")
            
            print(predictions['dominant_emotion'])
            predictions['dominant_emotion'] = 0
            frame_num+=1
    
        else:
            print("No faces or too many faces found")
            
GPIO.cleanup() #cleans up and resets any ports that was used in the program


