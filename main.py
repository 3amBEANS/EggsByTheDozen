import cv2, sys
import numpy as np

from ellipseDetector import ellipseDetector


def main():
    saveImages = True
    displayImages = True
    
    fileName = "unlabaled3.jpg"
    thresh = 210
    
    for i in range(0, len(sys.argv)):
        if (sys.argv[i] == "-f"):
            fileName = sys.argv[i+1]
        elif (sys.argv[i] == "-t"):
            thresh = int(sys.argv[i+1])
    
    im_gray = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    binary = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1] 
    
    #Otsu Test Can Be Implemented to Guess Threshold Values#
    #im_bw = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    if (saveImages): cv2.imwrite("imThresh.png", binary)
    
    contourImage = cv2.imread(fileName)
    
    
    
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    cv2.drawContours(contourImage, contours, -1, (0,0,0), 3)
    if (saveImages): cv2.imwrite("imContours.png", contourImage);
    
    ellipseImage = cv2.imread(fileName)
    
    #RANSAC Approach O(n) Ellipse Fitting per Contour
    ellipseHelper = ellipseDetector()
    for contour in contours: 
        if len(contour)>=5:
            bestEllipse = ellipseHelper.fitEllipse_RANSAC(contour)
            cv2.ellipse(ellipseImage, bestEllipse, (255,0,255), 1)
    
    cv2.imwrite("imParasites.png", ellipseImage);
    
    
    
if __name__=="__main__":
    main()