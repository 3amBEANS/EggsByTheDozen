import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import cv2
from matplotlib.animation import FuncAnimation
import sys

ImageFiles = ["letter2.png", "unlabeled3.jpeg", "arrows1.jpeg"]
Images = []

for fileName in ImageFiles:
    testImg = cv2.imread(fileName)
    
    with open(fileName+".txt", "r") as annotationFile: 
        for line in annotationFile: 
            cX, cY, width, height = line.split()
            topLeft = (cX-width/2, cY-height/2)
            bottomRight = (cX+width/2, cY+height/2)
            testImg = cv2.rectangle(testImg, topLeft, bottomRight, (0,200,0), 3)

    Images.append(testImg, fileName)
    cv2.imshow("TEST", testImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
