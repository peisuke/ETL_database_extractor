import os
import numpy as np
import struct
import tqdm
import glob
import json
from PIL import Image, ImageEnhance

filename = 'ETL8B/ETL8B2C*'
filenames = sorted(glob.glob(filename))

basedir = 'output'
dirname = 'ETL8'

def read_ETL8B(f):
    record_size = 512
    s = f.read(record_size)
    if len(s) == 0:
        return None, None
    r = struct.unpack('>2H4s504s', s)
    iF = Image.frombytes('1', (64, 63), r[3], 'raw')
    iP = iF.convert('RGBA')
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(64)
    return iE, r[1]

def read_file(filename):
    data = []
    with open(filename, 'rb') as f:
        while True:
            img, label = read_ETL8B(f)
            if img is None:
                return data
            data.append({'image': img, 'label': label})
            
label_data = []
for f in filenames:
    child_dir = os.path.basename(f)
    os.makedirs(os.path.join(basedir, dirname, child_dir), exist_ok=True)
    
    data = read_file(f)
    for i, d in enumerate(tqdm.tqdm(data)):
        filename = os.path.basename(f) + '_{0:08d}.png'.format(i)
        fullpath = os.path.join(basedir, dirname, child_dir, filename)
        d['image'].save(fullpath)
        label_data.append({'filename': os.path.join(dirname, child_dir, filename), 'label': d['label']})
        
with open(os.path.join(basedir, 'ETL8B.json'), 'w') as f:
    json.dump(label_data, f)