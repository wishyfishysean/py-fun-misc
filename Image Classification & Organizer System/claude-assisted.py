"""
Image Classification and Organization System
Automatically classifies, renames, and organizes images into folders
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
import hashlib

class ImageClassifier:
    def __init__(self, source_folder, output_folder="organized_images"):
        self.source_folder = Path(source_folder)
        self.output_folder = Path(output_folder)
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
        
        # Create output folder if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)
        
    def classify_by_content(self, img_path):
        """Classify image based on basic properties"""
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                aspect_ratio = width / height
                mode = img.mode
                
                # Classification logic
                if aspect_ratio > 1.5:
                    return "panoramic"
                elif aspect_ratio < 0.7:
                    return "portrait"
                elif mode == "RGBA" or mode == "LA":
                    return "transparent"
                elif width >= 3000 or height >= 3000:
                    return "high_resolution"
                elif width <= 500 and height <= 500:
                    return "thumbnails"
                else:
                    return "standard"
        except Exception as e:
            print(f"Error classifying {img_path}: {e}")
            return "uncategorized"
    
    def classify_by_date(self, img_path):
        """Classify by creation/modification date"""
        try:
            timestamp = os.path.getmtime(img_path)
            date = datetime.fromtimestamp(timestamp)
            return date.strftime("%Y-%m")
        except:
            return "unknown_date"
    
    def classify_by_size(self, img_path):
        """Classify by file size"""
        try:
            size_mb = os.path.getsize(img_path) / (1024 * 1024)
            if size_mb < 0.5:
                return "small"
            elif size_mb < 2:
                return "medium"
            else:
                return "large"
        except:
            return "unknown_size"
    
    def generate_hash(self, img_path):
        """Generate hash for duplicate detection"""
        hash_md5 = hashlib.md5()
        with open(img_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()[:8]
    
    def rename_image(self, img_path, category, index):
        """Generate new filename"""
        ext = img_path.suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_short = self.generate_hash(img_path)
        new_name = f"{category}_{timestamp}_{index:04d}_{hash_short}{ext}"
        return new_name
    
    def organize_images(self, classification_method="content"):
        """Main method to organize images"""
        print(f"Starting image organization from: {self.source_folder}")
        print(f"Output directory: {self.output_folder}\n")
        
        # Find all images
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(self.source_folder.glob(f"*{ext}"))
            image_files.extend(self.source_folder.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print("No images found in the source folder!")
            return
        
        print(f"Found {len(image_files)} images\n")
        
        # Process each image
        processed = 0
        skipped = 0
        
        for idx, img_path in enumerate(image_files, 1):
            try:
                # Classify image
                if classification_method == "content":
                    category = self.classify_by_content(img_path)
                elif classification_method == "date":
                    category = self.classify_by_date(img_path)
                elif classification_method == "size":
                    category = self.classify_by_size(img_path)
                else:
                    category = "general"
                
                # Create category folder
                category_folder = self.output_folder / category
                category_folder.mkdir(exist_ok=True)
                
                # Rename and move image
                new_name = self.rename_image(img_path, category, idx)
                new_path = category_folder / new_name
                
                shutil.copy2(img_path, new_path)
                
                print(f"✓ Processed: {img_path.name}")
                print(f"  → Category: {category}")
                print(f"  → New name: {new_name}\n")
                
                processed += 1
                
            except Exception as e:
                print(f"✗ Error processing {img_path.name}: {e}\n")
                skipped += 1
        
        # Summary
        print("=" * 60)
        print(f"Organization complete!")
        print(f"Processed: {processed} images")
        print(f"Skipped: {skipped} images")
        print(f"Output location: {self.output_folder.absolute()}")
        print("=" * 60)
    
    def find_duplicates(self):
        """Find duplicate images based on hash"""
        print("Scanning for duplicate images...\n")
        
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(self.source_folder.glob(f"*{ext}"))
            image_files.extend(self.source_folder.glob(f"*{ext.upper()}"))
        
        hash_dict = {}
        duplicates = []
        
        for img_path in image_files:
            try:
                img_hash = self.generate_hash(img_path)
                if img_hash in hash_dict:
                    duplicates.append((hash_dict[img_hash], img_path))
                    print(f"Duplicate found:")
                    print(f"  Original: {hash_dict[img_hash].name}")
                    print(f"  Duplicate: {img_path.name}\n")
                else:
                    hash_dict[img_hash] = img_path
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate(s)")
        else:
            print("No duplicates found!")
        
        return duplicates


# Example usage
if __name__ == "__main__":
    # Configuration
    SOURCE = "images"  # Change this to your source folder
    OUTPUT = "organized_images"  # Output folder
    
    # Create classifier instance
    classifier = ImageClassifier(SOURCE, OUTPUT)
    
    # Choose classification method: "content", "date", or "size"
    print("Image Classification & Organization System")
    print("=" * 60)
    print("\nClassification methods available:")
    print("1. content - Based on image dimensions and properties")
    print("2. date - Based on file creation/modification date")
    print("3. size - Based on file size")
    print("\nUsing: content-based classification\n")
    
    # Organize images
    classifier.organize_images(classification_method="content")
    
    # Optional: Find duplicates
    print("\n" + "=" * 60)
    classifier.find_duplicates()
