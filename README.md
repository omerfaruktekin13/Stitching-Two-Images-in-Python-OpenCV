# Stitching Two Images in Python OpenCV

## Project Media
![Dxxxxx](https://github.com/omerfaruktekin13/Stitching-Two-Images-in-Python-OpenCV/blob/main/Media/e.jpg "Deneme ")
|:--:|
| *Final Result* |
![Dxxxxx](https://github.com/omerfaruktekin13/Stitching-Two-Images-in-Python-OpenCV/blob/main/Media/a.jpg "Deneme ")
| *Left Part of the Image (Gondor from LOTR)* |
![Dxxxxx](https://github.com/omerfaruktekin13/Stitching-Two-Images-in-Python-OpenCV/blob/main/Media/b.png "Deneme ")
| *Right Part of the Image (Rohan from LOTR)* |
![Dxxxxx](https://github.com/omerfaruktekin13/Stitching-Two-Images-in-Python-OpenCV/blob/main/Media/c.jpg "Deneme ")
| *Calculated Stitch Path* |
![Dxxxxx](https://github.com/omerfaruktekin13/Stitching-Two-Images-in-Python-OpenCV/blob/main/Media/d.jpg "Deneme ")
| *Stitched Image Before Filters* |

## Description
I want to share an algorithm: "Stitching Images with Calculation of Squared Difference of the Pixels." Briefly, the methodology calculates the smallest squared difference of the overlapped pixels in grayscale and creates a path in the way you choose. I used Minas Tirith (Gondor Castle) and Rohan images to test my algorithm which is written in Python and OpenCV. The second and third images represent the original images from the Lord of the Rings movies. The fourth one depicts the calculated seam path by the algorithm in grayscale and the last image is the result in an RGB color map. I added median blur to decrease the sharp-cutting places of the images to the final result and show it in grayscale (first image). In the end, we have a perfect image that Gandalf riding his Shadowfax between two mankind towns in Middle Earth. 

## Tools and Languages
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<p> * Python3 </p>
<p> * OpenCV </p>
<p> * Jupyter Notebook or any suitable integrated development environment (IDE) </p>

## Installation
> 1. Download Stitching.py file
> 2. Use your own images and change the image path in the code
> 3. Try other overlapping sizes to observe changes in your combined image.

## Open to Development
Please share your comments and ideas about the project with me. Thank you for your time.
