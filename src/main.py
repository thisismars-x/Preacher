'''
This program allows a user to natively use gesture control
to rotate and translate a wireframe model.

Controls:
---------

[LEFT]: pinch to rotate
    vertically to rotate in y axes
    horizontally to rotate in x axes
    .. or any combination

[RIGHT]: move your hand wherever you want to
    move the model also
    zoom factor is controlled by a slider on screen
'''

import numpy as np
import pygame as pgm
import pygame_widgets
from pygame_widgets.slider import Slider
from math import sin, cos, radians
import cv2 as cv
import mediapipe as mp

'''to parse wireframe model | necessary transformations'''
from parser import decode
from declarations import *
from move import *

'''top level declarations'''
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

pgm.init()

if PREACHERMAN:
    pgm.mixer.init()
    pgm.mixer.music.load('../resources/preacher man.mp3')
    pgm.mixer.music.play(-1)

screen = pgm.display.set_mode(SCREEN)
pgm.display.set_caption("e3D")
clock = pgm.time.Clock()

'''
------------------
adding more support                                     
chose your .obj wireframe directly from application
set ROTATESPEED, CAMERAINDEX, etc. global variables
a help manual

To disable shell, run with flag --no-shell, or CLIWINDOW = True
To enable opencv window run with --cv-open, or SHOWCVWINDOW = True
--cv-open sets SHOWCVWINDOW = True
'''

import argparse
args = argparse.ArgumentParser(description = "Disable shell")
args.add_argument('--no-shell', action = 'store_true')
args.add_argument('--cv-open', action = 'store_true')
__args = args.parse_args()

if __args.cv_open:
    SHOWCVWINDOW = True

if __args.no_shell:
    CLIWINDOW = False


def text(msg, x, y):
    '''
    nothing special
    renders text for my basic cli-alike interface
    '''
    font = pgm.font.SysFont('p052', 20)
    label = font.render(msg, True,  BLUE)
    screen.blit(label, (x, y))

'''
exits_all is set when we exit the initial 'shell' by the window directly(using X button), this causes
all applied settings to be default and does not proceed to other window
'''
exits_all = False

