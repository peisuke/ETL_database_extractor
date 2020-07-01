import argparse
import os
import numpy as np
import struct
import tqdm
import glob
import json
from PIL import Image, ImageEnhance

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

def read_ETL6(f):
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

def read_ETL7(f):
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

def read_ETL8G(f):
    record_size = 8199
    s = f.read(record_size)
    if len(s) == 0:
        return None, None
    r = struct.unpack('>2H8sI4B4H2B30x8128s11x', s)
    iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
    iP = iF.convert('RGBA')
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(64)
    return iE, r[1]

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

def read_ETL9G(f):
    record_size = 8199
    s = f.read(record_size)
    if len(s) == 0:
        return None, None
    r = struct.unpack('>2H8sI4B4H2B34x8128s7x', s)
    iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
    iP = iF.convert('RGBA')
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(64)
    return iE, r[1]

def read_file(filename, decoder, jis2unicode, conv_map=None):
    data = []
    idx = 0
    with open(filename, 'rb') as f:
        while True:
            if idx % 1000 == 0:
                print(idx)

            img, label = decoder(f)
            if img is None:
                return data
            
            if conv_map is not None:
                if label in conv_map:
                    label = conv_map[label]
                else:
                    continue
            
            if label in jis2unicode:
                targetname = os.path.basename(filename) + '_{0:08d}.png'.format(idx)
                fullpath = os.path.join(basedir, dirname, child_dir, targetname)
                img.save(fullpath)
                data.append({'filename': os.path.join(dirname, child_dir, targetname), 'label': jis2unicode[label]})
            
            idx += 1
            
if __name__ == '__main__':
    dataname = ['ETL1', 'ETL6', 'ETL7', 'ETL8B', 'ETL8G', 'ETL9B', 'ETL9G']
    parser = argparse.ArgumentParser(prog='ETL')
    parser.add_argument('-d', '--data', type=str, choices=dataname)
    parser.add_argument('-o', '--output', type=str, default='output')
    
    args = parser.parse_args()
    
    print(args.data)
    
    basedir = args.output
    
    props = {
        'ETL1': {
            'dirname': 'ETL1',
            'filename': 'ETL1/ETL1C_*',
            'conv_map': 'katakana_map.json',
            'decoder': read_ETL1,
            'output': 'ETL1.json'
        },
        'ETL6': {
            'dirname': 'ETL6',
            'filename': 'ETL6/ETL6C_*',
            'conv_map': 'katakana_map.json',
            'decoder': read_ETL6,
            'output': 'ETL6.json'
        },
        'ETL7': {
            'dirname': 'ETL7',
            'filename': 'ETL7/ETL7?C_*',
            'conv_map': 'hiragana_map.json',
            'decoder': read_ETL7,
            'output': 'ETL7.json'
        },
        'ETL8B': {
            'dirname': 'ETL8B',
            'filename': 'ETL8B/ETL8B2C*',
            'decoder': read_ETL8B,
            'output': 'ETL8B.json'
        },
        'ETL8G': {
            'dirname': 'ETL8G',
            'filename': 'ETL8G/ETL8G_*',
            'decoder': read_ETL8G,
            'output': 'ETL8G.json'
        },    
        'ETL9B': {
            'dirname': 'ETL9B',
            'filename': 'ETL9B/ETL9B_*',
            'decoder': read_ETL9B,
            'output': 'ETL9B.json'
        },
        'ETL9G': {
            'dirname': 'ETL9G',
            'filename': 'ETL9G/ETL9G_*',
            'decoder': read_ETL9G,
            'output': 'ETL9G.json'
        },    
    }
    
    prop = props[args.data]
    
    dirname = prop['dirname']
    filenames = sorted(glob.glob(prop['filename']))
    
    conv_map = None
    if 'conv_map' in prop:
        with open(prop['conv_map'], 'r') as f:
            conv_map = json.load(f)
        conv_map = {int(k): v for k, v in conv_map.items()}
    
    decoder = prop['decoder']
    
    jis2unicode = {}
    f = open('JIS0208.TXT', 'r')
    for row in f:
        if row[0] != '#':
            code = row.split("\t")[1]
            char = row.split("\t")[2]
            jis2unicode[int(code, 16)] = int(char, 16)
    f.close()
        
    label_data = []
    for f in filenames:
        child_dir = os.path.basename(f)
        os.makedirs(os.path.join(basedir, dirname, child_dir), exist_ok=True)    
        data = read_file(f, decoder, jis2unicode, conv_map=conv_map)
        label_data.extend(data)

    with open(os.path.join(basedir, prop['output']), 'w') as f:
        json.dump(label_data, f)