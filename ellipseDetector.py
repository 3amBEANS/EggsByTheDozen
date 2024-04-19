import numpy as np
import cv2
import math 
import random

class ellipseDetector:
    
    def __init__(self):
        pass
    
    def distPoint_Ellipse(self, BoundingRectangle, Point):
        (cxE, cyE), (WidthE, HeightE), rotE = BoundingRectangle
        ptX, ptY = Point[0], Point[1] * -1
        radX, radY = WidthE / 2, HeightE / 2
        angleToCenterE = math.atan2(ptY - cyE * -1, ptX - cxE)
        nearestEX, nearestEY = cxE + radX * math.cos(angleToCenterE), cyE * -1 + radY * math.sin(angleToCenterE)
        return (ptX - nearestEX) ** 2 + (ptY * -1 - nearestEY * -1) ** 2, (nearestEX, -1 * nearestEY)
    
    def fitEllipse_RANSAC(self, Contour):
        if len(Contour) < 5:
            print("Contour Too Small")
            
        
        maxInliers, bestFit = 0, ((0,0),(0,0),0)
        
        MaxIterations = int(len(Contour)/3)
        for i in range(MaxIterations):
            sample = np.array([Contour[i][0] for i in random.sample(range(len(Contour)),5)])
            potentFit = cv2.fitEllipseDirect(sample)
            numInliers = 0
            for pt in Contour:
                pt = tuple(pt[0])
                d = self.distPoint_Ellipse(potentFit, pt)[0]
                if d < 15:
                    numInliers += 1
            if numInliers > maxInliers:
                maxInliers = numInliers
                bestFit = potentFit
        
        return bestFit