import time, os
def command_parser(command):
    global EXAMPLE, ROTATIONSPEED, CAMERA_INDEX, SHOWCVWINDOW

    PATH = EXAMPLE 
    ROTATE = ROTATIONSPEED
    INDEX = CAMERA_INDEX
    SHOWCV = SHOWCVWINDOW
    
    command = command.strip()
    commands = command.split(' ')

    '''
    some useful commands
    'help' for any questions
    '''

    if commands[0] == '':
        return ["   No command entered."]

    elif commands[0] == 'cd' and len(commands) > 1:
        try:
            os.chdir(commands[1])
            PATH = commands[1]
            return [f"  Switched to {os.getcwd()}"]
        except FileNotFoundError:
            return ["   Directory not found."]
        except NotADirectoryError:
            return ["   Not a directory."]
        except PermissionError:
            return ["   Permission denied."]

    elif commands[0] == 'ls':
        return os.listdir(os.getcwd())

    elif commands[0] == 'clear':
        return [""]

    elif commands[0] == 'SPEEDROTATION' and len(commands) > 1:
        ROTATE = float(commands[1])
        ROTATIONSPEED = ROTATE
        return [f'  Rotation speed set at {ROTATE}']

    elif commands[0] == 'CAMERAINDEX' and len(commands) > 1:
        INDEX = int(commands[1])
        CAMERA_INDEX = INDEX
        return [f'  Camera at index {INDEX}']

    elif commands[0] == 'SET' and len(commands) > 1:
        PATH = os.path.join(os.getcwd(), commands[1])
        EXAMPLE = PATH
        return [f'  Set path to {PATH}']

    elif commands[0] == 'START':
        return ["   Exiting..."]
    
    elif commands[0] == "SHOWCVWINDOW" and len(commands) > 1:
        SHOWCVWINDOW = 0 if commands[1] == '0' else 1
        return [f'  OpenCV window enabled'] if SHOWCVWINDOW == 1 else ['    OpenCV window disabled']

    elif 'default' in command or 'reset' in command:
        CAMERA_INDEX = 1
        SPEEDROTATION = 0.2
        EXAMPLE = '../resources/preacher man.obj'
        return ['   Restored to default values']

    elif 'return' in command:
        return [f"  PATH: {PATH}",
                f"  SPEEDROTATION: {ROTATE}",
                f"  CAMERAINDEX: {INDEX}",
                f"  SHOWCV: {SHOWCV}",""]

    elif commands[0] == 'help':
        return [
            "Hello, Preacher!",
            "This is the 'help' section. Read below:",
            "All commands are somewhat lazily evaluated.",
            "Word count > 2, remains un-read", " ",
            "[cd] - change directory",
            "[ls] - lists subdirectories, can not access hidden files using flags", 
            "[CAMERAINDEX x[int]] - sets camera index for opencv-python",
            "OpenCV requires different indexes if an external camera is used",
            "Generally 0 is okay. If the application fails with:",
            "[can't open by camera index] then this will mitigate", " ",
            "[SHOWCV 1/0] - flag to show opencv window", 
            "[SET x.obj] - select model x.obj from this directory for display", 
            "[SPEEDROTATION x[float]] - set rotation speed. Default is almost always fine", " ",
            "[START] - proceed", 
            "[info] - About this Interface",
            "Any line with 'return'- logs values",
            "Any line with 'default or reset'- restores settings",
            "default/restore has more precedence than return."
        ]

    elif commands[0] == 'info':

        return ["About this Interface", " ",
        "All the top level declarations go to [declaration.py]",
        "All necessary functions go to [move.py]",
        "File parsing is done entirely in [parser.py]", " ",
        "Later, if you want to run the program without shell, place your wireframe in src",
        "and change EXAMPLE to your file name",
        "You can play with the parameters from declarations",
        "It's much easier to just use the shell interface",
        "run [python3 main.py --no-shell] to avoid shell, by default shows EXAMPLE model",
        "you can add [--cv-open] to show open cv window along side your model",
        "I use [poetry] for requirements, the .lock file guarantees no version breaks",
        "Install poetry, run poetry install, then poetry shell to activate venv"]

    return ["Unrealizable command. For help, type help."]


def shell():

    global exits_all

    in_ = ''
    output = []
    output_time = None

    running = True
    while running:
        screen.fill(BLACK)
        text("  >   " + in_, 10, 20)

        for i, line in enumerate(output):
            text(line, 10, 60 + i * 25)

        pgm.draw.rect(screen, BLUE, (5, 10, SCREEN[0] - 10, 40), 2)
        pgm.display.flip()

        for event in pgm.event.get():
            if event.type == pgm.QUIT:
                exits_all = True
                running = False

            if event.type == pgm.KEYDOWN:
                if event.key == pgm.K_RETURN:
                    output = command_parser(in_)
                    in_ = ''
                    output_time = time.time()

                    if "   Exiting..." in output:
                        running = False  
                        
                elif event.key == pgm.K_BACKSPACE:
                    in_ = in_[:-1]
                else:
                    in_ += event.unicode

        pgm.display.flip()




'''to display necessary status'''
FONT = pgm.font.Font('../resources/1942.ttf', FONTSIZE)

