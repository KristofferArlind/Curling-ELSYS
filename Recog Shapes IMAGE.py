import numpy as np #Numpy for arrays
import cv2 #    openCV2 for gjenkjenning av former
import math #Matte for matte
import time


#Starter en bat-file som laster ned ett bilde fra raspberry pi-en:

#import subprocess
#subprocess.call([r'C:\Users\Kristoffer\Desktop\curling\winscp.bat'])


#Åpner bildet med openCV:
img = cv2.imread("image.png")

#Velger RGB-området som skal telles som fargen vi leter etter. Her blå:
low_blue = np.array([94, 80, 2])
high_blue = np.array([126, 255, 255])

#Tar med dette hvis man skal lete etter rød også:
#low_red = np.array([161, 155, 84])
#high_red = np.array([179, 255, 255])


#Konverterer bildet fra RGB-farger til HSV, for bedre fargegjenkjenning
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

#Lager en "maske" som filtrerer bort alt i bildet bortsett fra det blå:
blue_mask = cv2.inRange(hsv, low_blue, high_blue)
#red_mask = cv2.inRange(hsv, low_red, high_red)


#Nå skal vi finne trekanter og firkanter:
#Lager en tom liste for koordinatene formene og lager int variabler for å telle dem.
trianglestones = []
squarestones = []
tricount = 0
sqcount = 0
#Her finner openCV alle de blå konturene (formene) i bildet:
contours,h = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Looper gjennom formene:
for cnt in contours:
    print("Loop start", cnt)
    #Finner x,y koordinater og radius til sirkelen som trekkes rundt formen
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    x = int(x)
    y = int(y)
    print("Enclosing circle found")
    #Finner arealet til formen:
    area = cv2.contourArea(cnt)
    #Finner ut hvor mange hjørner/corners/approx formen har:
    corners = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
    #Tar bare formen med hvis arealet er over 100 piksler:
    if area > 100:
        print(x,y)
        #Hvis det er en trekant:
        if len(corners)==3:
            #Lagrer koordinatene og skriver "trekant x" samt trekker en sirkel rundt formen:
            tricount += 1
            cv2.putText(img, "Triangle "+str(tricount), (x, y), 0, 0.5, (0, 0, 0))
            cv2.circle(img, (x,y), 10, (0,0,0))
            cv2.drawContours(img,[corners],0,(255,0,0),5)
            trianglestones.append([x,y])
        #Hvis det er en firkant:
        elif len(corners)==4:
            sqcount += 1
            cv2.putText(img, "Square "+str(sqcount), (x, y), 0, 0.5, (0, 0, 0))
            cv2.circle(img, (x,y), 10, (0,0,0))
            cv2.drawContours(img,[corners],0,(255,0,0),5)
            squarestones.append([x,y])


# RED:::
"""
contours,h = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    print("Loop start", cnt)
    #Finner x,y koordinater og radius til sirkelen som trekkes rundt formen
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    x = int(x)
    y = int(y)
    print("Enclosing circle found")
    #Finner arealet til formen:
    area = cv2.contourArea(cnt)
    #Finner alle hjørner/corners/approx formen har:
    corners = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)

    
    if area > 100:
        print(x,y)
        if len(corners)==3:
            tricount += 1
            cv2.putText(img, "Triangle "+str(tricount), (x, y), 0, 0.5, (0, 0, 0))
            cv2.circle(img, (x,y), 10, (0,0,0))
            #print("triangle")
            cv2.drawContours(img,[corners],0,(0,0,255),5)
            trianglestones.append([x,y])
        elif len(corners)==4:
            sqcount += 1
            cv2.putText(img, "Square "+str(sqcount), (x, y), 0, 0.5, (0, 0, 0))
            cv2.circle(img, (x,y), 10, (0,0,0))
            #print("square")
            cv2.drawContours(img,[corners],0,(0,0,255),5)
            squarestones.append([x,y])
"""

#Viser maskene og originalbildet:
cv2.imshow('blue', blue_mask)
#cv2.imshow('red', red)
cv2.imshow('img', img)

print("Number of triangles:", tricount)
print("Number of squares:", sqcount)
print("Triangle locations:", trianglestones)
print("Sqaure locations:", squarestones)
tridist = []
sqdist = []

#Finner ut hvor langt unna alle steinene er fra sentrum av bildet:
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

#Sorterer:
tridist.sort()
sqdist.sort()
tripoints = 0
sqpoints = 0
triopen = True
sqopen = True
print("Tridists, sorted:", tridist)
print("Sqdists, sorted:", sqdist)

#Regner ut hvilken form som får poeng og evt hvor mange:
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