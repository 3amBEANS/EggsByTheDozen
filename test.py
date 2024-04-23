import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import cv2
from matplotlib.animation import FuncAnimation
import sys
from imageHelper import pad, pad_all
from detect import testProtocol, Parasite
import math

from ellipseDetector import ellipseDetector



ImageFiles = ["letter2.png", "unlabeled3.jpeg", "arrows1.jpeg"]
Images = []

for fileName in ImageFiles:
    testImg = cv2.imread(fileName)
    
    with open(fileName+".txt", "r") as annotationFile: 
        Parasites = []
        for line in annotationFile: 
            cX, cY, width, height = [float(s) for s in line.split()]
            topLeft = (int(cX-width/2), int(cY-height/2))
            bottomRight = (int(cX+width/2), int(cY+height/2))
            area = width*height
            testImg = cv2.rectangle(testImg, topLeft, bottomRight, (0,130,0), 2)
            cX+=64 #ACCOUNTS FOR PADDING
            cY+=64
            Parasites.append(Parasite(cX, cY, width, height, area))

    Images.append((testImg, fileName, Parasites))
    #cv2.imshow("TEST", testImg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def getTestImages(Images):
    print(len(Images))
    detected = []
    for (img,file,Parasites) in Images:
        im_t, observed = testProtocol(file, img, 210, Parasites)
        calculate_error(Parasites,observed)
        image_rgb = cv2.cvtColor(im_t, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        pil_image = pil_image.resize((533,400), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(image=pil_image)
        detected.append(tk_image)
    
    return detected

def calculate_squared_distance(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2

def calculate_error(expected, observed):
    exp_size = len(expected)
    ob_size = len(observed)
    miss_nums = []

    if ob_size > exp_size * 1.5:
        print("Too many detected parasites, increase binary threshold.")
        #return miss_nums
    elif ob_size < exp_size * 0.4:
        print("Not enough detected parasites, decrease binary threshold.")
        #return miss_nums

    duplicates = 0
    misses = 0
    total_error = 0
    undetected = 0

    detection_paired = [1] * ob_size

    for i in range(exp_size):
        max_dist = 901
        paired = False
        p1 = expected[i]
        for a in range(ob_size):
            p2 = observed[a]
            curr_dist = calculate_squared_distance(p1.centerX, p1.centerY, p2.centerX, p2.centerY)
            if curr_dist < 900:
                detection_paired[a] = 0
                real_dist = math.sqrt(curr_dist)

                if not paired:
                    paired = True
                    total_error += 0.1 * real_dist
                else:
                    duplicates += 1
                    #print(f"DUPLICATE parasite detection found at {p2.centerX},{p2.centerY}")
                    total_error += 0.5 * real_dist
                #print(f"\nOBSERVED PARASITE found at {p2.centerX},{p2.centerY}")
                #print(f"{real_dist} from expected parasite at {p1.centerX}, {p1.centerY}")

                if curr_dist < max_dist:
                    max_dist = curr_dist
        if max_dist == 901:
            #print(f"Undetected Barber Worm Egg!!! at {p1.centerX},{p1.centerY}")
            undetected += 1

    for i, num in enumerate(detection_paired):
        if num == 1:
            miss_nums.append(i)
        misses += num

    print("\n-----------PERFORMANCE-----------\n")
    print(f"Parasites Expected: {exp_size}")
    print(f"Parasites Detected: {ob_size}")
    print(f"Undetected Parasite Eggs: {undetected}")
    print(f"False Positive Eggs: {misses}\n")
    print("\n---------ERROR ANALYSIS----------\n")
    print(f"DistanceError: {total_error}")
    total_error += 5 * misses
    total_error += 20 * undetected
    print(f"Total Error Score: {total_error}\n")

    return miss_nums


root = tk.Tk()
testImgs = getTestImages(Images)
root.title("Image Grid")


label1 = tk.Label(root, image = testImgs[0])
label2 = tk.Label(root, image = testImgs[1])
label3 = tk.Label(root, image = testImgs[2])


label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=1, column=1)

root.geometry("1500x800")

root.mainloop()
        
    

    

def getBestEllipse(ellipseHelper, Contour):
    return ellipseHelper.fitEllipse_Polygon(Contour)

def getBinaryThreshold(gray_image, threshold):
    #OTSU METHOD
    return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    #TRADITIONAL METHOD
    #return cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)[1] 

def testParasites(fileName, thresh, outFile = "", saveImages = True):
    
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