'''
instead of using hands for zoom, i resort to using manual zoom sliders
images are much steadier this way and generally a single zoom factor
is enough for visualization
'''
slider = Slider(screen, SCREEN[0]//8 , SCREEN[1] * 9 // 10, SCREEN[0] * 6 // 8, 12, min=1, max=2000, step=1, color=BLUE, handleColour=BLUE)


def draw(screen, vertices, edges):
    '''
    Draw the wireframe model
    '''
    for edge in edges:
        start, end = edge
        pgm.draw.line(screen, BLUE, vertices[start], vertices[end], WIDTH)

def main():
    global ZOOM

    ZOOM = slider.getValue() 

    cap = cv.VideoCapture(CAMERA_INDEX)
    angle_x, angle_y = 0, 0
    translation_x, translation_y = 0, 0
    running = True

    vertices, edges = decode(EXAMPLE)

    while running:
        events = pgm.event.get()
        for event in events:
            if event.type == pgm.QUIT:
                running = False

            slider.listen(event)


        ret, frame = cap.read()
        if not ret: break

        frame = cv.flip(frame, 1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        left_hand_found = False
        right_hand_found = False

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = hand_info.classification[0].label
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if label == "Left":
                    left_hand_found = True

                    '''left hand controls rotation'''
                    index_tip = hand_landmarks.landmark[8]
                    thumb_tip = hand_landmarks.landmark[4]

                    '''get pixel coordinates'''
                    index_x, index_y = int(index_tip.x * 800), int(index_tip.y * 600)
                    thumb_x, thumb_y = int(thumb_tip.x * 800), int(thumb_tip.y * 600)

                    distance = np.hypot(thumb_x - index_x, thumb_y - index_y)

                    if distance < 50:
                        angle_x += (thumb_y - index_y) * ROTATIONSPEED
                        angle_y += (thumb_x - index_x) * ROTATIONSPEED

                elif label == "Right":
                    right_hand_found = True

                    '''right hand controls translation'''
                    index_tip = hand_landmarks.landmark[8]

                    '''get pixel coordinates'''
                    index_x, index_y = int(index_tip.x * 800), int(index_tip.y * 600)

                    translation_x = index_x - SCREEN[0] // 2
                    translation_y = index_y - SCREEN[1] // 2


        if SHOWCVWINDOW:
            cv.imshow('Hand Tracking', frame)
            if cv.waitKey(1) & 0xFF == ord('q'): break

        screen.fill(BLACK)

        ZOOM = slider.getValue()

        rotated_vertices = rotate(vertices, angle_x, angle_y)
        projected_vertices = projection(rotated_vertices, 800, 600, scale=ZOOM, translation=(translation_x, translation_y))

        draw(screen, projected_vertices, edges)

        '''
        some information about the image
        and global constants
        
        the file name maybe too long to show
        reducing it's size
        '''

        paths = EXAMPLE.split('/')
        path_ = None

        path_ = EXAMPLE if len(paths) < 4 else paths[-1]

        text0 = FONT.render(f"Path               :{path_}", True, BLUE)
        text1 = FONT.render(f"Rotation speed at  :{ROTATIONSPEED}", True, BLUE)
        text2 = FONT.render(f"Camera index       :{CAMERA_INDEX}", True, BLUE)
        text3 = FONT.render(f"Nodes              :{len(vertices)}", True, BLUE)
        text4 = FONT.render(f"Edges              :{len(edges)}", True, BLUE)
        

        y_offset = 50
        screen.blit(text0, (50, y_offset))
        screen.blit(text1, (50, y_offset + text0.get_height()))
        screen.blit(text2, (50, y_offset + text0.get_height() + text1.get_height()))
        screen.blit(text3, (50, y_offset + text0.get_height() + text1.get_height() + text2.get_height()))
        screen.blit(text4, (50, y_offset + text0.get_height() + text1.get_height() + text2.get_height() + text3.get_height()))


        pgm.draw.rect(screen, BLUE, (20, 20, SCREEN[0] - 40, SCREEN[1] - 40), 2)
        pygame_widgets.update(events)

        slider.draw()
        
        
        pgm.display.flip()
        clock.tick(20)

    cap.release()
    cv.destroyAllWindows()
    pgm.quit()

if __name__ == "__main__":

    if not __args.no_shell: 
        shell()
    
    if not exits_all: 
        main()
