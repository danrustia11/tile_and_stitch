#
# Optimized tiling class for object detection
# Authors: DJAR (WUR), EASH (DLSU)
# 
# 2022_08_07
# - First version
# - Have to put the codes in a class
#
# 2022_08_09
# - Written a class
#
# 2022_08_14
# - Added labels in tiling
#


import os
import cv2
import math
import numpy as np
from PIL import Image
import pandas as pd


def make_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except:
        pass

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def rounddown(x):
    return int(math.floor(x / 100.0)) * 100

def tiff_to_jpeg(root, filename):
    tiff_filename = os.path.join(root, filename)
    file_ext = os.path.splitext(tiff_filename)[1].lower()
    if file_ext == ".tif":
        jpeg_filename = os.path.splitext(tiff_filename)[0] + ".jpg"
        if os.path.isfile(jpeg_filename):
            pass
        else:
            try:
                im = Image.open(os.path.join(root, filename))
                print("Generating jpeg for {}".format(filename))
                im.thumbnail(im.size)
                im.save(jpeg_filename, "JPEG", quality=100)
            except Exception as e:
                print(e)
    else:
        pass

    return jpeg_filename


class tiler():
    def __init__(self, TILING_SIZE, PADDING):
        print("Created tiler object!")
        self.TP = TILING_SIZE + PADDING
        self.PADDING = PADDING
        self.TILING_SIZE = TILING_SIZE
        print("Tiling size: {}".format(TILING_SIZE))
        print("Padding/overlap: {}".format(PADDING))
        print("Tiling w/ padding: {}".format(self.TP))



    #
    # Inputs:
    # image (cv2 format)
    # labels (df)
    #
    # Outputs:
    # [cropped_image, new_labels]
    # cropped_image - cropped image in cv2 format
    # new_labels - retranslated labels based on cropped image
    #
    def remove_borders(self, image, labels=[], INCLUDE_LABELS=0, DEBUG=0):   

        #
        # Image cropping
        #
        s = image.shape
        l = s[0]
        w = s[1]
    
        w = rounddown(w)
        l = rounddown(l)
    
        # Get divisibility
        # div_x = math.floor(w / self.TP)
        # div_y = math.floor(l / self.TP)
    
        # Generate a list of tiling sizes
        w_list = [(self.TP*a) - self.PADDING*(a-1) for a in np.arange(0, 10) if w >= (self.TP*a) - self.PADDING*(a-1)]
        l_list = [(self.TP*a) - self.PADDING*(a-1) for a in np.arange(0, 10) if l >= (self.TP*a) - self.PADDING*(a-1)]
    
        # Get the maximum tiling size to minimize loss
        x_max = max(w_list)
        y_max = max(l_list)
    
        # Half of excess to make the cut distributed
        border_x = abs((w - x_max)/2)
        border_y = abs((l - y_max)/2)
    
        # Get cutting coords
        x1 = int(0 + border_x)
        x2 = int(w - border_x)
        y1 = int(0 + border_y)
        y2 = int(l - border_y)
    
    
        new_w = x1-x2
        new_l = y1-y2
    
        # Find out loss
        loss_x = w - x_max
        loss_y = l - y_max
    
        # Crop the image
        cropped_image = image[y1:y2, x1:x2]

            
        if DEBUG:
            print("Original size = {} {}".format(w, l))
            # print("Divisibility = {} {}".format(div_x, div_y))
            print("Target size = {} {}".format(x_max, y_max))
            print("Border cut = {} {}".format(border_x, border_y))
            # print(x1, x2, y1, y2)
            print(new_w, new_l)
            print(loss_x, loss_y)
    
    
    
        if INCLUDE_LABELS:
            new_labels = labels.copy()
        
            # Get image original sizes
            orig_w = image.shape[1]
            orig_h = image.shape[0]
        
            # Get cropped image size
            new_w = cropped_image.shape[1]
            new_h = cropped_image.shape[0]
        
            # Denormalize first the coordinates
            unnormed_x1 = labels.iloc[:,1] * orig_w
            unnormed_y1 = labels.iloc[:,2] * orig_h
        
            # Remove loss/2 from denormalized coordinates
            # then, normalize according to new size
            new_x1 = (unnormed_x1 - (loss_x/2)) / new_w
            new_y1 = (unnormed_y1 - (loss_y/2)) / new_h
        
            # Apply changes to df
            new_labels.iloc[:,1] = new_x1 
            new_labels.iloc[:,2] = new_y1
        
            return (cropped_image, new_labels)
        else:
            return cropped_image

    #
    # Crop into cuttable sizes first
    #
    # Inputs:
    # image_dir - the image src dir
    # base_cropped_dir - where the cropped images will be saved
    #
    # Output:
    # cropped_files - filenames of the cropped images
    #
    def remove_borders_dir(self, image_dir, base_cropped_dir, INCLUDE_LABELS=0, DEBUG=0, VERBOSE=1):
        files = os.listdir(image_dir)
        files = [image_dir + "/" + f for f in files]
        files = [f for f in files if ".jpg" in f]
        
        cropped_files = []
        for f, file in enumerate(files):   
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext == ".tif":
                filename = self.tiff_to_jpeg(image_dir, file)
            else:
                filename = file
                
            
            # Read image
            image = cv2.imread(filename)
            if INCLUDE_LABELS:
                filename_label = os.path.splitext(file)[0].lower() + ".txt"
                
                if os.path.exists(filename_label):
                    # Read labels
                    labels = pd.read_csv(filename_label, sep=' ', names=['class', 'x1', 'y1', 'w', 'h'])
                    cropped_image, new_labels = self.remove_borders(image, labels, INCLUDE_LABELS = INCLUDE_LABELS)        
                                
                    # Save the labels
                    cropped_labels = base_cropped_dir + "/" + os.path.basename(file).replace(".jpg", "_cropped.txt")
                    new_labels.to_csv(cropped_labels, header=None, index=False, sep=' ')
            else:
                cropped_image = self.remove_borders(image, INCLUDE_LABELS = 0)        
                
            
            # Save the image
            cropped_file = base_cropped_dir + "/" + os.path.basename(file).replace(".jpg", "_cropped.jpg")
            cv2.imwrite(cropped_file, cropped_image)


            if VERBOSE:
                print("{}/{} {} {}".format(f+1, len(files), cropped_file, cropped_image.shape))
            cropped_files.append(cropped_file)
        return cropped_files
            
            
    
    #
    # Do the tiling (images must be divisible already by tile_size + padding)
    #
    # Input:
    # image (cv2)
    # labels (df)
    #
    # Output:
    # tiled_image_pairs = [x, y, tiled_image, tiled_labels]
    #
    def tile_image(self, image, labels=[], INCLUDE_LABELS=0, DEBUG=0):
             
        # Floor the dimensions
        s = image.shape
        l = s[0]
        w = s[1]
        
        # Get divisibility
        # div_x = math.floor(w / self..TP)
        # div_y = math.floor(l / self..TP)
    
        # Generate a list of tiling sizes
        w_list = [(self.TP*a) - self.PADDING*(a-1) for a in np.arange(0, 10) if w >= (self.TP*a) - self.PADDING*(a-1)]
        l_list = [(self.TP*a) - self.PADDING*(a-1) for a in np.arange(0, 10) if l >= (self.TP*a) - self.PADDING*(a-1)]
        
        d1 = len(w_list)-1
        d2 = len(l_list)-1
        
        # tile_size * y : ((tile_size+200) * (y + 1)) - padding
        # 0000 : 1800 (tile_size+padding)*1 - 200*0
        # 1600 : 3400 (tile_size+padding)*2 - 200*1
        # 3200 : 5000 (tile_size+padding)*3 - 200*2
        # 4800 : 6600 (tile_size+padding)*4 - 200*3
        
        
        
        if INCLUDE_LABELS:
            labels.loc[:, ["x1", "w"]] *= w
            labels.loc[:, ["y1", "h"]] *= l
            
            labels_x1 = labels.iloc[:,1]
            labels_x2 = labels.iloc[:,1] + labels.iloc[:,3]
            labels_y1 = labels.iloc[:,2]
            labels_y2 = labels.iloc[:,2] + labels.iloc[:,4]
        
        tiled_image_pairs = []
        for x in range(0, int(d1)):
            for y in range(0, int(d2)):
                # Perform tiling 
                tx1 = x*self.TILING_SIZE
                tx2 = ((self.TP)*(x+1)) - (self.PADDING*(x))
                ty1 = y*self.TILING_SIZE
                ty2 = ((self.TP)*(y+1)) - (self.PADDING*(y))
                tiled_image = image[ty1: ty2, tx1:tx2] 
                
                
                if INCLUDE_LABELS:
                    # Check if label is in the tiled image
                    tilemask = (labels_x2 <= tx2) & \
                                 (labels_x1 >= tx1) & \
                                 (labels_y2 <= ty2) & \
                                 (labels_y1 >= ty1) 
                    tiled_labels = labels.loc[tilemask]
                    
                    # Adjust the offset
                    tiled_labels.loc[:, "y1"] -= ty1
                    tiled_labels.loc[:, "x1"] -= tx1
    
                    # Renormalize
                    tiled_labels.loc[:, ["x1", "w"]] /= self.TP
                    tiled_labels.loc[:, ["y1", "h"]] /= self.TP
    
                    tiled_image_pairs.append([x, y, tiled_image, tiled_labels])
                else:
                    tiled_image_pairs.append([x, y, tiled_image])
           
        return tiled_image_pairs
            
        
    
    
    
    
    
    
    
    #
    # Do the tiling (images must be divisible already by tile_size + padding)
    #
    # Input:
    # base_cropped_dir - the image src dir
    # train_cropped_dir - where the tiled images will be saved
    #
    # Output:
    # tiled_images - filenames of the tiled images
    #
    def tile_image_dir(self, base_cropped_dir, tiled_dir, INCLUDE_LABELS=0, DEBUG=0, VERBOSE=1):
        files = os.listdir(base_cropped_dir)
        files = [base_cropped_dir + "/" + f for f in files if ".jpg" in f]

        tiled_images = []
        for f, file in enumerate(files):   
            # Read image
            image = cv2.imread(file)
      
            # Do tiling
            if INCLUDE_LABELS:
                filename_label = os.path.splitext(file)[0].lower() + ".txt"
                
                if os.path.exists(filename_label):
                    labels = pd.read_csv(filename_label, sep=' ', names=['class', 'x1', 'y1', 'w', 'h'])
                    tiled_image_pairs = self.tile_image(image, labels, INCLUDE_LABELS=INCLUDE_LABELS)
            else:
                tiled_image_pairs = self.tile_image(image)


            # Save tiled outputs
            for n in range(0, len(tiled_image_pairs)):
                basename = os.path.basename(file)
                x = tiled_image_pairs[n][0]
                y =  tiled_image_pairs[n][1]
                tiled_image = tiled_image_pairs[n][2]
                
                cropped_file = tiled_dir + "/" + basename.replace("_cropped.jpg", "_{}_{}.jpg".format(x, y))
                cv2.imwrite(cropped_file, tiled_image)
                
                
                if INCLUDE_LABELS:
                    tiled_labels = tiled_image_pairs[n][3]
                    tiled_filename = tiled_dir + "/" + basename.replace("_cropped.jpg", "_{}_{}.txt".format(x, y))
                    tiled_labels.to_csv(tiled_filename, header=None, index=False, sep=' ')
                    
                tiled_images.append(cropped_file)
            
            if VERBOSE:
                print("{}/{}".format(f+1, len(files)), file)
                
        return tiled_images



