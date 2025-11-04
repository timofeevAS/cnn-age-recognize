#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/datasets"
UTKFACE_DIR="${DATA_DIR}/UTKFace"
ZIP_PATH="${SCRIPT_DIR}/utkface-new.zip"
TMP_DIR="${DATA_DIR}/tmp"

echo "📦 Installing UTKFace dataset..."

# Dont download archive if exists.
if [ ! -f "$ZIP_PATH" ]; then
    echo "⬇️  Downloading UTKFace..."
    curl -L -o "$ZIP_PATH" "https://www.kaggle.com/api/v1/datasets/download/jangedoo/utkface-new"
fi

mkdir -p "$UTKFACE_DIR" "$TMP_DIR"
echo "🧩 Extracting only utkface_aligned_cropped/UTKFace..."
unzip -q -o "$ZIP_PATH" "utkface_aligned_cropped/UTKFace/*.jpg" -d "$TMP_DIR"

if [ -d "$TMP_DIR/utkface_aligned_cropped/UTKFace" ]; then
    rsync -a "$TMP_DIR/utkface_aligned_cropped/UTKFace/" "$UTKFACE_DIR/"
    echo "✅ Moved $(ls "$UTKFACE_DIR" | wc -l) files to $UTKFACE_DIR"
else
    echo "❌ Expected folder not found inside archive"
    exit 1
fi

echo "📁 Delete temporary folder..."
rm -rf "$TMP_DIR"

echo "✅ Installing UTKFaces succesful!"

echo "📦 Installing APPA dataset..."

ZIP_PATH="${SCRIPT_DIR}/appa-real-release.zip"
if [ ! -f "$ZIP_PATH" ]; then
    echo "⬇️  Downloading APPA dataset..."
    curl -L -o "$ZIP_PATH" "https://data.chalearnlap.cvc.uab.cat/AppaRealAge/appa-real-release.zip"
fi

APPA_DIR="${DATA_DIR}/appa"

echo "🧩 Extracting appa data set appa-real-release/..."
unzip -q -o "$ZIP_PATH" \
  "appa-real-release/gt_avg_train.csv" \
  "appa-real-release/gt_test.csv" \
  "appa-real-release/gt_valid.csv" \
  "appa-real-release/train/*" \
  "appa-real-release/test/*" \
  "appa-real-release/valid/*" \
  -d $APPA_DIR

if [ -d "$APPA_DIR/appa-real-release" ]; then
    rsync -a "$APPA_DIR/appa-real-release/" "$APPA_DIR"
    echo "✅ Moved $(ls "$APPA_DIR/appa-real-release/" | wc -l) files to $APPA_DIR"
else
    echo "❌ Expected folder not found inside archive"
    exit 1
fi

echo "📁 Delete temporary folder..."
rm -rf "$APPA_DIR/appa-real-release"

echo "🗯️ Filtering appa dataset..."
echo "🗯️ Left only necessary pictures in storage... ($APPA_DIR/train)"
find "$APPA_DIR/train" -type f ! -name "*.jpg_face.jpg" -delete
echo "🗯️ Left only necessary pictures in storage... ($APPA_DIR/test)"
find "$APPA_DIR/test" -type f ! -name "*.jpg_face.jpg" -delete
echo "🗯️ Left only necessary pictures in storage... ($APPA_DIR/valid)"
find "$APPA_DIR/valid" -type f ! -name "*.jpg_face.jpg" -delete

echo "✅ Installing APPA real faces succesful!"