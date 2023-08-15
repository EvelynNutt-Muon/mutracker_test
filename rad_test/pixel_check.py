"""
Just some psuedo code + notes:

Move raw images from RPi to PC. Don't need to take any new images.
Move dark frames from RPi to PC. 
Set file paths for raw image folder & dark frames.
Make new path (and/or folder) for anomaly image.
For each raw images, check for dead and hot pixels.
If dead or hot pixel is detected, display an image highlighting that pixel.
Keep the one image and update as code runs through the whole file.
Edge case: see if pixels change before and after a power cycle event.
Edge case: see if pixels 'recovered' by the end of the rad test.
Edge case: characterize the noise from beam on.
What raw values do the pixels show when hit by the beam?
How does radiation noise impact Mutracker outputted orientation?
Based on results, determine if Mutracker OV2311 is fly-able.

"""


import os
import argparse
from PIL import Image


DESCRIPTION = """
Python3 script for checking Mutracker dead and hot pixels.
"""


def generate_anomaly_pixel_highlight(input_image_path, dark_frame_paths, dead_threshold, hot_threshold, dead_highlight_color, hot_highlight_color):
    # Load the input image and dark frames.
    input_image = Image.open(input_image_path)
    dark_frames = [Image.open(path) for path in dark_frame_paths]

    # Convert all dark grames to the same mode as the input image.
    mode = input_image.mode
    dark_frames = [frame.convert(mode) for frame in dark_frames]

    # Calculate the mean dark frame.
    mean_dark_frame = Image.blend(dark_frames[0], dark_frames[1], alpha=1.0 / len(dark_frames))

    # Subtract the mean dark frame from the input image.
    corrected_image = Image.blend(input_image, mean_dark_frame, alpha=-1.0)

    # Convert the image to grayscale for easier pixel analysis.
    grayscale_image = corrected_image.convert("L")

    # Identify dead and hot pixels based on the threshold.
    dead_pixel_coordinates = []
    hot_pixel_coordinates = []
    for y in range(grayscale_image.height):
        for x in range(grayscale_image.width):
            pixel_value = grayscale_image.getpixel((x,y))
            if pixel_value <= dead_threshold:
                dead_pixel_coordinates.append((x,y))
            if pixel_value >= hot_threshold:
                hot_pixel_coordinates.append((x,y))

    # Generate a new image with dead and hot pixels highlighted.
    highlight_image = input_image.copy()
    highlight_pixels = highlight_image.load()
    for coord in dead_pixel_coordinates:
        highlight_pixels[coord] = dead_highlight_color
    for coord in hot_pixel_coordinates:
        highlight_pixels[coord] = hot_highlight_color

    return highlight_image

def pixel_check(raw_dir, anom_dir):
    # Anomaly dir setup, one time use.
    anomaly_folder_path = '{}/{}/'.format(anom_dir, "anomaly-detected").replace('//','/')
    # os.makedirs(anomaly_folder_path)

    # Create new image filepath.
    anomaly_file_path = '{}{}.{}'.format(anomaly_folder_path, "anom", anom_dir)

    # Loop through each raw image from rad test and highlight detected anomaly pixels.
    for filename in os.listdir(raw_dir):
        # Construct the full path to the image.
        raw_path = os.path.join(raw_dir, filename)
        dark_frame_paths = ["C:\\Users\\Evelyn Nutt\\Downloads\\anomaly_img\\darkframes\\0.png","C:\\Users\\Evelyn Nutt\\Downloads\\anomaly_img\\darkframes\\1.png"]
        # Create new anomaly image filepath.
        anomaly_file_path = '{}{}.{}'.format(anomaly_folder_path, filename, anom_dir)
        # Highlight dead and hot pixels.
        highlight_image = generate_anomaly_pixel_highlight(raw_path, dark_frame_paths, 10, 245, (128,0,128), (255,0,0))
        highlight_image.save(anomaly_file_path)

    highlight_image.show()

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--dir', type=str, default = "C:\\Users\\Evelyn Nutt\\Downloads\\0811_radtest_png", help='Path to store RadTest png images')
    parser.add_argument('--anom', type=str, default = "C:\\Users\\Evelyn Nutt\\Downloads\\anomaly_img", help='Path to store RadTest anomaly images')
    args = parser.parse_args()
    pixel_check(args.dir, args.anom)

if __name__ == "__main__":
    main()