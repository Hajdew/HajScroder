import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog

def transcode_videos(input_dir, output_dir, cq=20, preset='medium'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the base name of the input directory
    folder_name = os.path.basename(input_dir.rstrip(os.sep))
    
    # Create a subdirectory in the output directory with the same name as the input folder
    output_folder = os.path.join(output_dir, folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Scan the input directory and process videos
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        if os.path.isdir(item_path):
            # Recursively process subdirectories
            transcode_videos(item_path, output_folder, cq, preset)
        elif item.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v')):  # Add more video formats if needed
            input_file = item_path
            output_file = os.path.join(output_folder, os.path.splitext(item)[0] + '_transcoded.mp4')
            
            try:
                print(f'Transcoding {input_file} to {output_file}...')
                (
                    ffmpeg
                    .input(input_file)
                    .output(output_file, vcodec='av1_nvenc', cq=cq, preset=preset)
                    .global_args('-y', '-hwaccel', 'cuda')
                    .run()
                )
                print(f'Successfully transcoded {input_file} to {output_file}')
            except ffmpeg.Error as e:
                print(f'Error transcoding {input_file}: {e.stderr.decode("utf-8")}')

def select_directory(title):
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
