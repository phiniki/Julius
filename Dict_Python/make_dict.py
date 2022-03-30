from pykakasi import kakasi
import subprocess

dict_name = 'mydict'

kakasi = kakasi()

def make_yomi():
    f = open('word_list.txt', 'r')
    data = f.read()
    f.close()

    yomi_list = []
    for i in data.split('\n'):
        kakasi.setMode('J', 'H') #漢字からひらがなに変換
        kakasi.setMode("K", "H") #カタカナからひらがなに変換
        conv = kakasi.getConverter()
        yomi_list.append(i + '\t' + conv.do(i)) #[単語] + [Tab] + [ひらがな]

    yomi = '\n'.join(yomi_list)

    f = open(dict_name + '.yomi', 'w')
    f.write(yomi)
    f.close()

def make_phone():
    yomi2voca = 'C:/Julius/julius-4.6-win32bin/bin/yomi2voca.pl'
    cmd = "perl {0} ./{1} > ./{2}".format(yomi2voca, dict_name + '.yomi', dict_name + '.phone')
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def make_grammar():
    f = open(dict_name + '.phone', 'r')
    data = f.read()
    f.close()

    grammar = ['S : NS_B WORD NS_E']
    for i in data.split('\n')[:-1]:
        word = i.split('\t')[1].upper().replace(' ', '') #すべて大文字に変換、スペース削除
        grammar.append('WORD : ' + word)

    grammar = '\n'.join(grammar)

    f = open(dict_name + '.grammar', 'w')
    f.write(grammar)
    f.close()

def make_voca():
    f = open(dict_name + '.phone', 'r')
    data = f.read()
    f.close()

    voca = []
    for i in data.split('\n')[:-1]:
        word = i.split('\t')[1].upper().replace(' ', '') #すべて大文字に変換、スペース削除
        voca.append('% ' + word + '\n' + i)
    voca.append('% NS_B')
    voca.append('[s] silB')
    voca.append('% NS_E')
    voca.append('[/s]    silE')

    voca = '\n'.join(voca)

    f = open(dict_name + '.voca', 'w')
    f.write(voca)
    f.close()

def make_dict():
    mkdfa = 'C:/Julius/julius-4.6-win32bin/bin/mkdfa.pl'
    cmd = "perl {0} {1}".format(mkdfa, dict_name)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

make_yomi()
make_phone()
make_grammar()
make_voca()
make_dict()
