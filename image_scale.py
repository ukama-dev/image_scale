#!/usr/bin/env python3
"""
iOS App Icon Generator

This script takes an input image and generates all the necessary icon sizes
required for an iOS application.

Usage:
    python image_scale.py input_image.png [output_directory] [options]

If output_directory is not specified, icons will be saved to './AppIcons'

License:
    MIT License
    See the LICENSE file for details.
"""

import os
import sys
import json
import argparse
from typing import Optional
from dataclasses import dataclass
from PIL import Image


@dataclass
class IconSpec:
    """Specification for an app icon."""
    size: int
    filename: str
    idiom: str
    scale: str
    role: Optional[str] = None
    subgroup: Optional[str] = None


class AppIconGenerator:
    """
    A class to generate app icons for iOS applications.
    """

    # Define all required iOS app icon sizes by device type
    IPHONE_ICONS = [
        IconSpec(60, "iphone_60pt@3x", "iphone", "3x", "primary"),
        IconSpec(60, "iphone_60pt@2x", "iphone", "2x", "primary"),
        IconSpec(40, "iphone_40pt@3x", "iphone", "3x", "spotlight"),
        IconSpec(40, "iphone_40pt@2x", "iphone", "2x", "spotlight"),
        IconSpec(29, "iphone_29pt@3x", "iphone", "3x", "settings"),
        IconSpec(29, "iphone_29pt@2x", "iphone", "2x", "settings"),
        IconSpec(20, "iphone_20pt@3x", "iphone", "3x", "notification"),
        IconSpec(20, "iphone_20pt@2x", "iphone", "2x", "notification"),
    ]

    IPAD_ICONS = [
        IconSpec(83.5, "ipad_83.5pt@2x", "ipad", "2x", "primary"),
        IconSpec(76, "ipad_76pt@2x", "ipad", "2x", "primary"),
        IconSpec(40, "ipad_40pt@2x", "ipad", "2x", "spotlight"),
        IconSpec(40, "ipad_40pt", "ipad", "1x", "spotlight"),
        IconSpec(29, "ipad_29pt@2x", "ipad", "2x", "settings"),
        IconSpec(29, "ipad_29pt", "ipad", "1x", "settings"),
        IconSpec(20, "ipad_20pt@2x", "ipad", "2x", "notification"),
        IconSpec(20, "ipad_20pt", "ipad", "1x", "notification"),
    ]

    APP_STORE_ICON = [
        IconSpec(1024, "appstore", "ios-marketing", "1x", "primary"),
    ]

    def __init__(self, input_path: str, output_dir: str, quality: str = "high"):
        """
        Initialize the AppIconGenerator.

        Args:
            input_path: Path to the input image
            output_dir: Directory to save the generated icons
            quality: Quality of the resized images ('high', 'medium', or 'low')
        """
        self.input_path = input_path
        self.output_dir = output_dir
        self.quality = quality
        self.processed_count = 0
        self.total_count = len(self.IPHONE_ICONS + self.IPAD_ICONS + self.APP_STORE_ICON)
        self.needs_upscaling = False

        # Create output directory structure
        self.ios_dir = os.path.join(output_dir, "ios")
        os.makedirs(self.ios_dir, exist_ok=True)

        # Validate input image
        self._validate_input_image()

    def _validate_input_image(self) -> None:
        """
        Validate the input image exists and has sufficient resolution.

        Raises:
            FileNotFoundError: If the input file doesn't exist
            ValueError: If the image is too small
        """
        if not os.path.isfile(self.input_path):
            raise FileNotFoundError(f"Input file '{self.input_path}' does not exist.")

        with Image.open(self.input_path) as img:
            min_dimension = min(img.width, img.height)
            if min_dimension < 512:
                raise ValueError(
                    f"Input image is too small ({img.width}x{img.height}). "
                    "Minimum size is 512x512 pixels."
                )
            elif min_dimension < 1024:
                print(f"Warning: Input image ({img.width}x{img.height}) is smaller than the recommended 1024x1024 pixels.")
                print("The image will be upscaled to generate the required icon sizes.")
                self.needs_upscaling = True
            else:
                self.needs_upscaling = False

    def _get_resize_method(self) -> int:
        """
        Get the appropriate resize method based on the quality setting.

        Returns:
            The PIL resize filter to use
        """
        quality_map = {
            "high": Image.LANCZOS,
            "medium": Image.BICUBIC,
            "low": Image.BILINEAR
        }
        return quality_map.get(self.quality.lower(), Image.LANCZOS)

    def _process_image(self, img: Image.Image, output_size: int, output_path: str) -> None:
        """
        Process and save an image at the specified size.

        Args:
            img: The source image
            output_size: The size to resize to
            output_path: Where to save the resized image
        """
        # Resize the image
        resize_method = self._get_resize_method()
        resized_img = img.resize((output_size, output_size), resize_method)

        # Save the resized image
        resized_img.save(output_path, "PNG", optimize=True)

        # Update progress
        self.processed_count += 1
        progress = (self.processed_count / self.total_count) * 100
        print(f"[{progress:.1f}%] Created: {output_path} ({output_size}x{output_size})")

    def _upscale_image(self, img: Image.Image, target_size: int = 1024) -> Image.Image:
        """
        Upscale an image to the target size using the high-quality resize method.

        Args:
            img: The source image to upscale
            target_size: The target size (width and height) for the upscaled image

        Returns:
            The upscaled image
        """
        current_size = img.width  # Image is already square at this point
        if current_size >= target_size:
            return img

        print(f"Upscaling image from {current_size}x{current_size} to {target_size}x{target_size}...")
        # Always use LANCZOS for upscaling as it provides the best quality
        return img.resize((target_size, target_size), Image.LANCZOS)

    def _prepare_image(self) -> Image.Image:
        """
        Prepare the input image for processing.

        Returns:
            A square version of the input image, upscaled if necessary
        """
        with Image.open(self.input_path) as img:
            # Convert to RGB if needed
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')

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

            # Create a copy to work with
            processed_img = img.copy()

            # Upscale if needed
            if self.needs_upscaling:
                processed_img = self._upscale_image(processed_img)

            return processed_img

    def _generate_contents_json(self) -> None:
        """Generate a Contents.json file for Xcode asset catalogs."""
        contents = {
            "images": [],
            "info": {
                "version": 1,
                "author": "xcode"
            }
        }

        # Add all icons to the images array
        for icon_set in [self.IPHONE_ICONS, self.IPAD_ICONS, self.APP_STORE_ICON]:
            for icon in icon_set:
                # Calculate actual pixel size
                scale_factor = int(icon.scale[0]) if icon.scale[0].isdigit() else 1
                pixel_size = int(icon.size * scale_factor)

                image_info = {
                    "size": f"{icon.size}x{icon.size}",
                    "idiom": icon.idiom,
                    "filename": f"{icon.filename}_{pixel_size}x{pixel_size}.png",
                    "scale": icon.scale
                }

                if icon.role:
                    image_info["role"] = icon.role

                if icon.subgroup:
                    image_info["subgroup"] = icon.subgroup

                contents["images"].append(image_info)

        # Write the Contents.json file
        contents_path = os.path.join(self.ios_dir, "Contents.json")
        with open(contents_path, 'w') as f:
            json.dump(contents, f, indent=2)

        print(f"Created: {contents_path}")

    def generate_icons(self) -> None:
        """Generate all required app icons."""
        try:
            # Prepare the image
            img = self._prepare_image()

            # Process all icon sizes
            for icon_set in [self.IPHONE_ICONS, self.IPAD_ICONS, self.APP_STORE_ICON]:
                for icon in icon_set:
                    # Calculate actual pixel size
                    scale_factor = int(icon.scale[0]) if icon.scale[0].isdigit() else 1
                    pixel_size = int(icon.size * scale_factor)

                    # Generate output path
                    output_filename = f"{icon.filename}_{pixel_size}x{pixel_size}.png"
                    output_path = os.path.join(self.ios_dir, output_filename)

                    # Process the image
                    self._process_image(img, pixel_size, output_path)

            # Generate Contents.json for Xcode
            self._generate_contents_json()

            print(f"\nAll iOS app icons have been generated in: {os.path.abspath(self.output_dir)}")
            print("You can now use these icons in your iOS app project.")

        except Exception as e:
            print(f"Error generating icons: {e}")
            sys.exit(1)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Generate iOS app icons from an input image.')
    parser.add_argument('input_image', help='Path to the input image (preferably 1024x1024 PNG)')
    parser.add_argument('output_dir', nargs='?', default='AppIcons',
                        help='Directory to save the generated icons (default: AppIcons)')
    parser.add_argument('--quality', choices=['high', 'medium', 'low'], default='high',
                        help='Quality of the resized images (default: high)')

    args = parser.parse_args()

    try:
        # Create the generator and generate icons
        generator = AppIconGenerator(args.input_image, args.output_dir, args.quality)
        generator.generate_icons()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
