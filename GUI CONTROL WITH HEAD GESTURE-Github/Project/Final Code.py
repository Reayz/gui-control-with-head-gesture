
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

flag = 1;
oldx = -1;
oldy = -1;
cnt = 0;

main_frame_x1 = 100;
main_frame_y1 = 100;
main_frame_x2 = 300;
main_frame_y2 = 250;

left_x1 = 30;
left_y1 = 30;
left_x2 = 80;
left_y2 = 80;

right_x1 = 500;
right_y1 = 30;
right_x2 = 550;
right_y2 = 30;

img = None

def color_all():
    # rectange for left mouse
    cv2.rectangle(img, (30,30), (80,80), (255,0,0), 3)
    cv2.rectangle(img, (30,30), (55,55), (255,0,0), -1)

    # rectange for right mouse
    cv2.rectangle(img, (130,30), (180,80), (255,0,0), 3)
    cv2.rectangle(img, (155,30), (180,55), (255,0,0), -1)
    
    # rectange for double mouse
    cv2.rectangle(img, (230,30), (280,80), (255,0,0), 3)
    cv2.rectangle(img, (240,40), (260,60), (255,0,0), -1)
    cv2.rectangle(img, (250,50), (270,70), (255,0,0), -1)  

def color_left():
    # rectange for left mouse
    cv2.rectangle(img, (30,30), (80,80), (0,0,255), 3)
    cv2.rectangle(img, (30,30), (55,55), (0,0,255), -1)

def color_right():
    # rectange for right mouse
    cv2.rectangle(img, (130,30), (180,80), (0,0,255), 3)
    cv2.rectangle(img, (155,30), (180,55), (0,0,255), -1)

def color_double():
    # rectange for double mouse
    cv2.rectangle(img, (230,30), (280,80), (0,0,255), 3)
    cv2.rectangle(img, (240,40), (260,60), (0,0,255), -1)
    cv2.rectangle(img, (250,50), (270,70), (0,0,255), -1)
    
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 10)

    color_all();
    if flag == 1:
        color_left();
        
    if flag == 2:
        color_right();

    if flag == 3:
        color_double();
        
    cv2.rectangle(img, (main_frame_x1,main_frame_y1), (main_frame_x2,main_frame_y2), (0,0,0), 2)

    mx = -1
    for (x,y,w,h) in faces:
        mx=max(mx, w*h);

    newx = -1;
    newy = -1;
    for (x,y,w,h) in faces:
        if(mx==w*h):
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

            if x>=30 and x<=80 and y>=30 and y<=80:
                flag=1; # left click
                color_all();
                color_left();

            if x>=130 and x<=180 and y>=30 and y<=80:
                flag=2;  # right click
                color_all();
                color_right();

            if x>=230 and x<=280 and y>=30 and y<=80:
                flag=3;  # double click
                color_all();
                color_double();
            
            newx = x - main_frame_x1;
            newy = y - main_frame_y1;

            newx = (newx*sx)/(main_frame_x2-main_frame_x1);
            newy = (newy*sy)/(main_frame_y2-main_frame_y1);
                
            mouse.position = (newx, newy)
           

            if oldx == -1:
                oldx = newx;
                oldy = newy;
            else:

                # print cnt

                if abs(oldx - newx) > 30:
                    oldx = newx;
                    oldy = newy;
                    cnt = 0;
                else:
                    cnt = cnt + 1;
                    if cnt < 10:
                        continue;
                    
                    if flag == 1:
                       mouse.click(Button.left, 1);
                    if flag == 2:
                        mouse.click(Button.right, 1);
                    if flag == 3:
                        mouse.click(Button.left, 2);
                    
                    cnt = 0;
                    oldx = newx;
                    oldy = newy;
                    
            break;
    
        
    cv2.imshow('Result', img)
    #img_new = cv2.resize(img, (510, 510))
    #cv2.imshow('new', img_new)

    # stop with Esc key
    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()

