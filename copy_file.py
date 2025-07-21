"""
@ Date: 2020/6/29
@ Author: Xiao Zhuo
@ Brief: Split CHAOS DataSet into my directory
@ Filename: split_dataset_1.py
"""
# -*- coding: utf-8 -*-
import os
import shutil as file
import pydicom
import os
import PIL as img
import numpy as np

dst_TrainData = "./data/train/Data"
dst_TrainGround = "./data/train/Ground"
dst_TestData = "./data/val/Data"
dst_TestGround = "./data/val/Ground"

def convert_from_dicom_to_png(img):
    low_window  = np.min(img)
    high_window = np.max(img)
    lungwin = np.array([low_window * 1.0, high_window * 1.0])
    newimg = (img - lungwin[0]) / (lungwin[1] - lungwin[0])  #归一化
    newimg = (newimg * 255).astype(np.uint8)  #扩展像素值到【0，255】
    return newimg

def save_dicom_as_png(orifile, savefile):
    dcm = pydicom.dcmread(orifile)

    image = dcm.pixel_array
    result = convert_from_dicom_to_png(image)
    img.Image.fromarray(result).resize((256, 256), resample=img.Image.Resampling.NEAREST).save(savefile)

def collect_T1_name(patient_dir):
    ground_paths = list()
    inphase_paths = list()

    t1_datadir = os.path.join(patient_dir, "T1DUAL")
    ground_dir = os.path.join(t1_datadir, "Ground")
    ground_names = os.listdir(ground_dir)
    nums_ground = len(ground_names)
    # 拼接Ground文件夹的文件，存入到ground_paths列表中
    for i in range(nums_ground):
        ground_paths.append(os.path.join(ground_dir, ground_names[i]))

    inphase_dir = os.path.join(t1_datadir, "DICOM_anon", "InPhase")
    inphase_names = os.listdir(inphase_dir)
    nums_inphase = len(inphase_names)

    # 拼接inphase文件夹的文件，存入到inphase_paths列表中
    for i in range(nums_inphase):
        inphase_paths.append(os.path.join(inphase_dir, inphase_names[i]))

    return ground_paths, inphase_paths

def each_(dst_Ground, dst_Data, sub_dir, ground_paths, inphase_paths):
    for num, path in enumerate(ground_paths):
        _, ext = os.path.splitext(path)
        # print(f"ext: {ext}, target: png")
        dst_groundpath = os.path.join(dst_Ground, "T1_Patient%s_No%d.png" % (sub_dir, num))
        image = img.Image.open(path)
        # print(f"Ground have shape: {(image.width, image.height)}")
        image.resize((256, 256)).save(dst_groundpath)

    for num, path in enumerate(inphase_paths):
        _, ext = os.path.splitext(path)
        # print(f"ext: {ext}, target: dcm")
        dst_inphasepath = os.path.join(dst_Data, "T1_Patient%s_No%d.png" % (sub_dir, num))
        save_dicom_as_png(path, dst_inphasepath)
    

def invoke():
    dataset_dir = os.path.join("Train_Sets", "MR")
    train_pct = 0.8
    test_pct = 0.2
    
    for root, dirs, files in os.walk(dataset_dir):
        dir_count = len(dirs)
        train_point = int(dir_count * train_pct)
        i = 0
        for sub_dir in dirs:  # sub_dir代表病人编号
            patient_dir = os.path.join(root, sub_dir)
            ground_paths, inphase_paths = collect_T1_name(patient_dir)
            if i < train_point:
                each_(dst_TrainGround, dst_TrainData, sub_dir, ground_paths, inphase_paths)
            else:
                each_(dst_TestGround, dst_TestData, sub_dir, ground_paths, inphase_paths)
            i += 1
        break


