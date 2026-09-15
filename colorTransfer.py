import numpy as np

'''Adjusts the selected source image’s colors to better match its target section.
It could apply a color overlay or transfer LAB color statistics while preserving
the original image’s details.'''

def adjustTileColor(tile,targetRegion,strength=0.35):
    if strength <= 0:
        return tile
    targetColor = np.mean(targetRegion,axis=(0,1))
    colorLayer = np.zeros(tile.shape)
    for c in range(3):
        colorLayer[:,:,c] = targetColor[c]
    mixed = tile.astype(float)*(1-strength) + colorLayer*strength
    mixed = np.clip(mixed,0,255)
    return mixed.astype(np.uint8)
