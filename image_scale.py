#!/usr/bin/env python3
"""
iOS App Icon Generator

This script takes an input image and generates all the necessary icon sizes
required for an iOS application.

Usage:
    python image_scale.py input_image.png [output_directory]

If output_directory is not specified, icons will be saved to './AppIcons'
"""

import os
import sys
import argparse
from PIL import Image

# Define all required iOS app icon sizes
# Format: (size, filename_prefix, description)
IOS_ICON_SIZES = [
    (1024, "appstore", "App Store"),
    (180, "iphone_60pt@3x", "iPhone App Icon @3x"),
    (167, "ipad_83.5pt@2x", "iPad Pro App Icon"),
    (152, "ipad_76pt@2x", "iPad, iPad mini App Icon"),
    (120, "iphone_60pt@2x", "iPhone App Icon @2x"),
    (120, "iphone_40pt@3x", "iPhone Spotlight @3x"),
    (87, "iphone_29pt@3x", "iPhone Settings @3x"),
    (80, "iphone_40pt@2x", "iPhone Spotlight @2x"),
    (80, "ipad_40pt@2x", "iPad Spotlight @2x"),
    (76, "ipad_76pt", "iPad App Icon @1x"),
    (60, "iphone_60pt", "iPhone App Icon @1x"),
    (58, "iphone_29pt@2x", "iPhone Settings @2x"),
    (58, "ipad_29pt@2x", "iPad Settings @2x"),
    (40, "iphone_40pt", "iPhone Spotlight @1x"),
    (40, "ipad_40pt", "iPad Spotlight @1x"),
    (29, "iphone_29pt", "iPhone Settings @1x"),
    (29, "ipad_29pt", "iPad Settings @1x"),
    (20, "iphone_20pt", "iPhone Notification @1x"),
    (20, "ipad_20pt", "iPad Notification @1x"),
]

def resize_image(input_image_path, output_size, output_path):
    """
    Resize the input image to the specified size and save it to the output path.
    
    Args:
        input_image_path (str): Path to the input image
        output_size (int): Size of the output image (width and height)
        output_path (str): Path to save the resized image
    """
    try:
        with Image.open(input_image_path) as img:
            # Check if image is square
            if img.width != img.height:
                print(f"Warning: Input image is not square ({img.width}x{img.height}). Icons should be square.")
                # Crop to square from center
                min_dimension = min(img.width, img.height)
                left = (img.width - min_dimension) // 2
                top = (img.height - min_dimension) // 2
                right = left + min_dimension
                bottom = top + min_dimension
                img = img.crop((left, top, right, bottom))
                
            # Resize the image
            resized_img = img.resize((output_size, output_size), Image.LANCZOS)
            
            # Save the resized image
            resized_img.save(output_path)
            print(f"Created: {output_path} ({output_size}x{output_size})")
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate iOS app icons from an input image.')
    parser.add_argument('input_image', help='Path to the input image (preferably 1024x1024 PNG)')
    parser.add_argument('output_dir', nargs='?', default='AppIcons', 
                        help='Directory to save the generated icons (default: AppIcons)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.input_image):
        print(f"Error: Input file '{args.input_image}' does not exist.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")
    
    # Process each icon size
    for size, prefix, description in IOS_ICON_SIZES:
        output_filename = f"{prefix}_{size}x{size}.png"
        output_path = os.path.join(args.output_dir, output_filename)
        
        resize_image(args.input_image, size, output_path)
    
    print(f"\nAll iOS app icons have been generated in: {os.path.abspath(args.output_dir)}")
    print("You can now use these icons in your iOS app project.")

if __name__ == "__main__":
    main()
