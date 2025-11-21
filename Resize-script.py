#Script to resize photos for use in Scratch backdrops

from PIL import Image, ImageOps
import os

# --- Configuration ---
input_folder = "input_images"   # Folder containing your images
output_folder = "scratch_backdrops"  # Folder to save resized images
target_size = (480, 360)        # Scratch backdrop size
suffix = "_scratchBD"           # Suffix for output files

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")

# Process images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(extensions):
        input_path = os.path.join(input_folder, filename)
        img = Image.open(input_path)

        # Resize while keeping aspect ratio and add padding
        img_resized = ImageOps.contain(img, target_size)
        # Create new blank image and paste resized image centered
        background = Image.new("RGBA", target_size, (255, 255, 255, 255))
        paste_pos = ((target_size[0] - img_resized.width) // 2,
                     (target_size[1] - img_resized.height) // 2)
        background.paste(img_resized, paste_pos)

        # Save as PNG with new suffix
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{base_name}{suffix}.png")
        background.save(output_path)

        print(f"Saved: {output_path}")

print("All images processed!")
