import numpy as np

'''Decides which source image best matches each section of the target image.
It compares colors and applies rules to limit repeated images
or prevent identical neighboring tiles.'''

reusePenalty= 15

def colorDistance(c1,c2):
    c1=np.array(c1).astype(float)
    c2=np.array(c2).astype(float)
    dist = np.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)
    return dist

def findBestMatch(targetColor,tileList):
    bestTile = None
    bestScore = float("inf")
    for tile in tileList:
        score = colorDistance(targetColor,tile["avgColor"])
        score = score + tile["uses"]*reusePenalty
        if score < bestScore:
            bestScore = score
            bestTile = tile
    bestTile["uses"] = bestTile["uses"] + 1
    return bestTile
