import subprocess
import os

def srilm(srilm_path, input_corpus, output_language_model, output_ngram):
    path = os.getcwd().replace(os.sep,'/')+"/" # 実行中のパス取得
    cmd = "{0} -text {1} -lm {2} -order 3 -write {3}".format(srilm_path, path+input_corpus, path+output_language_model, path+output_ngram)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

if __name__ == '__main__':
    srilm_path = "C:/cygwin64/srilm/bin/cygwin64/ngram-count"
    input_corpus = "corpus.txt"
    output_language_model = "lm.txt"
    output_ngram = "count.txt"

    srilm(srilm_path, input_corpus, output_language_model, output_ngram)










