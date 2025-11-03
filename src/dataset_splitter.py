import shutil
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

CSV_PATH = Path("artifacts/dataset_marks.csv")
OUTPUT_DIR = Path("datasets/splits")
K = 8
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)
assert "image_name" in df.columns and "age" in df.columns

# splitting by ages.
df["age_bin"] = pd.qcut(df["age"], q=K, labels=False, duplicates="drop")

print(df.groupby("age_bin")["age"].describe())  # посмотреть диапазоны квантилей

train_df, temp_df = train_test_split(
    df,
    test_size=0.3,                # 70% train, 30% остальное
    stratify=df["age_bin"],
    random_state=42
)

val_df, test_df = train_test_split(
    temp_df,
    test_size=1/3,                # 1/3 от 30% = 10% от общего
    stratify=temp_df["age_bin"],
    random_state=42
)

train_df.to_csv(OUTPUT_DIR / "train_labels.csv", index=False)
val_df.to_csv(OUTPUT_DIR / "val_labels.csv", index=False)
test_df.to_csv(OUTPUT_DIR / "test_labels.csv", index=False)

print(f"Train: {len(train_df)}  Val: {len(val_df)}  Test: {len(test_df)}")

# Copying files.

SPLITTED_PATH = Path("datasets/splits")
ALL_IMAGES_PATH = Path("datasets/processed")

TRAIN_PATH = SPLITTED_PATH.joinpath("train/")
VALIDATE_PATH = SPLITTED_PATH.joinpath("validate/")
TEST_PATH = SPLITTED_PATH.joinpath("test/")

for index, row in train_df.iterrows():
    image_name = row["image_name"]
    age = row["age"]
    
    src_path = ALL_IMAGES_PATH.joinpath(image_name)
    dst_path = TRAIN_PATH.joinpath(image_name)
    
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"Copied {src_path} -> {dst_path} (TRAIN)")
    
for index, row in val_df.iterrows():
    image_name = row["image_name"]
    age = row["age"]
    
    src_path = ALL_IMAGES_PATH.joinpath(image_name)
    dst_path = VALIDATE_PATH.joinpath(image_name)
    
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"Copied {src_path} -> {dst_path} (VALIDATE)")
    
for index, row in test_df.iterrows():
    image_name = row["image_name"]
    age = row["age"]
    
    src_path = ALL_IMAGES_PATH.joinpath(image_name)
    dst_path = TEST_PATH.joinpath(image_name)
    
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"Copied {src_path} -> {dst_path} (TEST)")