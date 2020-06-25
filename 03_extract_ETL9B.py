import os
import numpy as np
import struct
import tqdm
import glob
import json
from PIL import Image, ImageEnhance

filename = 'ETL9B/ETL9B_*'
filenames = sorted(glob.glob(filename))

basedir = 'output'
dirname = 'ETL9'

def read_ETL9B(f):
    record_size = 576
    s = f.read(record_size)
    if len(s) == 0:
        return None, None
    r = struct.unpack('>2H4s504s64x', s)
    iF = Image.frombytes('1', (64, 63), r[3], 'raw')
    iP = iF.convert('RGBA')
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(64)
    return iE, r[1]

def read_file(filename):
    data = []
    idx = 0
    with open(filename, 'rb') as f:
        while True:
            if idx % 1000 == 0:
                print(idx)
            img, label = read_ETL9B(f)
            if img is None:
                return data
            
            targetname = os.path.basename(filename) + '_{0:08d}.png'.format(idx)
            fullpath = os.path.join(basedir, dirname, child_dir, targetname)
            img.save(fullpath)
            data.append({'filename': os.path.join(dirname, child_dir, targetname), 'label': label})
            
            idx += 1
            
label_data = []
for f in filenames:
    child_dir = os.path.basename(f)
    os.makedirs(os.path.join(basedir, dirname, child_dir), exist_ok=True)    
    data = read_file(f)
    label_data.extend(data)
    
with open(os.path.join(basedir, 'ETL9B.json'), 'w') as f:
    json.dump(label_data, f)