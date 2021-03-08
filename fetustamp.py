import sys
from ftucalc import *

''' KryptoMagick Fetu Document Stamp Standalone '''
''' Version 'AD'  '''

''' Usage: python3 fetustamp.py signing_document destination_document outpufile '''

input_filenameA = sys.argv[1]
input_filenameB = sys.argv[2]
output_filename = sys.argv[3]

documentA = read_fetu_document_report(input_filenameA)
documentB = read_fetu_document_report(input_filenameB)
stamp_document(documentA, documentB, input_filenameB, output_filename)
