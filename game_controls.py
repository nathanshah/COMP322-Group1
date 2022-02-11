from turtle import position
import pyautogui
import math

last_position = (None,None)
last_dir = ''

def keypress():
    ''' 
    Choose any four keys that a user can press to control the game.
    Update this doc string with your choices. 
    '''

    import keyboard

    # put your code here
    while True:
        if keyboard.is_pressed('w'):
            pyautogui.press('up')

        elif keyboard.is_pressed('a'):
            pyautogui.press('left')

        elif keyboard.is_pressed('s'):
            pyautogui.press('down')

        elif keyboard.is_pressed('d'):
            pyautogui.press('right')


def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        # put your code here
        global last_position
        global last_dir

        if last_position[0] == None or last_position[1] == None:
            last_position = pyautogui.position()

        else:
            current_position = pyautogui.position()
            current_x = current_position[0]
            current_y = current_position[1]

            print("Last Position: ", end="")
            print(last_position)
            print("Current Position: ", end="")
            print(current_position)

            diff_x = current_x - last_position[0]
            diff_y = current_y - last_position[1]

            if abs(diff_x) >= 3 or abs(diff_y) >= 3:

                if abs(diff_y) > abs(diff_x): #up down
                    if diff_y < 0:
                        pyautogui.press('up')
                        last_dir = 'up'
                    else:
                        pyautogui.press('down')
                        last_dir = 'down'
                else: #left right
                    if diff_x > 0:
                        pyautogui.press('right')
                        last_dir = 'right'
                    else:
                        pyautogui.press('left')
                        last_dir = 'left'

                print("Last Position: ", end="")
                print(last_position)
                print("Current Position: ", end="")
                print(current_position, end="")
                print(last_dir)

            last_position = current_position        

    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = None
    colorUpper = None

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()


    while True:
        # your code here
        continue
        



def finger_tracking():
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    # put your code here


def unique_control():
    # put your code here
    pass

def main():
    control_mode = input("How would you like to control the game? ")
    if control_mode == '1':
        keypress()
    elif control_mode == '2':
        trackpad_mouse()
    elif control_mode == '3':
        color_tracker()
    elif control_mode == '4':
        finger_tracking()
    elif control_mode == '5':
        unique_control()

if __name__ == '__main__':
	main()
