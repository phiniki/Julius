import subprocess
import time
import os

path = os.getcwd().replace(os.sep,'/')+"/" # 実行中のパス取得

srilm_path = "C:/cygwin64/srilm/bin/cygwin64/ngram-count"
mkbingram = "C:/Julius/julius-4.6-win32bin/bin/mkbingram.exe"

input_sentence = 'sentence.txt'
corpus = 'corpus.txt'
reversal_corpus = 'reversal_corpus.txt'
forward_n_gram = "forward_n-gram.arpa"
backward_n_gram = "backward_n-gram.arpa"
bingram = "n-gram.bingram"

def strip_cmd_injection(instr):
    inj = [";", "|", "&", "`", "(", ")", "$", "<", ">", "*", "?", "{", "}", "[", "]", "!", "？", "！", "「", "」", "\n"]
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

def make_corpus():
    f = open(input_sentence, 'r')
    lines = f.read().split('\n')
    f.close()

    Words = []
    for line in lines:
        if line == "" or line == " ":
            continue
        words = []
        for cha in chasen(line):
            words.append(cha[0])
        Words.append(" ".join(words).replace("。 ", "。\n"))

    f = open(corpus, 'w')
    f.write("\n".join(Words))
    f.close()

def make_reversal_corpus():
    f = open(corpus, 'r')
    lines = f.read().split('\n')
    f.close()

    Words = []
    for line in lines:
        Words.append(" ".join(line.split(" ")[::-1]))

    f = open(reversal_corpus, 'w')
    f.write("\n".join(Words))
    f.close()

def make_forward_n_gram():
    cmd = "{0} -order 2 -text {1} -unk -lm {2}".format(srilm_path, path+corpus, path+forward_n_gram)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

def make_backward_n_gram():
    cmd = "{0} -order 3 -text {1} -unk -lm {2}".format(srilm_path, path+reversal_corpus, path+backward_n_gram)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

def make_mkbingram():
    cmd = "{0} -nlr {1} -nlr {2} {3}".format(mkbingram, path+forward_n_gram, path+backward_n_gram, path+bingram)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

if __name__ == '__main__':
    make_corpus()
    make_reversal_corpus()
    make_forward_n_gram()
    make_backward_n_gram()
    make_mkbingram()










