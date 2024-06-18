# Advanced Image Editor

## Overview
This Python application implements an advanced image editor GUI using tkinter. It allows users to upload images, apply various filters and enhancements, perform image operations like crop and rotate, add text to images, and save/download the processed images.

## Features
- **Image Upload**: Allows users to upload images (supports .jpg, .jpeg, .png formats).
- **Filter Functions**: Apply filters such as Blur, Sharpen, Grayscale, Sepia, Negative, Vivid, Grainy, and Normal.
- **Enhancement Sliders**: Adjust image attributes like Brightness, Contrast, Color, Sharpness, and Blur Amount using sliders.
- **History Management**: Supports Undo and Redo operations for multiple steps in image editing.
- **Save and Download**: Save edited images locally in .png or .jpg/.jpeg formats and download them.
- **Comparison View**: Provides a side-by-side view of the original and processed images.
- **Text Overlay**: Allows users to add custom text to images with options for font size, type, and position.
- **Crop and Rotate**: Perform cropping and rotation operations on images.

## Dependencies
- Python 3.x
- Libraries:
  - tkinter
  - PIL (Pillow)

## Usage
1. **Installation**:
   - Ensure Python 3.x is installed.
   - Install Pillow library using pip:
     ```
     pip install Pillow
     ```

2. **Execution**:
   - Run the `app.py` script.
   - Use the "Upload Image" button to load an image for editing.

3. **Editing Features**:
   - **Filters**: Click on filter buttons to apply effects like Blur, Grayscale, Sepia, etc.
   - **Enhancements**: Use sliders to adjust attributes such as Brightness, Contrast, etc.
   - **Operations**: Crop, Rotate, and Add Text buttons perform respective operations on the image.

4. **Saving and Downloading**:
   - Use "Save" button to save the current edited image.
   - Use "Download" button to save the edited image with a new filename.

5. **Undo/Redo**:
   - Click "Undo" or "Redo" buttons to navigate through editing history.

6. **Comparison View**:
   - Click "Before and After" to view the original and processed images side by side.

7. **Exiting**:
   - Close the application window to exit.

## Contributing
Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## Acknowledgments
- Built using tkinter for GUI development.
- Uses Pillow library for image processing capabilities.
