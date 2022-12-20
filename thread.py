#!/usr/bin/env python3
import cv2
from deepface import DeepFace
import numpy as np
import RPi.GPIO as GPIO
import time
import sys
import board
import neopixel
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import datetime
import multiprocessing
from rpi_ws281x import PixelStrip, Color
#import pygame
#from pygame.locals import*
import argparse

text = "Happy Halloween!!"
pixel_pin = board.D18
pixel_pin2 = board.D21
num_pixels = 192
display_width = 24
display_height = 8
num_pixels2 = 192
matrixbrightness = 0.2
scrollSpeed = 0.14 #adjust the scrolling speed here-> smaller number=faster scroll
TextColor = (0,255,0) #set the color of your text here in RGB, default is white
servoPIN = 2
servoPIN2 = 3
# LED strip configuration:
LED_COUNT = 32        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LED_COUNT2 = 192        # Number of LED pixels.
LED_PIN2 = 18          # GPIO pin connected to the pixels (18 uses PWM!).
GPIO.setup(servoPIN, GPIO.OUT) #uses GPIO.BCM mode set in neopixel library
pwm = GPIO.PWM(servoPIN, 50) # GPIO 3 for PWM with  clock frequency 50Hz
pwm.start(0) #servo will always start with a 0 duty cycle
GPIO.setup(servoPIN2, GPIO.OUT) #uses GPIO.BCM mode set in neopixel library
pwm2 = GPIO.PWM(servoPIN2, 50) # GPIO 3 for PWM with  clock frequency 50Hz
pwm2.start(0) #servo will always start with a 0 duty cycle


ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=matrixbrightness, auto_write=False, pixel_order=ORDER)
#pixels2 = neopixel.NeoPixel(pixel_pin2, num_pixels2, brightness=matrixbrightness, auto_write=False, pixel_order=ORDER)

rotation = 0
#load your font
font = ImageFont.truetype("LiberationMono-Regular.ttf", 9)
 # Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
strip2 = PixelStrip(LED_COUNT2, LED_PIN2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip2.begin()



#for the Adafruit NeoMatrix grid
def getIndex(x, y):        
    x = display_width-x-1    
    return (x*8)+y

#use for the flex grid
def getIndex2(x, y):
    x = display_width-x-1
    if x % 2 != 0:
        return (x*8)+y
    else:
        return (x*8)+(7-y)

if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)
# Measure the size of our text
text_width, text_height = font.getsize(text)

# Create a new PIL image big enough to fit the text
image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
draw = ImageDraw.Draw(image)

#for servos
draw.text((display_width, -1), text, font=font, fill=255)
image.save("img.png", "PNG")
def SetAngle(angle):
    duty = angle/18 +2
    GPIO.output(2,True) #turns on the pin for output
    GPIO.output(3,True) #turns on the pin for output
    pwm2.ChangeDutyCycle(duty) #change the duty cycle to math the one we calculated
    pwm.ChangeDutyCycle(duty) #change the duty cycle to math the one we calculated
    sleep(1) #wait 1 second
    GPIO.output(2, False) #turns off the pin
    GPIO.output(3, False) #turns off the pin
    #servo.duty_cycle =0 #changes it back to 0
    pwm.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0) #change the duty cycle to math the one we calculated
    
    
#for led ring effect
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

#for led ring effect
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

#for led ring effect
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

#for led ring effect
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

#for led ring effect
def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

#for led ring effect
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

#def media(sound):
    #pygame.mixer.init()
    #pygame.mixer.music.load(sound)
    #pygame.mixer.music.play(-1)
    #time.sleep(2)
    #pygame.mixer.quit()
#for servos    
def function1():
    #SetAngle(90)
    #SetAngle(179)
    def countdown(h, m, s):
        total_seconds = h*3600 + m*60 + s
    
        while total_seconds >0:
            timer = datetime.timedelta(seconds = total_seconds)
            print(timer, end= "\r")
            #time.sleep(1)
            SetAngle(179)
            SetAngle(90)
            total_seconds -= 1
        print("Bzzt! The countdown is at zero seconds!")
    i =0
