import os
import cv2
import numpy as np

'''Handles general image operations, such as loading files, fixing image orientation, cropping images
to the correct aspect ratio, resizing them, converting colors, and calculating average colors'''
tilePixelSize= 40
allowedTypes= [".png",".jpg",".jpeg",".webp",".bmp"]

def loadTargetImage(path="./images/target.png"):
    img = cv2.imread(path)
    if img is None:
        print("could not open the target image -> "+path)
    return img

def tileAmountReq(img):
    height, width = img.shape[:2]
    NumTileRow=width//tilePixelSize
    NumTileCol=height//tilePixelSize
    totalTiles=NumTileRow*NumTileCol
    return NumTileRow,NumTileCol,totalTiles

def loadImageCollection(folder="./images/tiles/"):
    CollectionImg = []
    fileNames = os.listdir(folder)
    fileNames.sort()
    for name in fileNames:
        isImage = False
        for ext in allowedTypes:
            if name.lower().endswith(ext):
                isImage = True
        if isImage == False:
            continue
        img = cv2.imread(os.path.join(folder,name))
        if img is None:
            print("skipping "+name+" (cv2 couldnt read it)")
            continue
        CollectionImg.append(img)
    return CollectionImg

def cropSquare(img):
    img_h, img_w = img.shape[:2]
    size = min(img_h,img_w)
    x = int((img_w - size) / 2)
    y = int((img_h - size) / 2)
    crop_img = img[y:y + size, x:x + size]
    return crop_img

def cropCollectionImg(imgList):
    newList=[]
    for img in imgList:
        crop_img = cropSquare(img)
        small = cv2.resize(crop_img,(tilePixelSize,tilePixelSize),interpolation=cv2.INTER_AREA)
        newList.append(small)
    return newList

def cropTargetToGrid(img):
    height, width = img.shape[:2]
    NumTileRow,NumTileCol,totalTiles = tileAmountReq(img)
    useW = NumTileRow*tilePixelSize
    useH = NumTileCol*tilePixelSize
    x = (width - useW)//2
    y = (height - useH)//2
    return img[y:y+useH, x:x+useW]

def avgLabColor(img):
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
    return np.mean(lab,axis=(0,1))
