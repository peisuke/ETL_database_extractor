import argparse
import os
import numpy as np
import tqdm
import glob
import json
import util
from PIL import Image

if __name__ == '__main__':
    dataname = ['ETL1', 'ETL6', 'ETL7', 'ETL8B', 'ETL8G', 'ETL9B', 'ETL9G']
    parser = argparse.ArgumentParser(prog='ETL')
    parser.add_argument('-d', '--data', type=str, choices=dataname, required=True)
    parser.add_argument('-i', '--input', type=str, default='input')
    parser.add_argument('-o', '--output', type=str, default='output')
    
    args = parser.parse_args()
    
    json_name = args.data
    if args.data in ['ETL1', 'ETL6', 'ETL7']:
        check_function = util.check_image
        denoise_function = util.denoise_etl1
    elif args.data in ['ETL8B', 'ETL8G', 'ETL9B']:
        check_function = util.check_ok
        denoise_function = util.denoise_etl2
    elif args.data in ['ETL9G']:
        check_function = util.check_ok
        denoise_function = util.denoise_etl9G
        
    json_file = os.path.join(args.input, json_name + '.json')
    
    with open(json_file, 'r') as f:
        etl = json.load(f)
    
    for e in tqdm.tqdm(etl):
        img = Image.open(os.path.join(args.input, e['filename'])).convert('L')
        e['valid'] = check_function(img)
        img = denoise_function(img)
        
        filename = os.path.join(args.output, e['filename'])
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        img.save(filename)
        
    with open(os.path.join(args.output, json_name + '.json'), 'w') as f:
        json.dump(etl, f)