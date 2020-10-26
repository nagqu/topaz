# topaz - it be makin frames

topaz is a small script which turns your video into (almost) desired number of frames



## requirements:
* click
* ffmpeg (with ffprobe)



## usage:

```./topaz.py [path to file] [number of frames] ```

script works on linux and WSL (tested). not sure about mac but probably works too.

## to do:
* idk try to get rid of eval or sanitize the input somehow (values for the fps can be wild)
* maybe more options if i come up with them