__author__ = "Ömer Faruk Tekin"
__version__ = "1.0.1"
__maintainer__ = "Ömer Faruk Tekin"
__email__ = "omertekin13@gmail.com"

import numpy as np
import matplotlib.pyplot as plt
%config InlineBackend.figure_formats = 'retina'
from matplotlib import rcParams
import cv2
rcParams['figure.figsize']=[20,28]

#float64touint8_image function converts float64 values to uint8 integers of image.
def float64touint8_image(float_image):
    return np.uint8(np.clip(float_image.round(),0,255))

#PNG_to_RGB function transforms PNG format image to RGB format
def PNG_to_RGB(PNG_Image):
    PNG_Image = PNG_Image[:,:,:3]
    PNG_Image = PNG_Image * 255
    PNG_Image = float64touint8_image(PNG_Image)
    return PNG_Image

#dwnScale function is created in the purpose of downscaling of the image according to scale rate number. Return value array of uint8 values.
def downScale(image,scale_rate)
    r,c,ch = np.shape(image)
    r = int(scale_rate * int(r/scale_rate))
    c = int(scale_rate * int(c/scale_rate))
    image = image[:r,:c]
    r = int(r/scale_rate)
    c = int(c/scale_rate)
    result = np.zeros((r,c,3),np.uint8)
    for i in range(r):
        for j in range(c):
            result[i,j,0] = int(np.average(image[i*scale_rate:i*scale_rate+scale_rate,j*scale_rate:j*scale_rate+scale_rate,0]))
            result[i,j,1] = int(np.average(image[i*scale_rate:i*scale_rate+scale_rate,j*scale_rate:j*scale_rate+scale_rate,1]))
            result[i,j,2] = int(np.average(image[i*scale_rate:i*scale_rate+scale_rate,j*scale_rate:j*scale_rate+scale_rate,2]))  
    return result

#get_seam function gets minimum values of the difference values which calculated with squared difference of pixels. Returns the best path for stitching two images.
def get_Seam(dif):
    height, width = dif.shape
    cost = dif.copy()
    seam = np.zeros((height))
    for j in range(height):
        if(j == 0):
            continue
        for i in range(width):
            if(i == 0):
                cost[j,i] += np.amin((cost[j-1,i],cost[j-1,i+1]))
                continue
            if(i == width-1):
                cost[j,i] += np.amin((cost[j-1,i-1],cost[j-1,i]))
                continue
            cost[j,i] += np.amin((cost[j-1,i-1],cost[j-1,i],cost[j-1,i+1]))
    for j in reversed(range(height)):
        if(j == height-1):
            seam[j] = np.argmin((cost[j]))
            continue
        down = int(seam[j+1])
        if(down == 0):
            seam[j] = (down) + np.argmin((cost[j,down],cost[j,down+1]))
            continue
        if(down == width-1):
            seam[j] = (down-1) + np.argmin((cost[j,down-1],cost[j,down]))
            continue
        seam[j] = (down-1) + np.argmin((cost[j,down-1],cost[j,down],cost[j,down+1]))
    return seam

#Reading two different images
img1 = PNG_to_RGB(plt.imread('gondor.png')) #PNG format to RGB
img2 = downScale(plt.imread('rohan.jpg'),2) #Size of the second image is much bigger than first one. Therefore, I downscaled it.

#Brightness & Contrast
adj_1 = cv2.convertScaleAbs(img1, alpha=0.7, beta=1) #I adjusted brightness and contrast value of first image to equalize sky colors
adj_2=cv2.convertScaleAbs(img2, alpha=0.7, beta=1) #I adjusted brightness and contrast value of second image to equalize sky colors
imgL=adj_1[:427,:1016] #Matching the size of the images
imgR=adj_2[:427,:1016] #Matching the size of the images
imgRr=np.fliplr(imgR) #Vertically flipping for making castles closer to each other

overlap = 570 #Over lapping pixel value
heightL, widthL, temp = imgL.shape
heightR, widthR, temp = imgRr.shape
stitch = np.concatenate((imgL[:,:widthL-int(overlap/2)], imgRr[:,int(overlap/2):]), axis=1) #Stitching overlapped images
plt.imshow(stitch)

#Showing overlapped parts of the two images with subplot
tinyL = imgL[:,widthL-overlap:]
tinyR = imgRr[:,:overlap]
fig, ax = plt.subplots(1,2)
ax[0].imshow(tinyL)
ax[1].imshow(tinyR)

# RGB to Gray Scale transforming
tinyL_g = np.dot(tinyL, [0.299,0.587,0.114])
tinyR_g = np.dot(tinyR, [0.299,0.587,0.114])

#Squared Difference calculation to use in seam (path) creation
diff = cv2.subtract(tinyL_g,tinyR_g)
diff = cv2.multiply(diff,diff)

#Display the squared difference in gray scale
plt.imshow(diff,cmap='gray')
np.shape(diff)

#Creation of the seam. The function gets lowest values of the pixels and its neighborhoods which means the blackest pixels.
my_seam = get_Seam(diff)

#Depicting the path in white pixels
diff_seam = diff.copy()
height, width = diff.shape
for i in range(height):
    diff_seam[i,int(my_seam[i])] = 255 * 255 #White pixels
plt.imshow(diff_seam,cmap='gray')

#This parts creates middle section. Seam determines which pixels should be taken from left overlapped and right overlapped parts. Seam shown in blue.
middle = tinyL.copy() 
for i in range(height):   
    j = int(my_seam[i])
    while j < width:
        middle[i,j] = tinyR[i,j]
        j += 1
middle_marked = middle.copy()
for i in range(height):
    middle_marked[i,int(my_seam[i])] = np.array((0,255,0))
plt.imshow(middle_marked,cmap='gray')

#I added median blur filter to decrease sharp passes of the sky colors then concatenate them.
tr=cv2.medianBlur(middle_marked,3)
cut_stitch = np.concatenate((imgL[:,:widthL-overlap], tr), axis=1)
cut_stitch = np.concatenate((cut_stitch, imgRr[:,overlap:]), axis=1)
plt.imshow(cut_stitch)

#Last section shows the image in gray scale.
cut_stitch = np.concatenate((imgL[:,:widthL-overlap], tr), axis=1)
cut_stitch = np.concatenate((cut_stitch, imgRr[:,overlap:]), axis=1)
z=np.dot(cut_stitch, [0.299,0.587,0.114])
plt.imshow(z,cmap='gray')