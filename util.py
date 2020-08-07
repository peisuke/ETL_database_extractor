import os
import random
import json
import tqdm
import numpy as np
import mojimoji
import ipyplot
import glob
import cv2
import unicodedata
from collections import defaultdict
import re
from PIL import Image

def check_image(img):
    img = np.array(img)

    img = denoiser(img)
    
    # ノイズが多ければ除外
    float_img = (img // 255).astype(np.float)
    val = np.abs(float_img[1:] - float_img[:-1]).sum()
    
    dilated_img = cv2.dilate(img, np.array([[1,1,1],[1,1,1],[1,1,1]], dtype=np.uint8))

    # 文字が中心にければ除外
    simg = img.sum(axis=0)
    center = np.sum(simg[len(simg)//2-8:len(simg)//2+8])
    edge = np.sum(simg[:8] + simg[-8:])    
    
    if val > 300: # ごま塩ノイズ多めなら除外
        return False
    elif np.count_nonzero(dilated_img) > img.size // 4: #画面の1/4がノイズの場合は除外
        return False
    elif center <= edge:
        return False
    else:
         return True
        
def check_ok(img):
    return True

def denoiser(img, nb_foreground=200, bins=20):
    values = sorted(img.reshape(-1))
    base_val = values[len(values) // 2]
    img = np.clip(img, base_val, 255) - base_val
    
    v, k = np.histogram(img.reshape(-1), bins=bins)
    thresh1 = k[np.argmax(v)]
    idx = np.nonzero(np.cumsum(v[::-1]) > nb_foreground)[0][0]
    thresh2 = k[-idx]

    edge = cv2.Canny(img, thresh1, thresh2)

    mask = cv2.dilate(edge, np.ones((3, 3), np.int))
    mask = cv2.dilate(mask, np.ones((5, 5), np.int))
    mask = cv2.dilate(mask, np.ones((5, 5), np.int))
    mask = cv2.erode(mask, np.ones((5, 5), np.int))
    
    idx = np.where(mask==0)

    _, image = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image[idx] = 0
    return image

def simple_denoiser(img, nb_foreground=200, bins=20):
    _, image = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return image

def remove_point(img):
    nLabels, labelImages = cv2.connectedComponents(img)

    for lbl in range(1, nLabels):
        ys, xs = np.where(labelImages == lbl)
        if len(ys) < 5:
            img[ys,xs] = 0
    return img

def remove_edge(img, pos=2):
    nLabels, labelImages = cv2.connectedComponents(img)

    for lbl in range(1, nLabels):
        ys, xs = np.where(labelImages == lbl)
        center = np.median(xs), np.median(ys)

        if xs.min() < pos and center[0] < pos*2:
            img[ys,xs] = 0
        if ys.min() < pos and center[1] < pos*2:
            img[ys,xs] = 0
        if xs.max() >= labelImages.shape[1] - pos and center[0] >= labelImages.shape[1] - pos*2:
            img[ys,xs] = 0
        if ys.max() >= labelImages.shape[0] - pos and center[1] >= labelImages.shape[0] - pos*2:
            img[ys,xs] = 0
    return img

def clip(img):
    x, y, w, h = cv2.boundingRect(img) 
    img = img[y:y+h, x:x+w]
    img = np.pad(img, ((5, 5), (3, 3)), mode='constant', constant_values=0)
    if h < w:
        p = (w - h) // 2
        img = np.pad(img, ((p, p), (0, 0)), mode='constant', constant_values=0)
    return img

def denoise_etl1(img):
    img = np.array(img)
    img = denoiser(img)
    img = remove_point(img)
    img = remove_edge(img)
    img = clip(img)
    return Image.fromarray(img)

def denoise_etl2(img):
    img = np.array(img)
    img = simple_denoiser(img)
    img = remove_point(img)
    #img = remove_edge(img, pos=10)
    img = clip(img)
    return Image.fromarray(img)

def denoise_etl9G(img):
    img = np.array(img)
    img = simple_denoiser(img)
    img = remove_point(img)
    img = remove_edge(img, pos=10)
    img = clip(img)
    return Image.fromarray(img)