from PIL import Image, ImageOps
import numpy as np
import cv2
from tqdm import tqdm

'''The main program. It reads the target image and source-image folder, divides the target into cells, 
calls the other files to find matching tiles, builds the final mosaic, and saves it.'''
Mainimage=1



