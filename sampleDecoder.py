#!/usr/bin/env python3

import sys
import argparse

# Setup the arguments
parser = argparse.ArgumentParser(description='Decode a string of complex samples.', add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('sampleFile', help='Binary file with the complex samples.')
parser.add_argument('samplesPerSymbol', help='Number of samples per symbol.')
parser.add_argument('--preamble','-p', default='AAAAAAAA', help='Preample in hex, default AAAAAAAA.')
parser.add_argument('--address','-a', default='8E89BED6', help='Access addres in hex, default 8E89BED6.')

# Parse the arguments
args = parser.parse_args()

print('sampleFile:      ', args.sampleFile)
print('samplePerSymbol: ', args.samplesPerSymbol)
print('preamble:        ', args.preamble)
print('address:         ', args.address)

sys.exit(0)
