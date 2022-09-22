import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))


""" fileopenbox opens the box to choose file
and help us store file path as string """
def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)
    

def cartoonify(ImagePath):
    org_image = cv2.imread(ImagePath)
    
    org_image = cv2.cvtColor(org_image, cv2.COLOR_BGR2RGB)

    # confirm that image is chosen
    if org_image is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(org_image, (900, 2000))

    #converting an image to grayscale
    grayScaleImage = cv2.cvtColor(org_image, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (900, 2000))

    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (900, 2000))

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 7)

    ReSized4 = cv2.resize(getEdge, (900, 2000))

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(org_image, 2, 200, 200)
    ReSized5 = cv2.resize(colorImage, (900, 2000))

    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (900, 2000))
    
    
    #plot the original and cartoonified image
     
    images=[ReSized1, ReSized6]
    titles=["original image","cartoon image"]
    fig, axes = plt.subplots(1,2, figsize=(12,12), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
         ax.imshow(images[i], cmap='gray')
         ax.set_title(titles[i])
         ax.axis('off')
    plt.show()

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)


top.mainloop()