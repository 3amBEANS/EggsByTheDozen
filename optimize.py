import cv2
from testHelper import getTestImagePacks, getTestImages
import matplotlib.pyplot as plt
import numpy as np

def optimize(ImagePack):
    ThresVals = []
    TotalError = []
    MissedParasites = []
    
    img,file,Parasites = ImagePack
    for i in range(70, 245, 3):
        errorVal, missed = getTestImages(ImagePack)[1]
        ThresVals.append(i)
        TotalError.append(errorVal)
        MissedParasites.append(missed)
    
    plt.figure(figsize=(10, 6))
    plt.plot(ThresVals, TotalError, label='Total Error', marker='o')
    plt.plot(ThresVals, MissedParasites, label='Missed Parasites', marker='s')
    plt.xlabel('Threshold Values')
    plt.ylabel('Count')
    plt.title('Error Analysis by Threshold')
    plt.legend()
    plt.grid(True)
    plt.show()
    
imagePacks = getTestImagePacks()
optimize(imagePacks[0])