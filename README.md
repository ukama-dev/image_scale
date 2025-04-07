# iOS App Icon Generator

A Python script that generates all the necessary icon sizes required for iOS applications, organized by device type and with proper naming conventions for Xcode.

## Features

- Generates all required iOS app icon sizes for iPhone and iPad
- Creates a proper directory structure for easy import into Xcode
- Generates a Contents.json file for Xcode asset catalogs
- Supports different quality levels for image resizing
- Validates input images for proper size and format
- Shows progress during generation
- Handles non-square images by automatically cropping

## Requirements

- Python 3.6+
- Pillow library

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python image_scale.py input_image.png [output_directory] [options]
```

### Arguments

- `input_image.png`: Path to the input image (preferably a 1024x1024 PNG)
- `output_directory` (optional): Directory to save the generated icons (default: `./AppIcons`)

### Options

- `--quality {high,medium,low}`: Quality of the resized images (default: high)

### Example

```bash
python image_scale.py my_icon.png MyAppIcons --quality high
```

This will generate all the required iOS app icon sizes in the `MyAppIcons/ios` directory along with a Contents.json file for Xcode.

## Generated Icon Sizes

The script generates the following iOS app icon sizes:

### iPhone Icons

| Size (points) | Scale | Actual Size (pixels) | Usage |
|--------------|-------|----------------------|-------|
| 60x60 | @3x | 180x180 | App Icon |
| 60x60 | @2x | 120x120 | App Icon |
| 40x40 | @3x | 120x120 | Spotlight |
| 40x40 | @2x | 80x80 | Spotlight |
| 29x29 | @3x | 87x87 | Settings |
| 29x29 | @2x | 58x58 | Settings |
| 20x20 | @3x | 60x60 | Notification |
| 20x20 | @2x | 40x40 | Notification |

### iPad Icons

| Size (points) | Scale | Actual Size (pixels) | Usage |
|--------------|-------|----------------------|-------|
| 83.5x83.5 | @2x | 167x167 | App Icon (iPad Pro) |
| 76x76 | @2x | 152x152 | App Icon |
| 40x40 | @2x | 80x80 | Spotlight |
| 40x40 | @1x | 40x40 | Spotlight |
| 29x29 | @2x | 58x58 | Settings |
| 29x29 | @1x | 29x29 | Settings |
| 20x20 | @2x | 40x40 | Notification |
| 20x20 | @1x | 20x20 | Notification |

### App Store

| Size (points) | Scale | Actual Size (pixels) | Usage |
|--------------|-------|----------------------|-------|
| 1024x1024 | @1x | 1024x1024 | App Store |

## Xcode Integration

The script generates a Contents.json file that allows you to easily import the icons into Xcode:

1. Generate the icons using this script
2. In Xcode, open your project's asset catalog
3. Right-click and select "New App Icon"
4. Delete the default AppIcon set
5. Copy the contents of the generated `ios` directory into your AppIcon.appiconset directory

## Notes

- The input image should be square and at least 512x512 pixels (1024x1024 recommended)
- Images between 512x512 and 1024x1024 will be automatically upscaled
- If the input image is not square, it will be automatically cropped from the center
- All generated icons are optimized PNG files
- The high-quality setting uses the Lanczos resampling algorithm for best results
- Upscaling always uses the Lanczos algorithm regardless of quality setting
