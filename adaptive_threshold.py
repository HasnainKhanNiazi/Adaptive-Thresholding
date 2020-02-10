# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 19:32:57 2020

@author: Hasnain Khan
"""

import numpy as np
import cv2

def adaptive_threshold(src , dst , maxValue , adaptiveMethod , thresholdType , blockSize , C):
     
    # Getting number of rows and columns
    rows_num = src.shape[0]
    cols_num = src.shape[1]
        
    # Default threshold value
    threshold_value = 5.0
    
    # Following code is calculating mean for threshold value if user choose ADAPTIVE_THRESH_MEAN_C in the arguments
    p = 1
    if adaptiveMethod == 0:
        for i in src[0 , 0:blockSize]:
            for j in src[0:blockSize , 0]:
                p += 1
                threshold_value += src[i , j]

        threshold_value = threshold_value / p
    # Here the code ends for ADAPTIVE_THRESH_MEAN_C
    
    # Following code is used to change the grayscale image into integral image
    integral_image = np.zeros_like(src, dtype=np.uint32)
    for col in range(cols_num):
        for row in range(rows_num):
            integral_image[row,col] = src[0:row,0:col].sum() 
    # Here the code ends for Integral Image
    
    for col in range(cols_num):
        for row in range(rows_num):
            x0 = max(col - blockSize, 0)
            x1 = min(col + blockSize, cols_num-1)
            y0 = max(row - blockSize, 0)
            y1 = min(row + blockSize, rows_num-1)
            
            Count = (x1 - x0) * (y1 - y0)
            weighted_sum = integral_image[y0, x0] + integral_image[y1, x1] - integral_image[y0, x1] - integral_image[y1, x0] - C # Here C is the constant that usr give
            
            if src[row, col] * Count < weighted_sum * (100 - threshold_value) / 100:
                dst[row,col] = 0
            else:
                dst[row,col] = maxValue
                
    return dst # Returning Final image

if __name__ == '__main__':
    src = cv2.imread("img.jpeg" , 0)
    cols = src.shape[1]
    #blockSize = int(cols/8) # Using int because sometimes it was giving results in float as the columns can be Odd
    blockSize = 11
    dst = np.zeros_like(src)
    dst = adaptive_threshold(src , dst , 255 , 1  , "", blockSize , 2)
    cv2.imshow("Adaptive Threshold" , dst)
    cv2.imshow("Original Image" , src)