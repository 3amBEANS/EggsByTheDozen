import cv2
from testHelper import getTestImagePacks, getTestImages, getTestErrors, getSingleTestError
import matplotlib.pyplot as plt
import numpy as np

def optimize(ImagePack):
    ThresVals = []
    TotalError = []
    UndetectedParasites = []
    print(type(ImagePack))
    
    Lowest_Error = (999,0)
    Least_Undetected = (999,0)
    
    for i in range(70, 245, 3):
        undetected,errorVal = getSingleTestError(ImagePack,i)
        ThresVals.append(i)
        TotalError.append(errorVal)
        UndetectedParasites.append(undetected)
        print(errorVal, undetected)
        
        if undetected < Least_Undetected[0]: Least_Undetected = (undetected, i)
        if errorVal < Lowest_Error[0]: Lowest_Error = (errorVal, i)
    
    print(Lowest_Error)
    print(Least_Undetected)
    
    
    return TotalError, UndetectedParasites
    
    plt.figure(figsize=(10, 6))
    plt.plot(ThresVals, TotalError, label='Total Error', marker='o')
    plt.plot(ThresVals, UndetectedParasites, label='Undetected Parasites', marker='s')
    plt.xlabel('Threshold Values')
    plt.ylabel('Count')
    plt.title('Error Analysis by Threshold')
    plt.legend()
    plt.grid(True)
    plt.show() 
    

def getDataForOptimizeAll(ImagePacks):
    ThresVals = range(70,245,3)
    TotalError1 = []
    TotalError2 = []
    TotalError3 = []
    Undetected1 = []
    Undetected2 = []
    Undetected3 = []
    
    TotalError1, Undetected1 = optimize(ImagePacks[0])
    TotalError2, Undetected2 = optimize(ImagePacks[1])
    TotalError3, Undetected3 = optimize(ImagePacks[2])
    
    plt.figure(figsize=(10, 6))
    plt.plot(ThresVals, TotalError1, label='Error (Easy Img)', marker='o')
    plt.plot(ThresVals, TotalError2, label='Error (Medium Img)', marker = '^', color='magenta')
    plt.plot(ThresVals, TotalError3, label='Error (Hard Img)', marker = 'D', color='cyan')
    plt.plot(ThresVals, Undetected1, label='Undetected (Easy)', marker='s')
    plt.plot(ThresVals, Undetected2, label = 'Undetected (Med)', marker = 'p', color = 'magenta')
    plt.plot(ThresVals, Undetected3, label='Undetected (Hard)', marker = '*', color='cyan')
    plt.xlabel('Threshold Values')
    plt.ylabel('Count')
    plt.title('Error Analysis by Threshold')
    plt.legend()
    plt.grid(True)
    plt.show() 
    
    
    
    
    
imagePacks = getTestImagePacks()
print(type(imagePacks))
optimize(imagePacks[2])