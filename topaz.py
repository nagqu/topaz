#!/usr/bin/env python

#import commands.py
import subprocess
import json
import os


def get_metadata(stream_path):
    probe = subprocess.check_output(['ffprobe', '-v', 'quiet', '-select_streams', 'v:0', '-show_entries', 'stream=duration,avg_frame_rate', '-of', 'json=c=1', stream_path])
    data = json.dumps(probe.decode('utf-8'))
    data = json.loads(data)
    return data


def extract_frames(stream_path, target_frame_num):
    metadata = json.loads(get_metadata(stream_path))
    fps = int(eval(metadata["streams"][0]["avg_frame_rate"]))
    duration = float(metadata["streams"][0]["duration"])
    total_frames = fps * duration
    target_fps = target_frame_num / duration
    parent_dir, filename = os.path.split(str(stream_path))
    filename = os.path.splitext(filename)
    out_dir = os.path.join((str(parent_dir)), 'frames/', str(filename[0]))

    if not os.path.isdir(str(out_dir)):
        os.makedirs(str(out_dir))
    
    
    if target_frame_num > total_frames:
        raise Exception("Target number of frames exceeds total number of source frames.")
    
    if target_frame_num == total_frames:
        subprocess.run(['ffmpeg', '-i', str(stream_path), '-r', str(fps), '-f', 'image2', f'{str(out_dir)}/frame_%05d.jpeg'])
        return 0
    else:
        subprocess.run(['ffmpeg', '-i', str(stream_path), '-r', str(target_fps), '-f', 'image2', f'{str(out_dir)}/frame_%05d.jpeg'])
        return 0


extract_frames("/mnt/c/Users/glassforms/Documents/Scripts/topaz/example.mov", 100)
