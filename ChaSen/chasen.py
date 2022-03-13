import subprocess
import time

def strip_cmd_injection(instr):
    inj = [";", "|", "&", "`", "(", ")", "$", "<", ">", "*", "?", "{", "}", "[", "]", "!", "\n"]
    for s in inj:
        instr = instr.replace(s, "")
    instr = instr.replace("", "")
    return instr

def chasen(arg):
    arg = strip_cmd_injection(arg)
    cmd = "echo {0} | chasen -iw".format(arg)
    subprocess.Popen("chcp 65001", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.1) # chcp 65001の反映待ち
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if stderr != b'':
        raise(Exception(stderr.decode('utf-8')))

    try:
        lines = stdout.decode('utf-8').split("\n")
    except:
        raise(Exception(stderr.decode('utf-8')))

    for line in lines:
        if (line == "EOS"):
            break
        yield line.split("\t")

if __name__ == '__main__':
    line = "'テストです。出来ていますか？'"
    for cha in chasen(line):
        print(cha)










