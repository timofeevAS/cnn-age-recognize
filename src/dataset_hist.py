import glob
import os

from pathlib import Path
import matplotlib.pyplot as plt

# This scripts saves histogram with age distribution for directory
dataset_path = os.path.join("datasets", "processed", "*.jpg")
images = glob.glob(dataset_path)

ages = []
for image in images:
    # Example of image name: `image_[num]_[real_age].jpg`
    path = Path(image)
    real_age = int(path.stem.split('_')[-1])
    ages.append(real_age)
    

if not ages:
    raise ValueError("Zero ages. Nothing to show.")
    
plt.figure(figsize=(10, 6))
plt.hist(ages, bins=100, edgecolor='black')
plt.title("Real age distribution")
plt.xlabel("Age")
plt.ylabel("Amount of image")
plt.grid(axis='y', alpha=0.4)
plt.tight_layout()
plt.savefig("age_histogram.pdf")