import sys
from ftucalc import *

''' KryptoMagick Fetu Calculator Standalone '''
''' Version 'AC'  '''

''' Usage: python3 fetucalc.py inputfile outpufile '''

input_filename = sys.argv[1]
output_filename = sys.argv[2]

f = open(input_filename, "r")
lines = f.read()
f.close()

record = process_text(lines)
write_record(record, output_filename)
