"""
# @file name  : conver2png.py
# @author     : Peter
# @date       : 2020-07-01
# @brief      : 将dicom格式转换成png格式
"""
import pydicom
import os
import matplotlib.pyplot as plt
import skimage
import PIL as img
import numpy as np

path_1 = "./data/val/Data"
path_2 = "./data/train/Data"

def convert_from_dicom_to_png(img):
    low_window  = np.min(img)
    high_window = np.max(img)
    lungwin = np.array([low_window * 1.0, high_window * 1.0])
    newimg = (img - lungwin[0]) / (lungwin[1] - lungwin[0])  #归一化
    newimg = (newimg * 255).astype(np.uint8)  #扩展像素值到【0，255】
    return newimg

def dicom_2png(orifile, savefile, w, h):
    print(f"Read file at{orifile}")
    dcm = pydicom.dcmread(orifile)

    image = dcm.pixel_array
    result = convert_from_dicom_to_png(image)
    img.Image.fromarray(result).save(savefile)

def invoke():
    names = os.listdir(path_1)
    for i in range(len(names)):
        dicom_path = os.path.join(path_1, names[i])
        png_name = os.path.splitext(names[i])[0]
        dst_path = os.path.join('./data/val/Data_8bit', (png_name + '.png'))
        dicom_2png(dicom_path, dst_path, 256, 256)
    
    names = os.listdir(path_2)
    for i in range(len(names)):
        dicom_path = os.path.join(path_2, names[i])
        png_name = os.path.splitext(names[i])[0]
        dst_path = os.path.join('./data/train/Data_8bit', (png_name + '.png'))
        dicom_2png(dicom_path, dst_path, 256, 256)
