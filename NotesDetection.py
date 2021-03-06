import skimage
from debug_utils import *
import numpy as np
import os
import cv2
from skimage.transform import hough_line, hough_line_peaks
import itertools 
from skimage.measure import find_contours
from statistics import mean
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from skimage import data, color, img_as_ubyte
from skimage.morphology import binary_erosion, binary_dilation, binary_closing,skeletonize, thin

import Binarization as binarization

lineNames = ['c1','d1','e1','f1','g1','a1','b1','c2','d2','e2','f2','g2','a2','b2']

# Returns the coordinates of note and array of the note names
def NotesPositions(thresholdedImg,linesPos,space,noteImg,thickness):

    # Creating circle SE with size of the note circle
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(space*0.9),int(space*0.9)))    
    erosion = cv2.erode(noteImg,kernel,iterations = 1)
    
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(space*0.05)+3,int(space*0.05)+3)) 
    erosion = cv2.morphologyEx(erosion, cv2.MORPH_DILATE, kernel2)


    debug_show_images([thresholdedImg,erosion])

    hollowPoints = _getHollowPoints(noteImg,space)
    notePoints = _getPoints(erosion)

    # Solid is 0 , Hollow is 1 (for third argument)
    for solidNote in notePoints:
        solidNote.append(0)

    for hollowNote in hollowPoints:
        hollowNote.append(1)

    bothNotesPoints = notePoints + hollowPoints

    linesDic = dict()
    linesDic = _linesNames(linesPos,space,thickness)

    notePoints = sorted(notePoints, key=lambda x: x[0])
    hollowPoints = sorted(hollowPoints, key=lambda x: x[0])
    bothNotesPoints = sorted(bothNotesPoints, key=lambda x: x[0])

    notesObj = []
    for note in bothNotesPoints:
        pointObj = []
        minimum = min(linesDic, key=lambda x:abs(x-note[1]))
        posName = linesDic[minimum]
        pointObj.append(note[0])
        pointObj.append(posName)
        pointObj.append(note[2])
        notesObj.append(pointObj)


    return notesObj

# Retruns dic of [lines y pos - names]
def _linesNames(linesPos,space,thickness):
    linesPos = list(linesPos)
    linesPos = sorted(linesPos,reverse=True)

    linesDic = dict()

    i = 0
    for pos in linesPos:
        linesDic[pos] = lineNames[i]
        linesDic[int(pos - ((space+thickness)/2))] = lineNames[i+1]
        i+=2
    return linesDic


# Returns set of points from countours in image
def _getPoints(img):
        points = []
        contours = find_contours(img, 0.8,fully_connected='low')

        for c in contours:
            xValues = np.round(c[:, 1]).astype(int)
            yValues = np.round(c[:, 0]).astype(int)

            point = []
            point.append( mean(xValues) )
            point.append( mean(yValues) )

            points.append(point)
                
        return points

def _getHollowPoints(img,space):
    kernelsq = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernelsq)
    
    kernelLine = cv2.getStructuringElement(cv2.MORPH_RECT,(7, 1))    

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernelLine)

    skeletonizedImage = np.uint8( skeletonize(closing/255) )

    h, w = skeletonizedImage.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    im_floodfill = skeletonizedImage.copy()
    cv2.floodFill(im_floodfill, mask, (0,0), 255);


    invertedFlood = 255 - im_floodfill

    kernelsq2 = np.ones((3,3),np.uint8)
    openinginvertedFlood = cv2.morphologyEx(invertedFlood, cv2.MORPH_OPEN, kernelsq2)

    kernelelipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(space*0.8),int(space*0.8)))    
   
    openinginvertedFlood = cv2.morphologyEx(openinginvertedFlood, cv2.MORPH_OPEN, kernelelipse)


    contours = find_contours(openinginvertedFlood, 0.8)
    points = []
    for c in contours:
        xValues = np.round(c[:, 1]).astype(int)
        yValues = np.round(c[:, 0]).astype(int)
        xdiff = (xValues.max() - xValues.min())
        ydiff = (yValues.max() - yValues.min())

        if not (xdiff > space*1.4 or ydiff > space*1.4):
            point = []
            point.append( mean(xValues) )
            point.append( mean(yValues) )
            points.append(point)

    return points

    







