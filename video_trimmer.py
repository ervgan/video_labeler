from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import sys

def video_trimmer():
	ffmpeg_extract_subclip(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), targetname=sys.argv[4])

video_trimmer()


