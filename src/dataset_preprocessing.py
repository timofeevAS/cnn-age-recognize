import shutil
import pandas as pd
import glob
import os

from pathlib import Path

# This script work as preprocessing existing dataset. To install dataset and make prepare work use script: datasets_install.sh TODO! (yet no script)
# After this step, you got directory: /datasets/all_images which contains images with name in format: image_[number]_[real_age].jpeg.

# Read metadata of APPA dataset.
csv_path = os.path.join("datasets", "appa", "*.csv")
csv_files = glob.glob(csv_path)

if not csv_files:
    raise FileNotFoundError("No CSV files found!")

df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

image_path_appa = os.path.join("datasets", "appa", "all_images", "*.jpg")
images_appa = glob.glob(image_path_appa)

# Copy images with next format name: image_[number]_[real_age]
IMAGE_NUMBER = 1
PREPROCESSED_PATH = os.path.join("datasets", "processed")
for image in images_appa:
    path = Path(image)
    image_name = path.name.split('_face')[0]
    
    row = df.loc[df['file_name'] == image_name, 'real_age']
    if row.empty:
        print(f"Not found real_age: {image_name}!")
        continue
    
    real_age = int(row.values[0])
    
    new_name = f"image_{IMAGE_NUMBER:05d}_{real_age}.jpg"
    dst_path = os.path.join(PREPROCESSED_PATH, new_name)
    
    shutil.copy2(image, dst_path)
    print(f"Copied {image} -> {new_name}")  
    
    IMAGE_NUMBER += 1

image_path_utkface = os.path.join("datasets", "UTKFace", "*.jpg")
images_utkface = glob.glob(image_path_utkface)

# Copy images with next format name: image_[number]_[real_age]
for image in images_utkface:
    path = Path(image)
    real_age = int(path.stem.split('_')[0])
    
    new_name = f"image_{IMAGE_NUMBER:05d}_{real_age}.jpg"
    dst_path = os.path.join(PREPROCESSED_PATH, new_name)
    
    shutil.copy2(image, dst_path)
    print(f"Copied {image} -> {new_name}")  
    
    IMAGE_NUMBER += 1
    