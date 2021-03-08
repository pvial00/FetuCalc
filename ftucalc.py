''' KryptoMagick Fetu Calculator '''
''' (Uvajda) - 2021 '''
''' Version 'AD' '''
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

def binary_sum(h):
    v = 0
    if h[0] == 1:
        v += 8
    if h[1] == 1:
        v += 4
    if h[2] == 1:
        v += 2
    if h[3] == 1:
        v += 1
    return v

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
    wrd_val = binary_sum(wrd)
    return wrd, wrd_val, ftu, val

class HWord:
    def __init__(self, word_obj):
        wrd, wrd_val, ftu, val = contruct_hword(word_obj)
        self.wrd = wrd
        self.wrd_val = wrd_val
        self.ftu = ftu
        self.val = val

class Word:
    def __init__(self, word):
        self.name = word
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

def fetu_residue_frequency(record):
    last = -1
    c = 0
    max_period = -1
    periods = []
    total = 0
    for r in record:
        if r.ftu_residue == last:
            #periods.append((r.ftu_residue, c))
            periods.append(c)
            c = 0
        else:
            c += 1
        last = r.ftu_residue
    for period in periods:
        if period > max_period:
            max_period = period
        total += period
    avg_period = int(total / len(periods))
    return periods, max_period, avg_period

def fetu_avg_weight(record):
    weights = 0
    for r in record:
         weights += r.ftu_weight
    avg = int(weights / len(record))
    return avg

def fetu_min_max_value(record):
    last = -1
    mn = 10000
    total = 0
    for r in record:
         val = r.ftu_val
         total += val
         if val > last:
             last = val
         if val < mn:
             mn = val
    return mn, last, total

def fetu_footprint(max_period, fetu_min_value, fetu_max_value, fetu_total, record):
    footprint = pow(fetu_max_value, max_period, fetu_total)
    for r in record:
        footprint = pow(footprint, max_period, fetu_total)
    return footprint

def fetu_binary_footprint(footprint, fetu_total, record):
    binary_footprint = fetu_total
    for r in record:
        binary_footprint = pow(binary_footprint, (r.hword.wrd_val + 1), footprint)
    return binary_footprint

def fetu_binary_mark(record):
    mark = 0
    for r in record:
        mark = (mark + r.hword.wrd_val) & 0xF
    return mark

def fetu_binary_message(record):
    bin_msg = []
    bin_msg_sum = 0
    for r in record:
        bin_msg.extend(r.hword.wrd)
        bin_msg_sum += r.hword.wrd_val
    return bin_msg, bin_msg_sum

def FermatPrimeTest(n):
    t = int(n / 2)
    r = pow(t, (n - 1) , n)
    if r == 1:
        return True
    else:
        return False

def generate_primes(val_total, bin_footprint):
    p = val_total
    q = bin_footprint
    while not FermatPrimeTest(p):
        p += 1
    while not FermatPrimeTest(q):
        q += 1
    return p, q

def generate_fetu_keys(footprint, bin_footprint, mark, bin_sum, val_total, max_period, max_value):
    secret_modulus = 0
    secret_key = 0
    p, q = generate_primes(val_total, bin_footprint)
    n = p * q

    phaseA0 = pow(max_period, footprint, n)
    phaseB0 = pow(max_period, bin_sum, n)
    phaseA1 = pow(phaseB0, footprint, n)
    phaseB1 = pow(phaseA0, bin_sum, n)
    phaseA2 = pow(max_value, footprint, n)
    phaseB2 = pow(max_value, bin_sum, n)
    phaseA3 = pow(phaseB2, footprint, n)
    phaseB3 = pow(phaseA2, bin_sum, n)
    if phaseA1 == phaseB1:
        secret_modulus = phaseA1
    public_modulus = n
    if phaseA3 == phaseB3:
        secret_key = phaseA3
    stamp = footprint * secret_key
    return public_modulus, secret_modulus, secret_key, stamp

def document_sign(secret_modulus, secret_key, document_footprint):
    return pow(document_footprint, secret_key, secret_modulus)

def document_verify(secret_modulus, secret_key, signature):
    v = pow(signature, secret_key, secret_modulus)
    print(v, signature)
    if v == signature:
        return True
    else:
        return False

