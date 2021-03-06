''' KryptoMagick Fetu Calculator '''
''' (Uvajda) - 2021 '''
''' Version 'AA' '''
''' This calculator provides the basic Fetu functions '''

def double(word):
    dbl = []
    for w in word:
        d = (w + w) % 26
        dbl.append(d)
    return dbl

def fetu_value(word):
    f = 0
    for w in word:
        f += w
    f += 1
    weight = int(f / (len(word)) + 1)
    return f, weight

def contruct_hword(word_obj):
    wrd = [0, 0, 0, 0]
    wrd[0] = word_obj.ftu % 2
    wrd[1] = ((word_obj.ftu % 2) + (word_obj.ftu_val % 2)) % 2
    wrd[2] = word_obj.ftu_weight % 2
    wrd[3] = word_obj.ftu_residue % 2
    val = 0
    for w in wrd:
        if w == 0:
            val += 1
    ftu = len(wrd) + 1
    return wrd, ftu, val

class HWord:
    def __init__(self, word_obj):
        wrd, ftu, val = contruct_hword(word_obj)
        self.wrd = wrd
        self.ftu = ftu
        self.val = val

class Word:
    def __init__(self, word):
        self.wrd = []
        for w in word:
            self.wrd.append(ord(w) - 65)
        self.ftu = len(self.wrd) + 1
        self.dbl = double(self.wrd)
        self.tri = double(self.dbl)
        self.qua = double(self.tri)

        self.ftu_val, self.ftu_weight = fetu_value(self.wrd)
        self.ftu_residue = self.ftu_weight % self.ftu
        self.hword = HWord(self)

def process_text(text):
    record = []
    for line in text.split('\n'):
        for word in line.split():
            record.append(Word(word))
    return record

def write_record(record, output_filename):
    f = open(output_filename, "w")
    for word in record:
        f.write("Fetu Word: "+str(word.wrd)+"\n")
        f.write("Fetu FTU: "+str(word.ftu)+"\n")
        f.write("Fetu Dbl: "+str(word.dbl)+"\n")
        f.write("Fetu Tri: "+str(word.tri)+"\n")
        f.write("Fetu Qua: "+str(word.qua)+"\n")
        f.write("Fetu FTU Val: "+str(word.ftu_val)+"\n")
        f.write("Fetu FTU Weight: "+str(word.ftu_weight)+"\n")
        f.write("Fetu FTU Residue: "+str(word.ftu_residue)+"\n")
        f.write("Fetu HWord Word: "+str(word.hword.wrd)+"\n")
        f.write("Fetu HWord FTU: "+str(word.hword.ftu)+"\n")
        f.write("Fetu HWord Val: "+str(word.hword.val)+"\n\n")
    f.close()

def fetu_scroll(
