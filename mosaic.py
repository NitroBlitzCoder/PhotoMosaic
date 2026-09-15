import os
import numpy as np
import cv2
from tqdm import tqdm
from imageUtil import *
from matcher import findBestMatch
from colorTransfer import adjustTileColor

'''The main program. It reads the target image and source-image folder, divides the target into cells,
calls the other files to find matching tiles, builds the final mosaic, and saves it.'''

colorStrength= 0.35

gotTkinter = True
try:
    import tkinter
    from tkinter import filedialog
except:
    gotTkinter = False

def prepTiles(folder):
    imgCollection = loadImageCollection(folder)
    imgCollection = cropCollectionImg(imgCollection)
    tileList=[]
    for img in imgCollection:
        # work out the average colour ONCE here, doing it inside the big loop was really slow
        tileList.append({"image":img,"avgColor":avgLabColor(img),"uses":0})
    return tileList

def buildMosaic(img,tileList):
    img = cropTargetToGrid(img)
    height, width = img.shape[:2]
    NumTileRow,NumTileCol,totalTiles = tileAmountReq(img)

    print("target size: "+str(width)+" x "+str(height))
    print("tile grid: "+str(NumTileRow)+" x "+str(NumTileCol))
    print("total number of images needed: "+str(totalTiles))

    mosaic = np.zeros_like(img)
    for row in tqdm(range(NumTileCol),desc="building mosaic"):
        for col in range(NumTileRow):
            x = col*tilePixelSize
            y = row*tilePixelSize
            region = img[y:y+tilePixelSize, x:x+tilePixelSize]

            targetColor = avgLabColor(region)
            tile = findBestMatch(targetColor,tileList)
            newTile = adjustTileColor(tile["image"],region,colorStrength)

            mosaic[y:y+tilePixelSize, x:x+tilePixelSize] = newTile
    return mosaic

def askWithWindow():
    window = tkinter.Tk()
    window.withdraw()
    targetPath = filedialog.askopenfilename(title="pick the target image",
                                            filetypes=[("images","*.png *.jpg *.jpeg *.webp *.bmp")])
    tileFolder = filedialog.askdirectory(title="pick the folder with the source images")
    window.destroy()
    return targetPath,tileFolder

def askWithTyping():
    targetPath = input("Import the target image by entering its path: ").strip().strip("\"'")
    tileFolder = input("Enter the folder containing the source images: ").strip().strip("\"'")
    return targetPath,tileFolder

def main():
    useWindow = "n"
    if gotTkinter:
        useWindow = input("use the file picker window? (y/n): ").strip().lower()
    else:
        print("tkinter is not installed so you have to type the paths")

    if useWindow == "y":
        targetPath,tileFolder = askWithWindow()
    else:
        targetPath,tileFolder = askWithTyping()

    # if you just press enter / close the picker it uses the folders inside the project
    if targetPath == "":
        targetPath = "./images/target.png"
    if tileFolder == "":
        tileFolder = "./images/tiles/"

    if os.path.isfile(targetPath) == False:
        print("the target image was not found")
        return
    if os.path.isdir(tileFolder) == False:
        print("the source image folder was not found")
        return

    img = loadTargetImage(targetPath)
    if img is None:
        return

    tileList = prepTiles(tileFolder)
    if len(tileList) == 0:
        print("no usable source images were found")
        return
    print("loaded "+str(len(tileList))+" source images")

    mosaic = buildMosaic(img,tileList)

    os.makedirs("output",exist_ok=True)
    outPath = "output/mosaic.png"
    saved = cv2.imwrite(outPath,mosaic)
    if saved:
        print("mosaic saved to "+outPath)
    else:
        print("the mosaic could not be saved")

main()
