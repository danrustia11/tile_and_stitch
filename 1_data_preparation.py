#
# Data preparation script for tiling
# Authors: DJAR (WUR), EASH (DLSU)
#
# 2022/08/12
# - Finished up to splitting
#
# 2022/08/14
# - Finished tiling part
#
#
# Sample usage
#
# If without labels:
# python 1_data_preparation.py --dir E:\Research_data\2022_WA\base --tile 1200 --padding 200
#
# If with labels:
# [With density splitting]
# python 1_data_preparation.py --dir "E:\Research_data\2022_CEA_B\base\train and validation" --tile 1200 --padding 200 --density 10,30
# [Without density splitting]
# python 1_data_preparation.py --dir "E:\Research_data\2022_CEA_B\base\train and validation" --tile 1200 --padding 200 
#




import argparse
from PIL import Image
import glob
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path
import random
import math
import shutil
import tools.image_tiler as tl

# change this to args
LOW_COUNT = 10
HIGH_COUNT = 30
SPLIT_BY_DENSITY = 0
TRAIN_VALID_SPLIT = 0.8 # % of dataset that will be used for training
TILING_SIZE = 1200
PADDING = 100*2
VERBOSE = 0
seed = 42

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, default="")
parser.add_argument('--split', type=list, default=[TRAIN_VALID_SPLIT, round(1-TRAIN_VALID_SPLIT, 2), 0])
parser.add_argument('--tile', type=int, default=TILING_SIZE)
parser.add_argument('--padding', type=int, default=PADDING)
parser.add_argument('--verbose', type=int, default=VERBOSE)
parser.add_argument('--density', type=str, default="")
args = parser.parse_args()




