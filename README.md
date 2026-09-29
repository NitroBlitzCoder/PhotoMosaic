# Photo Mosaic Generator

A local Python program that recreates a target image using a collection of smaller photographs. The program divides the target into a grid, compares the color of each grid section with the available source images, selects the closest match, adjusts its color, and places it into the final mosaic.

## Features

- Loads a target image from a user-provided file path
- Loads source images from a selected folder
- Crops source images into squares without stretching them
- Resizes every source image to a consistent tile size
- Converts colors to the LAB color space for perceptual color comparison
- Matches each target region to the source image with the closest average color
- Adjusts source-image colors to better resemble the target
- Displays progress while the mosaic is being generated
- Saves the completed mosaic as a PNG image

## How It Works

1. The user provides the path to a target image.
2. The user provides a folder containing source images.
3. Each source image is center-cropped and resized into a square tile.
4. The program calculates the average LAB color of every source tile.
5. The target is cropped so its dimensions divide evenly by the tile size.
6. The target is divided into square regions.
7. For each region, the program finds the source tile with the smallest LAB color distance.
8. The selected tile is tinted toward the target region's color.
9. All selected tiles are combined and saved as one mosaic image.

## Project Structure

```text
photomosaic/
├── images/
│   ├── target.png
│   └── tiles/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── image3.jpg
├── output/
├── mosaic.py
├── image_utils.py
├── matcher.py
├── color_transfer.py
├── requirements.txt
└── README.md
```

### Files

- `mosaic.py`: Runs the program and assembles the final mosaic.
- `image_utils.py`: Loads, crops, resizes, and analyzes images.
- `matcher.py`: Compares LAB colors and selects the closest source tile.
- `color_transfer.py`: Adjusts a selected tile toward the target region's color.
- `requirements.txt`: Lists the Python packages required by the project.

## Requirements

- Python 3.9 or newer
- NumPy
- OpenCV
- tqdm

## Installation

Clone or download the project, then open a terminal inside its folder.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
numpy
opencv-python
tqdm
```

## Usage

Run the program from the project directory:

```bash
python3 mosaic.py
```

When prompted, enter the path to the target image:

```text
Import the target image by entering its path: images/target.png
```

Then enter the path to the source-image folder:

```text
Enter the folder containing the source images: images/tiles
```

The finished mosaic will be saved as:

```text
output/mosaic.png
```

On macOS, an image or folder can also be dragged from Finder into the Terminal window to insert its path.

## Configuration

The main settings are stored near the top of `mosaic.py`:

```python
TILE_SIZE = 40
COLOR_STRENGTH = 0.35
```

### Tile size

`TILE_SIZE` controls the width and height of each tile in pixels.

- A smaller tile size creates more tiles and usually makes the target easier to recognize.
- A larger tile size makes the individual source photographs easier to see.

### Color strength

`COLOR_STRENGTH` controls how strongly each source tile is tinted toward the corresponding target region.

- `0.0`: no color adjustment
- `0.35`: moderate adjustment
- `1.0`: maximum adjustment

Values between `0.25` and `0.50` usually provide a reasonable balance.

## Color Matching

The program compares colors in LAB color space instead of directly comparing RGB values. LAB color distance generally represents perceived color differences more effectively.

For two LAB colors, the basic distance is:

```text
distance = sqrt((L1 - L2)^2 + (a1 - a2)^2 + (b1 - b2)^2)
```

The source image with the lowest distance is selected for the target region.

## Testing

Start with a small target image, such as `400 x 400` pixels, and 10 to 30 source images with noticeably different dominant colors.

Useful tests include:

- Confirming that every prepared source tile has the expected dimensions
- Checking that the target dimensions are divisible by `TILE_SIZE` after cropping
- Confirming that a red target region matches a mostly red source image
- Trying invalid file paths and empty source folders
- Comparing results with different tile sizes and color strengths
- Checking that `output/mosaic.png` exists and has the expected dimensions

## Current Limitations

- Matching currently uses average color, so it does not compare objects, shapes, or image meaning.
- The same source image may be selected many times.
- Large target images or large source collections may take longer to process.
- Images smaller than the configured tile size require validation or resizing.
- Source images must use a supported format such as PNG, JPG, JPEG, or WebP.

## Possible Improvements

- Add reuse penalties to prevent one source image from appearing too often
- Prevent identical images from being placed next to each other
- Cache processed tiles and color values for faster repeated runs
- Compare color histograms instead of only average colors
- Add edge or texture matching
- Add a local graphical file picker with Tkinter
- Add a Streamlit interface for local browser-based use
- Allow rectangular tiles and custom output resolutions
- Use image embeddings for semantic matching

## License

This project is intended for educational and portfolio use. Add a license file before distributing or accepting outside contributions.