#goes from 90 degrees to 170 degrees 5 times like a toggle
    while True:
        countdown(0,0,3)   
        i+=1   
        if i ==1:
            break
    print("Inside The Function 1")
#For text on led panels
def function2():
    def countdown(h, m, s):
        total_seconds = h*3600 + m*60 + s
        offset_x =0
        while total_seconds >0:
            timer = datetime.timedelta(seconds = total_seconds)
            print(timer, end= "\r")
              
            for x in range(display_width):
                for y in range(display_height):			
                    if image.getpixel((x + offset_x, y)) == 255:
                        pixels[getIndex2(x,y)] = TextColor
                        
                    else:
                        pixels[getIndex2(x,y)] = (0, 0, 0)                                

            offset_x += 1
            if offset_x + display_width > image.size[0]:
                offset_x = 0

            pixels.show()
            time.sleep(scrollSpeed) #scrolling text speed
            total_seconds -= 1
    i =0
    while True:
        countdown(0,1,50)   
        i+=1   
        if i ==1:
            pixels.fill((0, 0, 0))
            break
    print("Inside The Function 2")
#for rainbow effect on panels    
def function3():
        def wheel2(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
            if pos < 0 or pos > 255:
                r = g = b = 0
            elif pos < 85:
                r = int(pos * 3)
                g = int(255 - pos * 3)
                b = 0
            elif pos < 170:
                pos -= 85
                r = int(255 - pos * 3)
                g = 0
                b = int(pos * 3)
            else:
                pos -= 170
                r = 0
                g = int(pos * 3)
                b = int(255 - pos * 3)
            return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
        def rainbow_cycle(wait):
            for j in range(255):
                for i in range(num_pixels):
                    pixel_index = (i * 256 // num_pixels) + j
                    pixels[i] = wheel2(pixel_index & 255)
                pixels.show()
                time.sleep(wait)
        x = 0
        while True:
            pixels.show()
            time.sleep(1)
            print('rainbow time!')
            rainbow_cycle(0.005)  # rainbow cycle with 1ms delay per step
            x +=1
            print(x)
            if (x == 2):
                break
                
def function4():
    print('Idle Mode')
    pixels.fill((0, 0, 255))
    pixels.fill((255, 0, 255))
    pixels.fill((255, 255, 0))
    pixels.fill((0, 0, 0))
    colorWipe(strip, Color(255, 255, 255))
    SetAngle(90)
    
    
#led ring
def function5():
    print('Color wipe animations.')
    colorWipe(strip, Color(255, 0, 0))  # Red wipe
    colorWipe(strip, Color(0, 255, 0))  # Green wipe
    colorWipe(strip, Color(0, 0, 255))  # Blue wipe
    colorWipe(strip, Color(255, 0, 0))  # Red wipe
#led ring
def function6():
    print('Theater chase animations.')
    theaterChase(strip, Color(127, 127, 127))  # White theater chase
    theaterChase(strip, Color(127, 0, 0))  # Red theater chase
    theaterChase(strip, Color(0, 0, 127))  # Blue theater chase

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    sys.path.append('/lib/python3.9/dist-packages')
    face_cascade = cv2.CascadeClassifier(r'/home/pi/Desktop/scrollingTextMask/haarcascade_frontalface_default.xml')
    
    frame_num=0
    while(True):
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.4,5)
        
        if(np.shape(faces)[0] == 1):
            for (x,y,w,h) in faces:
                img_crop = img[y:y+h, x:x+w]
            if(frame_num%10 == 0):
                predictions = DeepFace.analyze(img_crop, actions = ['emotion'], enforce_detection = False)
            if(predictions['dominant_emotion'] == 'sad'):
                print("face is sad")
                function2()
                function4()
            elif(predictions['dominant_emotion'] == 'happy'):
                print("face is happy")
                function1()
                function6()
                function2()
                #time.sleep(3)
            elif(predictions['dominant_emotion'] == 'surprise'):
                print("face is surprise")
                function5()
                function2()
                #time.sleep(3)
            
            print(predictions['dominant_emotion'])
            predictions['dominant_emotion'] = 0
            frame_num+=1
    
        else:
            print("No faces or too many faces found")
            #function4()
GPIO.cleanup() #cleans up and resets any ports that was used in the program


