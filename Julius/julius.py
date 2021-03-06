import subprocess

# 日本語のパスはエラーがでる
julius      = "C:/Julius/julius-4.6-win32bin/bin/julius.exe"
main        = "C:/Julius/dictation-kit-4.5/main.jconf"
am_dnn      = "C:/Julius/dictation-kit-4.5/am-dnn.jconf"
julius_dnn  = "C:/Julius/dictation-kit-4.5/julius.dnnconf"

input_audio_file  = "input.wav"

args = [julius, "-C", main, "-C", am_dnn, "-dnnconf", julius_dnn, "-input", "rawfile", "-cutsilence"]

p = subprocess.run(args, stdout=subprocess.PIPE, input=input_audio_file, text=True)
print(p.stdout)
output = p.stdout.split("### read waveform input")[1].split("\n\n")
for i in output:
    if "sentence1:" not in i:
        continue
    sentence = i.split("sentence1:")[1].split("\n")[0].replace(" ", "")
    print(sentence)