# iOS App Icon Generator

A simple Python script to generate all the necessary icon sizes required for an iOS application.

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
python image_scale.py input_image.png [output_directory]
```

### Arguments

- `input_image.png`: Path to the input image (preferably a 1024x1024 PNG)
- `output_directory` (optional): Directory to save the generated icons (default: `./AppIcons`)

### Example

```bash
python image_scale.py my_icon.png MyAppIcons
```

This will generate all the required iOS app icon sizes in the `MyAppIcons` directory.

## Generated Icon Sizes

The script generates the following iOS app icon sizes:

| Size (pixels) | Description |
|---------------|-------------|
| 1024x1024 | App Store |
| 180x180 | iPhone App Icon @3x |
| 167x167 | iPad Pro App Icon |
| 152x152 | iPad, iPad mini App Icon |
| 120x120 | iPhone App Icon @2x / iPhone Spotlight @3x |
| 87x87 | iPhone Settings @3x |
| 80x80 | iPhone/iPad Spotlight @2x |
| 76x76 | iPad App Icon @1x |
| 60x60 | iPhone App Icon @1x |
| 58x58 | iPhone/iPad Settings @2x |
| 40x40 | iPhone/iPad Spotlight @1x |
| 29x29 | iPhone/iPad Settings @1x |
| 20x20 | iPhone/iPad Notification @1x |

## Notes

- The input image should ideally be square and at least 1024x1024 pixels
- If the input image is not square, it will be cropped from the center
- All generated icons are in PNG format
