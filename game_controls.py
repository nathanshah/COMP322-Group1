from ast import While
from turtle import position
import pyautogui

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

            diff_x = current_x - last_position[0]
            diff_y = current_y - last_position[1]

            if abs(diff_x) >= 3 or abs(diff_y) >= 3:

                if abs(diff_y) > abs(diff_x): #up down
                    if diff_y < 0 and last_dir !='up':
                        pyautogui.press('up')
                        last_dir = 'up'
                    elif last_dir != 'down':
                        pyautogui.press('down')
                        last_dir = 'down'
                else: #left right
                    if diff_x > 0 and last_dir != 'right':
                        pyautogui.press('right')
                        last_dir = 'right'
                    elif last_dir != 'left':
                        pyautogui.press('left')
                        last_dir = 'left'

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
    colorLower = (0,128,128)
    colorUpper = (255,255,255)

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

    center = None

    vs = mw.WebcamVideoStream().start()

    while True:
        frame = vs.read()

        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame, width=600)
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(frame, colorLower, colorUpper)
        mask = cv2.erode(mask,None,iterations =2)
        mask = cv2.dilate(mask,None,iterations =2)

        (contours, hierarchy) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            max_contour = max(contours, key= cv2.contourArea)
            (pt, radius) = cv2.minEnclosingCircle(max_contour)
            M = cv2.moments(max_contour)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            if radius > 10:
                pts.appendleft(center)
        
        if num_frames >= 10 and len(pts) >= 10:
            (dX,dY) = tuple(map(lambda i,j: i-j, pts[0], pts[9] ))

            if abs(dX) >= 25 or abs(dY) >= 25:

                if abs(dY) > abs(dX): #up down
                    if dY < 0 and direction != 'up':
                        pyautogui.press('up')
                        print("UP\n")
                        direction = 'up'
                    elif direction != 'down':
                        pyautogui.press('down')
                        print("DOWN\n")
                        direction = 'down'
                else: #left right
                    if dX > 0 and direction != 'right':
                        pyautogui.press('right')
                        direction = 'right'
                        print("RIGHT\n")
                    elif direction != 'left':
                        pyautogui.press('left')
                        print("LEFT\n")
                        direction = 'left'

        cv2.putText(frame, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
        cv2.imshow('Game Control Window', frame)
        num_frames +=1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        

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
