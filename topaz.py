#!/usr/bin/env python3

import click
import subprocess
import json
import os


def get_metadata(stream_path):
    probe = subprocess.check_output(['ffprobe', '-v', 'quiet', '-select_streams', 'v:0',
                                     '-show_entries', 'stream=duration,avg_frame_rate', '-of', 'json=c=1', stream_path])
    data = json.dumps(probe.decode('utf-8'))
    data = json.loads(data)

    return data


def extract_fps(fps_fraction):
    x1, x2 = fps_fraction.split("/")
    fps = float(x1) / float(x2)

    return fps


@click.command()
@click.argument(
    'stream_path', type=click.Path(exists=True, resolve_path=True), nargs=1
)
@click.argument('target_frame_num', type=click.INT, nargs=1)
def extract_frames(stream_path, target_frame_num):
    metadata = json.loads(get_metadata(stream_path))

    duration = float(metadata["streams"][0]["duration"])
    fps = extract_fps(metadata["streams"][0]["avg_frame_rate"])

    total_frames = fps * duration
    target_fps = target_frame_num / duration

    parent_dir, filename = os.path.split(str(stream_path))
    filename = os.path.splitext(filename)
    out_dir = os.path.join((str(parent_dir)), 'frames/', str(filename[0]))

    if os.path.isdir(str(out_dir)) and os.listdir(str(out_dir)):
        for file in os.listdir(str(out_dir)):
            os.remove(str(os.path.join(str(out_dir), str(file))))

    if not os.path.isdir(str(out_dir)):
        os.makedirs(str(out_dir))

    if target_frame_num > total_frames:
        raise ValueError()

    if target_frame_num == total_frames:
        subprocess.run(['ffmpeg', '-i', str(stream_path), '-r', str(fps),
                        '-f', 'image2', f'{str(out_dir)}/frame_%05d.jpeg'])
        return 0
    else:
        subprocess.run(['ffmpeg', '-i', str(stream_path), '-r', str(target_fps),
                        '-f', 'image2', f'{str(out_dir)}/frame_%05d.jpeg'])
        return 0


if __name__ == "__main__":
    try:
        extract_frames()
    except ValueError:
        print(
            "Target number of frames exceeds total number of source frames")
