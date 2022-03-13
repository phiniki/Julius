import subprocess

input_file = "input.mp4"
output_file = "output.wav"

args = ["ffmpeg", "-i", input_file, "-ar", "16000", "-ac", "1", output_file]

subprocess.run(args, stdout=subprocess.PIPE)