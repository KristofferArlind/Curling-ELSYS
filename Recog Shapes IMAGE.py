# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:16:01 2019

@author: Kristoffer
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 08:45:51 2019

@author: Kristoffer
"""

import numpy as np
import cv2
import math
import time


#import subprocess
#subprocess.call([r'C:\Users\Kristoffer\Desktop\curling\winscp.bat'])


#time.sleep(5)
#xcoor = np.array()
#ycoor = np.array()
#img = cv2.imread('shapes.png')
img = cv2.imread("image.png")
#colorlist = [[0,0,255], [0,128,255], [0,255,0], [0,255,255], [255,255,0], [255,128,0], [255,0,255], [127,0,255]]


low_blue = np.array([94, 80, 2])
high_blue = np.array([126, 255, 255])

#low_red = np.array([161, 155, 84])
#high_red = np.array([179, 255, 255])



hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

blue_mask = cv2.inRange(hsv, low_blue, high_blue)
blue = cv2.bitwise_and(img, img, mask=blue_mask)
#red_mask = cv2.inRange(hsv, low_red, high_red)
#red = cv2.bitwise_and(img, img, mask=red_mask)

#kernel = np.ones((5, 5), np.uint8)
#mask = cv2.erode(mask, kernel)

    
trianglestones = []
squarestones = []
contours,h = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
tricount = 0
sqcount = 0
for cnt in contours:
    print("Loop start", cnt)
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    x = int(x)
    y = int(y)
    print("Enclosing circle found")
    area = cv2.contourArea(cnt)
    approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
    #x = approx.ravel()[0]
    #y = approx.ravel()[1]
    
    if area > 100:
        print(x,y)
        if len(approx)==3:
            tricount += 1
            cv2.putText(img, "Triangle "+str(tricount), (x, y), 0, 0.5, (0, 0, 0))
            cv2.circle(img, (x,y), 10, (0,0,0))
            #print("triangle")
            cv2.drawContours(img,[approx],0,(255,0,0),5)
            trianglestones.append([x,y])
        elif len(approx)==4:
            sqcount += 1
            cv2.putText(img, "Square "+str(sqcount), (x, y), 0, 0.5, (0, 0, 0))
            cv2.circle(img, (x,y), 10, (0,0,0))
            #print("square")
            cv2.drawContours(img,[approx],0,(255,0,0),5)
            squarestones.append([x,y])


# RED:::
"""
contours,h = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv2.contourArea(cnt)
    approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if area > 100:
        if len(approx)==3:
            cv2.putText(img, "Triangle", (x, y), 0, 1, (0, 0, 0))
            print("triangle")
            cv2.drawContours(img,[approx],0,(0,0,255),5)
            tricount += 1

        elif len(approx)==4:
            cv2.putText(img, "Square", (x, y), 0, 1, (0, 0, 0))
            print("square")
            cv2.drawContours(img,[cnt],0,(0,0,255),5)
            sqcount += 1
"""
cv2.imshow('blue', blue)
#cv2.imshow('red', red)
cv2.imshow('img', img)

print("Number of triangles:", tricount)
print("Number of squares:", sqcount)
print("Triangle locations:", trianglestones)
print("Sqaure locations:", squarestones)
tridist = []
sqdist = []

resolution = [800,800]
origo = [resolution[0]/2, resolution[1]/2]
for i in range(len(trianglestones)):
    xdist = abs(trianglestones[i][0]-origo[0])
    ydist = abs(trianglestones[i][1]-origo[1])
    tridist.append(math.sqrt(xdist**2+ydist**2))

for i in range(len(squarestones)):
    xdist = abs(squarestones[i][0]-origo[0])
    ydist = abs(squarestones[i][1]-origo[1])
    sqdist.append(math.sqrt(xdist**2+ydist**2))

print("Tridists, not sorted:", tridist)
print("Sqdists, not sorted:", sqdist)

tridist.sort()
sqdist.sort()
tripoints = 0
sqpoints = 0
triopen = True
sqopen = True
print("Tridists, sorted:", tridist)
print("Sqdists, sorted:", sqdist)

while min(len(tridist), len(sqdist)) > 0:
    if tridist[0] < sqdist[0] and triopen:
        tripoints += 1
        del tridist[0]
        sqopen = False
    elif tridist[0] > sqdist[0] and sqopen:
        sqpoints += 1
        del sqdist[0]
        triopen = False
    else:
        break
print("Triangle:", tripoints)
print("Square:", sqpoints)
        



cv2.waitKey(0)
cv2.destroyAllWindows()