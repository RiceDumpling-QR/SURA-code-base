from moviepy.editor import VideoFileClip
# pip install moviepy

video = VideoFileClip("happy daddys day [ae379a95-8994-46ee-83f7-bf0c4bdde5d9].mp4")
#path to the mp4 file
video.audio.write_audiofile("test_audio.wav")
#path to the wav file
