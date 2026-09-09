import os
import cv2
import numpy as np

'''Handles general image operations, such as loading files, fixing image orientation, cropping images
to the correct aspect ratio, resizing them, converting colors, and calculating average colors'''
cropRatio= 4

def loadTargetImage():
    img = cv2.imread("./images/target.png")
    return img
def tileAmountReq(img):
    width, height = img.shape[:2]
    
    return ()
def loadImageCollection():
    list = os.listdir("./images/")
    return list
def cropImage(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


