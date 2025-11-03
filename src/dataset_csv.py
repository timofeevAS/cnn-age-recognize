import glob
import os

from pathlib import Path
import matplotlib.pyplot as plt

import pandas as pd

# This scripts saves csv with age distribution for images
dataset_path = os.path.join("datasets", "processed", "*.jpg")
images = glob.glob(dataset_path)

data = []
for image in images:
    # Example of image name: `image_[num]_[real_age].jpg`
    path = Path(image)
    real_age = int(path.stem.split('_')[-1])
    image_name = path.name
    data.append({'image_name': image_name, 'age': real_age})
    
if not data:
    raise ValueError("Zero ages. Nothing to show.")
    
df = pd.DataFrame(data)
df.to_csv('dataset_marks.csv')
print(df)