if args.dir != "":
    
    # Some error handling for density splitting
    images = [l for l in os.listdir(args.dir) if ".jpeg" in l]
    n_images = len(images)
    txts = [l for l in os.listdir(args.dir) if ".txt" in l]
    labels = [l for l in txts if "classes" not in l]
    n_labels = len(labels)
    density = args.density.split(",")

    print("")
    print("Data source directory: {}".format(args.dir))
    print("Data split [train, validation, test]: {}".format(args.split))
    print("Tiling size: {}".format(args.tile))
    print("Padding size: {}".format(args.padding))
    print("Number of images: {}".format(n_images))
    print("Number of labels: {}".format(n_labels))
    

    if len(density) == 2:
        SPLIT_BY_DENSITY = 1
        density = list(map(int, density))
        print("Density split: {}".format(density))
    if n_labels == 0:
        SPLIT_BY_DENSITY = 0
        INCLUDE_LABELS = 0
        print("[WARNING] Split by density not possible since no labels were detected!")
    else:
        INCLUDE_LABELS = 1
    print("")
    
    # Initialize a tiler object
    tiler = tl.tiler(TILING_SIZE, PADDING)
    print("")
    
    
    
    
    
    
    
    #
    # 1) Get all labels from directory
    #
    print("[1] Get all files")
    files_dir_list = glob.glob(args.dir  + '/*.jpg')
    files_dir_listPrime = list() #list holding directories without extensions
    
    # Remove extensions
    for file in files_dir_list:
        if "classes" not in file:
            child_path = Path(file).stem                    # remove .txt extension
            parent_path = os.path.split(file)[0]            # get only the parent path; leave out child path
            file = os.path.join(parent_path, child_path)    # filename without extension
            files_dir_listPrime.append(file)
        
    print("Number of basenames: {}".format(len(files_dir_listPrime)))
    print("Done getting all basenames!")
    print("")
    
    
    
    
    
    
    #
    # 2) Split by density
    #
    
    if SPLIT_BY_DENSITY == 1:
        print("[2] Split by density")
        # Empty lists for storing filenames
        low_data = list()
        medium_data = list()
        high_data = list()
        
        for file in files_dir_listPrime:
            # Read txt file and convert to dataframe
            labels_filename = file + '.txt'
            
            if os.path.exists(labels_filename):
                df = pd.read_csv(labels_filename, sep=' ', names=['x', 'y', 'w', 'h'])
                
                if df.shape[0] <= LOW_COUNT:
                    low_data.append(file)
                elif df.shape[0] > LOW_COUNT and df.shape[0] < HIGH_COUNT:
                    medium_data.append(file)
                elif df.shape[0] >= HIGH_COUNT:
                    high_data.append(file)
            
        print("LOW: {} HIGH: {}".format(LOW_COUNT, HIGH_COUNT))
        print("Low density images: {}".format(len(low_data)))
        print("Medium density images: {}".format(len(medium_data)))
        print("High density images: {}".format(len(high_data)))
        print("Done splitting!")
    else:
        all_data = files_dir_listPrime.copy()
        print("[2] Skipped split by density")
    print("")
                
    
    
    
    
            
            
            
    #
    # 3) Split each density by train and valid
    #
    
    print("[3] Split by train/valid")
    if SPLIT_BY_DENSITY == 1:   
        #split low density list by train and validation
        random.Random(seed).shuffle(low_data) #shuffle master list of low_cpb
        count = math.floor(len(low_data) * TRAIN_VALID_SPLIT)
        low_data_train = low_data[ : count]
        low_data_valid = low_data[count : ]
        
        #split medium density list by train and validation
        random.Random(seed).shuffle(medium_data) #shuffle master list of low_data
        count = math.floor(len(medium_data) * TRAIN_VALID_SPLIT)
        medium_data_train = medium_data[ : count]
        medium_data_valid = medium_data[count : ]
        
        #high density list by train and validation
        random.Random(seed).shuffle(high_data) #shuffle master list of low_data
        count = math.floor(len(high_data) * TRAIN_VALID_SPLIT) #floor value to avoid decimals
        high_data_train = high_data[ : count]
        high_data_valid = high_data[count : ]
        
        
        print("Low density train, valid: [{},{}]".format(len(low_data_train), len(low_data_valid)))
        print("Medium density train, valid: [{},{}]".format(len(medium_data_train), len(medium_data_valid)))
        print("High density train, valid: [{},{}]".format(len(high_data_train), len(high_data_valid)))
    else:
        random.Random(seed).shuffle(all_data) #shuffle master list of low_data
        count = math.floor(len(all_data) * TRAIN_VALID_SPLIT) #floor value to avoid decimals
        data_train = all_data[ : count]
        data_valid = all_data[count : ]
        
        print("Train, valid: [{},{}]".format(len(data_train), len(data_valid)))
    print("")
    
    
    
    
    
    
    #
    # 4) Compile all density images and augment training images
    #
    
    print("[4] Copy train/valid")
    split_folder = os.path.join(args.dir , 'split')
    tl.make_folder(split_folder)
    tl.make_folder(split_folder + '/train')
    tl.make_folder(split_folder + '/valid')

    
    if SPLIT_BY_DENSITY == 1:   
        # Copy train
        for file in low_data_train + medium_data_train + high_data_train:
            shutil.copy(file + '.jpg', os.path.join(split_folder, 'train')) #copy image
            try:
                shutil.copy(file + '.txt', os.path.join(split_folder, 'train')) #copy txt
            except:
                pass
        # Copy valid
        for file in low_data_valid + medium_data_valid + high_data_valid:
            shutil.copy(file + '.jpg', os.path.join(split_folder, 'valid')) #copy image
            try:
                shutil.copy(file + '.txt', os.path.join(split_folder, 'valid')) #copy txt
            except:
                pass
    else:
        # Copy train
        for file in data_train:
            shutil.copy(file + '.jpg', os.path.join(split_folder, 'train')) #copy image
            try:
                shutil.copy(file + '.txt', os.path.join(split_folder, 'train')) #copy txt
            except:
                pass
        for file in data_valid:
            shutil.copy(file + '.jpg', os.path.join(split_folder, 'valid')) #copy image
            try:
                shutil.copy(file + '.txt', os.path.join(split_folder, 'valid')) #copy txt
            except:
                pass
        
    print("Done copying train/valid images and labels!")
    print("")
        
        
    
        
    
    #
    # 5) Remove excessive borders from the image
    #
    print("[5] Remove borders")
    split_cropped_folder = split_folder + "_{}_{}".format(TILING_SIZE, PADDING)
    tl.make_folder(split_cropped_folder)
    
    folders = ["train", "valid"]
    for f in folders:
        src_folder = os.path.join(split_folder, f)
        dst_folder = os.path.join(split_cropped_folder, f)
        tl.make_folder(dst_folder)
        
        tiler.remove_borders_dir(src_folder, dst_folder, INCLUDE_LABELS = INCLUDE_LABELS, VERBOSE = VERBOSE)
    print("Done removing borders!")
    print("")
        
    
    

    #
    # 6) Perform tiling
    #
    
    print("[6] Perform tiling according to {}x{}".format(TILING_SIZE+PADDING, TILING_SIZE+PADDING))
    split_tiled_folder = split_folder + "_tiled_{}_{}".format(TILING_SIZE, PADDING)
    tl.make_folder(split_tiled_folder)
    
    folders = ["train", "valid"]
    for f in folders:
        src_folder = os.path.join(split_cropped_folder, f)
        dst_folder = os.path.join(split_tiled_folder, f)
        tl.make_folder(dst_folder)
        
        tiler.tile_image_dir(src_folder, dst_folder, INCLUDE_LABELS = INCLUDE_LABELS, VERBOSE = 0)
        
    print("Done tiling!")
    print("")
        


    
    
    
    
    '''
    
    # Maybe no need
    # 6 augment train images
    th.apply_flipping(source='./CPB dataset2/padded/train', target='./CPB dataset2/final/train')
    
    if not os.path.exists('./CPB dataset2/final/valid'):
        os.mkdir('./CPB dataset2/final/valid')
        os.mkdir('./CPB dataset2/final/valid/images')
        os.mkdir('./CPB dataset2/final/valid/labels')
        
    [shutil.copy(file, './CPB dataset2/final/valid/images') for file in glob.glob('./CPB dataset2/padded/valid/images/*.jpg')]
    [shutil.copy(file, './CPB dataset2/final/valid/labels') for file in glob.glob('./CPB dataset2/padded/valid/labels/*.txt')]
    
    
        
    
    '''
    