def write_record(record, output_filename):
    f = open(output_filename, "w")
    avg_weight = fetu_avg_weight(record)
    min_value, max_value, total = fetu_min_max_value(record)
    periods, max_period, avg_period = fetu_residue_frequency(record)
    footprint = fetu_footprint(max_period, min_value, max_value, total, record)
    binary_footprint = fetu_binary_footprint(footprint, total, record)
    binary_mark = fetu_binary_mark(record)
    bin_msg, bin_msg_sum = fetu_binary_message(record)
    public_modulus, secret_modulus, secret_key, stamp = generate_fetu_keys(footprint, binary_footprint, binary_mark, bin_msg_sum, total, max_period, max_value)
    f.write("Fetu Document Report ---- \n")
    f.write("Fetu Document Footprint: "+str(footprint)+"\n")
    f.write("Fetu Document Binary Footprint: "+str(binary_footprint)+"\n")
    f.write("Fetu Document Binary Mark: "+str(binary_mark)+"\n")
    f.write("Fetu Document Binary Sum: "+str(bin_msg_sum)+"\n")
    f.write("Fetu Document Value Total: "+str(total)+"\n")
    f.write("Fetu Document Max Period: "+str(max_period)+"\n")
    f.write("Fetu Document Avg Period Length: "+str(avg_period)+"\n")
    f.write("Fetu Document Min Value: "+str(min_value)+"\n")
    f.write("Fetu Document Max Value: "+str(max_value)+"\n")
    f.write("Fetu Document Avg Weight: "+str(avg_weight)+"\n")
    f.write("Fetu Public Modulus: "+str(public_modulus)+"\n")
    f.write("Fetu Secret Modulus: "+str(secret_modulus)+"\n")
    f.write("Fetu Secret Key: "+str(secret_key)+"\n")
    f.write("Fetu Stamp: "+str(stamp)+"\n\n")
    #f.write(str(bin_msg)+"\n")
    for n, word in enumerate(record):
        f.write("Record number: "+str(n)+"\n")
        f.write("Latin word: "+str(word.name)+"\n")
        f.write("Fetu Word: "+str(word.wrd)+"\n")
        f.write("Fetu FTU: "+str(word.ftu)+"\n")
        f.write("Fetu Dbl: "+str(word.dbl)+"\n")
        f.write("Fetu Tri: "+str(word.tri)+"\n")
        f.write("Fetu Qua: "+str(word.qua)+"\n")
        f.write("Fetu FTU Val: "+str(word.ftu_val)+"\n")
        f.write("Fetu FTU Weight: "+str(word.ftu_weight)+"\n")
        f.write("Fetu FTU Residue: "+str(word.ftu_residue)+"\n")
        f.write("Fetu HWord Word: "+str(word.hword.wrd)+"\n")
        f.write("Fetu HWord Binary value: "+str(word.hword.wrd_val)+"\n")
        f.write("Fetu HWord FTU: "+str(word.hword.ftu)+"\n")
        f.write("Fetu HWord Val: "+str(word.hword.val)+"\n\n")
    f.close()

class FetuDocument:
    footprint = 0
    binary_footprint = 0
    binary_mark = 0
    binary_sum = 0
    value_total = 0
    max_period = 0
    avg_period_length = 0
    min_value = 0
    avg_weight = 0
    fetu_public_modulus = 0
    fetu_secret_modulus = 0
    fetu_secret_key = 0
    fetu_stamp = 0
    signatures = []

def read_fetu_document_report(input_filename):
    f = open(input_filename, "r")
    text = f.read()
    f.close()
    
    lines = text.split('\n')
    num_signatures = 0
    for x in range(10):
        if "Signing" in lines[x]:
            num_signatures += 1

    n = num_signatures

    document = FetuDocument()
    document.footprint = int(lines[n+1].split(':')[1].strip())
    document.binary_footprint = int(lines[n+2].split(':')[1].strip())
    document.binary_mark = int(lines[n+3].split(':')[1].strip())
    document.binary_sub = int(lines[n+4].split(':')[1].strip())
    document.value_total = int(lines[n+5].split(':')[1].strip())
    document.max_period = int(lines[n+6].split(':')[1].strip())
    document.avg_period_length = int(lines[n+7].split(':')[1].strip())
    document.min_value = int(lines[n+8].split(':')[1].strip())
    document.avg_weight = int(lines[n+9].split(':')[1].strip())
    document.fetu_public_modulus = int(lines[n+10].split(':')[1].strip())
    document.fetu_secret_modulus = int(lines[n+11].split(':')[1].strip())
    document.fetu_secret_key = int(lines[n+12].split(':')[1].strip())
    document.fetu_stamp = int(lines[n+13].split(':')[1].strip())

    for x in range(n):
        footprint = int(lines[x].split(":")[1].split()[0].strip())
        signature = int(lines[x].split(":")[2].split()[0].strip())
        document.signatures.append((footprint, signature))
    return document

def stamp_document(signing_document, destination_document, destination_filename, output_filename):
    signing_footprint = signing_document.footprint
    destination_footprint = destination_document.footprint
    
    secret_signing_modulus = signing_document.fetu_secret_modulus
    secret_signing_key = signing_document.fetu_secret_key

    signature = document_sign(destination_footprint, secret_signing_modulus, secret_signing_key)
    
    f = open(destination_filename, "r")
    document_tmp = f.read()
    f.close()
    stamped_document = "Signing Footprint: "+str(signing_footprint)+": Signature: "+str(signature)+"\n"+document_tmp

    f = open(output_filename, "w")
    f.write(stamped_document)
    f.close()
