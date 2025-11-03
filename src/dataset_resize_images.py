import glob
import os
from pathlib import Path
from PIL import Image

PROCESSED_IMAGES_PATH = Path("datasets/processed/*.jpg")
all_images = glob.glob(str(PROCESSED_IMAGES_PATH))

OUTPUT_DIR = Path("datasets/resized")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for image in all_images:
    try:
        img = Image.open(image).convert("RGB")
        img_resized = img.resize((224, 224))

        filename = Path(image).name
        save_path = OUTPUT_DIR / filename

        img_resized.save(save_path, "JPEG")
        print(f"Resized: {str(save_path)}")
    except Exception as e:
        print(f"Error processing {image}: {e}")