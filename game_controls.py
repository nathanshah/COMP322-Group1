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
    colorLower = (29,86,6) #GREEN
    colorUpper = (64,255,255)

    #colorLower = (210,30,13) #PURPLE
    #colorUpper = (250,50,67)


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
        frame_raw = frame.copy()
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

            if abs(dX) >= 100 or abs(dY) >= 100:

                if abs(dY) > abs(dX): #up down
                    if dY < 0 and direction != 'up':
                        pyautogui.press('up')
                        #print("UP")
                        direction = 'up'
                    elif direction != 'down':
                        pyautogui.press('down')
                        #print("DOWN")
                        direction = 'down'
                else: #left right
                    if dX > 0 and direction != 'right':
                        pyautogui.press('right')
                        direction = 'right'
                        #print("RIGHT")
                    elif direction != 'left':
                        pyautogui.press('left')
                        #print("LEFT")
                        direction = 'left'

        cv2.putText(frame_raw, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
        cv2.imshow('Game Control Window', frame_raw)
        num_frames +=1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #print("Frame: %d, Pts: %d, Contour: %d, dX: %d, dY: %d" %(num_frames, len(pts), len(contours), dX, dY))

        

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

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(static_image_mode = False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    global last_dir

    while True:
        frame = vs.read()

        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame, width=600)
        frame_raw = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame)

        num_fingers = 0
        landmark_list = []

        if not results.multi_hand_world_landmarks:
            continue

        for hand_item in results.multi_hand_world_landmarks:
            for id, Im in enumerate(hand_item.landmark):

                (height, width, other) = frame.shape
                new_x = width * Im.x
                new_y = height * Im.y

               # cv2.circle(frame, (new_x,new_y), 3, (255,0,255), cv2.FILLED)
                landmark_list.append((id,new_x,new_y))
        
        if len(landmark_list) > 0:
            if landmark_list[4][1] < landmark_list[3][1]:
                num_fingers+=1
            
            if landmark_list[8][2] < landmark_list[6][2]:
                num_fingers+=1
            
            if landmark_list[12][2] < landmark_list[10][2]:
                num_fingers+=1

            if landmark_list[16][2] < landmark_list[14][2]:
                num_fingers+=1

            if landmark_list[20][2] < landmark_list[18][2]:
                num_fingers+=1

        if num_fingers == 1 and last_dir != 'up':
            #print("UP")
            pyautogui.press('up')
            last_dir = 'up'
        
        elif num_fingers == 2 and last_dir != 'down':
            #print("DOWN")
            pyautogui.press('down')
            last_dir = 'down'

        elif num_fingers == 3 and last_dir != 'left':
            #print("LEFT")
            pyautogui.press('left')
            last_dir = 'left'

        elif num_fingers == 4 and last_dir != 'right':
            #print("RIGHT")
            pyautogui.press('right')
            last_dir = 'right'

        cv2.putText(frame_raw,str(int(num_fingers)),(10,70),cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.imshow("Image", frame_raw)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def unique_control():
    # put your code here
    # pyaudio may not be able to be downloaded 
    # pip install pipwin
    # pip install pyaudio
    # instuctions on how to do this found by watching
    # 1) https://www.youtube.com/watch?v=K_WbsFrPUCk
    # 2) https://www.youtube.com/watch?v=dNMIdxWFfGg

   import speech_recognition as sr
   import pyttsx3

   engine = pyttsx3.init()
   engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')

   global last_dir

   r = sr.Recognizer()

   with sr.Microphone() as source:

       while True:
           audio = r.listen(source)

           try:
               command = r.recognize_google(audio)

               #print(command)

               if command == 'up' and last_dir != 'up':
                   pyautogui.press('up')
               elif command == 'down' and last_dir != 'down':
                   pyautogui.press('down')
               elif command == 'left' and last_dir != 'left':
                    pyautogui.press('left')
               elif command == 'right' and last_dir != 'right':
                    pyautogui.press('right')
               elif command == 'stop':
                   break
               else:
                    engine.say("Do not understand command")
                    engine.runAndWait()

           except:
               engine.say("Do not understand command")
               engine.runAndWait()
               
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
