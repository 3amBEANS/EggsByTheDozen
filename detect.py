import cv2, sys
import numpy as np
from imageHelper import pad, pad_all

from ellipseDetector import ellipseDetector

class Parasite:
    def __init__(self, centerX=0.0, centerY=0.0, width=0.0, height=0.0, estArea=0.0):
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.estArea = estArea

def getBestEllipse(ellipseHelper, Contour):
    return ellipseHelper.fitEllipse_Polygon(Contour)

def getBinaryThreshold(gray_image, threshold):
    #OTSU METHOD
    return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    #TRADITIONAL METHOD
    #return cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)[1] 

def detectParasites(fileName, thresh, outFile = "", saveImages = True):
    
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    
    binary = getBinaryThreshold(im_gray, thresh)

    contourImage = cv2.imread(fileName)
    ellipseImage = cv2.imread(fileName)
    
    #print(binary.shape)
    #print(contourImage.shape)
    #print(contourImage)
    
    im_gray, binary, contourImage, ellipseImage = pad_all([im_gray, binary, contourImage, ellipseImage])
    
    if (saveImages): cv2.imwrite("imThresh.png", binary)
    
    #print(binary)
    #print(binary.shape, contourImage.shape)
    
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    #Filter Contour Areas
    
    cv2.drawContours(contourImage, contours, -1, (0,0,0), 3)
    if (saveImages): cv2.imwrite("imContours.png", contourImage);
    
    #print("savedContours");
    #print(len(contours));
    
    num_eggs = 0
    
    ellipseHelper = ellipseDetector()
    for contour in contours: 
        if len(contour)>=5:
            bestEllipse = getBestEllipse(ellipseHelper, contour)
            if not bestEllipse == None: 
                cv2.ellipse(ellipseImage, bestEllipse, (0,0,255), 3)
                num_eggs+=1
    
    if (saveImages):
        if outFile == "":
            cv2.imwrite("imParasites.png", ellipseImage);
        else: 
            cv2.imwrite(outFile, ellipseImage);
        
    
        
    print("Seen: %d" % num_eggs)
    print("Eggs Per Gram: %d" % (num_eggs * 50))
    
    
def testProtocol(fileName, img, thresh, Parasites):
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    
    greenMat = img.copy()
    
    binary = getBinaryThreshold(im_gray, thresh)
    
    im_gray, binary, greenMat = pad_all([im_gray, binary, greenMat])
    
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    num_eggs = 0
    
    ellipseHelper = ellipseDetector()
    observedParasites = []
    for contour in contours: 
        if len(contour)>=5:
            bestEllipse = getBestEllipse(ellipseHelper, contour)
            if not bestEllipse == None: 
                cv2.ellipse(greenMat, bestEllipse, (0,0,255), 3)
                (cx,cy),(ma,ml),a = bestEllipse
                observedParasites.append(Parasite(cx,cy,ma,ml,ma*ml))
                num_eggs+=1
    
    
    
    #cv2.imshow("TEST", greenMat)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return greenMat, observedParasites