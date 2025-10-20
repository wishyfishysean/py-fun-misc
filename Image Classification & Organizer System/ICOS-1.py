import os
import shutil
from PIL import Image
import numpy as np
import tensorflow as tf

# --- SETTINGS ---
INPUT_FOLDER = "images_in"
OUTPUT_FOLDER = "classified"

# Create folders if not exist
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load pre-trained MobileNetV2 model + labels
model = tf.keras.applications.MobileNetV2(weights="imagenet")
decode_predictions = tf.keras.applications.mobilenet_v2.decode_predictions
preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

def classify_image(image_path):
    """Return top label prediction for a given image."""
    try:
        img = Image.open(image_path).convert('RGB').resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)
        decoded = decode_predictions(predictions, top=1)[0][0]
        label = decoded[1]  # e.g., 'golden_retriever'
        return label
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "unknown"

def organize_images():
    """Classify and move images."""
    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        
        file_path = os.path.join(INPUT_FOLDER, filename)
        label = classify_image(file_path)
        label_folder = os.path.join(OUTPUT_FOLDER, label)
        os.makedirs(label_folder, exist_ok=True)

        new_name = f"{label}_{filename}"
        new_path = os.path.join(label_folder, new_name)
        shutil.move(file_path, new_path)
        print(f"Moved {filename} → {new_path}")

if __name__ == "__main__":
    print("🔍 Classifying images in folder:", INPUT_FOLDER)
    organize_images()
    print("✅ Classification complete!")
