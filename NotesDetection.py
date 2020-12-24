import skimage
from commonfunctions import *
import numpy as np
import os
import cv2
from skimage.transform import hough_line, hough_line_peaks
import itertools 
from skimage.measure import find_contours
from statistics import mean

lineNames = ['c','d','e','f','g','a','b','c2','d2','e2','f2','g2','a2','b2']

# NOTE: Should get rid of cliff to avoid false notes
# TODO: find a way to detect hollow notes

# Returns the coordinates of note and array of the note names
def NotesPositions(thresholdedImg,linesPos,space):
    invertedImg = 1 - thresholdedImg
    invertedImg = np.uint8(invertedImg)

    # Creating circle SE with size of the note circle
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(space*0.9),int(space*0.9)))    
    erosion = cv2.erode(invertedImg,kernel,iterations = 1)
    
    show_images([thresholdedImg,erosion])

    notePoints = _getPoints(erosion)
    linesDic = dict()
    linesDic = _linesNames(linesPos,space)

    notePoints = sorted(notePoints, key=lambda x: x[0])

    notesNames = []
    for point in notePoints:
       minimum = min(linesDic, key=lambda x:abs(x-point[1]))
       notesNames.append(linesDic[minimum])

    return notePoints,notesNames

# Retruns dic of [lines y pos - names]
def _linesNames(linesPos,space):
    linesPos = list(linesPos)
    linesPos = sorted(linesPos,reverse=True)
    
    lowerExtraLine = linesPos[0] + space
    upperExtraLine = linesPos[-1] - space

    linesPos.insert(0,lowerExtraLine)
    linesPos.append(upperExtraLine)

    linesDic = dict()

    i = 0
    for pos in linesPos:
        linesDic[pos] = lineNames[i]
        linesDic[int(pos - (space/2))] = lineNames[i+1]
        i+=2
    return linesDic


# Returns set of points from countours in image
def _getPoints(img):
        points = []
        contours = find_contours(img, 0.8)
        for c in contours:
            xValues = np.round(c[:, 1]).astype(int)
            yValues = np.round(c[:, 0]).astype(int)

            point = []
            point.append( mean(xValues) )
            point.append( mean(yValues) )

            points.append(point)
                
        return points
