import os
import numpy as np
import struct
import tqdm
import glob
import json
from PIL import Image, ImageEnhance

filename = 'ETL1/ETL1C_*'
filenames = sorted(glob.glob(filename))

basedir = 'output'
dirname = 'ETL1'

with open('katakana_map.json', 'r') as f:
    conv_map = json.load(f)
    
conv_map = {int(k): v for k, v in conv_map.items()}

def read_ETL1(f):
    record_size = 2052
    s = f.read(record_size)
    if len(s) == 0:
        return None, None

    r = struct.unpack('>H2sH6BI4H4B4x2016s4x', s)
    iF = Image.frombytes('F', (64, 63), r[18], 'bit', 4)
    iP = iF.convert('RGBA')
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(16)
    
    return iE, r[3]

def read_file(filename):
    data = []
    idx = 0
    with open(filename, 'rb') as f:
        while True:
            if idx % 1000 == 0:
                print(idx)

            img, label = read_ETL1(f)
            if img is None:
                return data
            
            if label in conv_map:
                targetname = os.path.basename(filename) + '_{0:08d}.png'.format(idx)
                fullpath = os.path.join(basedir, dirname, child_dir, targetname)
                img.save(fullpath)
                data.append({'filename': os.path.join(dirname, child_dir, targetname), 'label': conv_map[label]})
            
            idx += 1

label_data = []
for f in filenames:
    child_dir = os.path.basename(f)
    os.makedirs(os.path.join(basedir, dirname, child_dir), exist_ok=True)    
    data = read_file(f)
    label_data.extend(data)
        
with open(os.path.join(basedir, 'ETL1.json'), 'w') as f:
    json.dump(label_data, f)
