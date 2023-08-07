from rad_test.run_radtest import EXPOSURE_REG_VALUE, RESOLUTION_H, RESOLUTION_W
import v4l2
import time
import os
import sys
from PIL import Image
from datetime import datetime
import arducam_mipicamera as arducam
from pathlib import Path 
import argparse

DESCRIPTION = """
Python3 script for running the MuTracker Image Sensor RadTest, which takes an image every 10 seconds.
"""

EXPOSURE_REG_VALUE = 64600 # This value was determined by experiment and corresponds to an exposure of 0.2s
RESOLUTION_W = 1600
RESOLUTION_H = 1300
MAX_FS_USAGE = 80

def init_camera():
    """
    Initialization routine for the MIPI Arducam.
    """
    camera = arducam.mipi_camera()
    camera.init_camera()
    camera.set_resolution(RESOLUTION_W, RESOLUTION_H)
    camera.software_auto_exposure(enable=False)
    camera.set_control(v4l2.V4L2_CID_EXPOSURE, EXPOSURE_REG_VALUE)
    return camera

def init_camera_auto():
    """
    Initialization routine for the MIPI Arducam using auto exposure settings.
    """
    camera = arducam.mipi_camera()
    camera.init_camera()
    camera.set_resolution(RESOLUTION_W, RESOLUTION_H)
    camera.software_auto_exposure(enable=True)
    return camera

def disk_usage(path):
    """
    Return disk usage statistics about the given path.
    Returned values are 'total', 'used', and 'free', which are the amount of total, used, and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return total, used, free

def generate_anomaly_pixel_highlight(input_image_path, dark_frame_paths, dead_threshold, hot_threshold, dead_highlight_color, hot_highlight_color):
    # Load the input image and dark frames.
    input_image = Image.open(input_image_path)
    dark_frames = [Image.open(path) for path in dark_frame_paths]

    # Calculate the mean dark frame.
    mean_dark_frame = Image.blend(*dark_frames, alpha=1.0 / len(dark_frames))

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

def run_radtest(image_dir, image_anom, image_fmt):
    # Date dir setup.
    now = datetime.now()
    current_time = now.isoformat()
    folder_path = '{}/{}/'.format(image_dir, current_time).replace('//','/')
    anomaly_folder_path = '{}/{}/'.format(image_anom, current_time).replace('//','/')
    os.makedirs(folder_path)
    os.makedirs(anomaly_folder_path)

    # Initialize camera
    camera = init_camera_auto()
    time.sleep(1)

    while (True):
        # Check diskspace before taking an image.
        total, used, free = disk_usage('/')
        percent_used = 100*used/total
        if percent_used > MAX_FS_USAGE:
            sys.exit("Filesystem usage exceeds program's allowed MAX_FS_USAGE")
        
        # Create new image filepaths.
        now = datetime.now()
        current_time = now.isoformat()
        file_path='{}{}.{}'.format(folder_path,current_time,image_fmt)
        anomaly_file_path='{}{}.{}'.format(anomaly_folder_path,current_time,image_anom)

        # Capture and save image.
        frame = camera.capture(encoding=image_fmt)
        frame.as_array.tofile(file_path)

        # Find and alert dead and hot pixels.
        input_image_path = file_path
        dark_frame_paths = ["path/to/dark_frame1.jpg","path/to/dark_frame2.jpg"]
        highlight_image = generate_anomaly_pixel_highlight(input_image_path, dark_frame_paths, 10, 245, (128,0,128), (255,0,0))
        highlight_image.save(anomaly_file_path)

        # Release memory.
        del frame

        # Also save a png image if image type selected was raw.
        if image_fmt == 'raw':
            raw_data = open(file_path,'rb').read()
            img_size = (RESOLUTION_W, RESOLUTION_H)
            img = Image.frombytes('L', img_size, raw_data)
            img.save(file_path.replace('raw','png'))
        
        # Wait 10s to take next image.
        time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--dir', type=str, default='/home/pi/mutracker_proto/radtest_data/', help='Path to store RadTest images')
    parser.add_argument('--anom', type=str, default='/home/pi/mutracker_proto/radtest_data/anomaly_images', help='Path to store RadTest anomaly images')
    parser.add_argument('--fmt', type=str, default='raw', choices=['raw','jpeg','i420'], help='Image format')
    args = parser.parse_args()
    run_radtest(args.dir, args.anom, args.fmt)


if __name__ == "__main__":
    main()