import os
import time
import ffmpeg
import tkinter as tk
from tkinter import filedialog

def transcode_video(input_file, output_file, cq=20, preset='medium'):
    """Transcode a single video file with retry logic."""
    max_retries = 5
    retry_delay = 20  # 1 minute in seconds
    
    for attempt in range(max_retries):
        try:
            print(f'Transcoding {input_file} to {output_file}... (Attempt {attempt + 1})')
            (
                ffmpeg
                .input(input_file)
                .output(output_file, vcodec='av1_nvenc', cq=cq, preset=preset)
                .global_args('-y', '-hwaccel', 'cuda')
                .run()
            )
            print(f'Successfully transcoded {input_file} to {output_file}')
            return  # Exit the function if successful
        except ffmpeg.Error as e:
            print(f'Error transcoding {input_file}: {e}')
            if attempt < max_retries - 1:
                print(f'Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)
            else:
                print(f'Failed to transcode {input_file} after {max_retries} attempts.')

def transcode_videos(input_dir, output_dir, cq=20, preset='medium'):
    """Recursively transcode all videos in the input directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    folder_name = os.path.basename(input_dir.rstrip(os.sep))
    output_folder = os.path.join(output_dir, folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        if os.path.isdir(item_path):
            transcode_videos(item_path, output_folder, cq, preset)
        elif item.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v')):
            output_file = os.path.join(output_folder, os.path.splitext(item)[0] + '_transcoded.mp4')
            if os.path.exists(output_file):
                print(f'Skipping {output_folder}, already exists as {output_file}')
                continue
            transcode_video(item_path, output_file, cq, preset)

def select_directory(title):
    """Open a dialog to select a directory."""
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title)
    root.destroy()
    return folder_path

if __name__ == "__main__":
    print("Please select the input directory containing videos to transcode.")
    input_directory = select_directory("Select Input Directory")
    
    if input_directory:
        print(f'Selected input directory: {input_directory}')
        
        print("Please select the output directory for transcoded videos.")
        output_directory = select_directory("Select Output Directory")
        
        if output_directory:
            print(f'Selected output directory: {output_directory}')
            transcode_videos(input_directory, output_directory)
        else:
            print("No output directory selected. Exiting.")
    else:
        print("No input directory selected. Exiting.")
