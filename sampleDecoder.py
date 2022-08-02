#!/usr/bin/env python3

import sys
import argparse
import csv
from math import pi, sqrt, exp
import re
import numpy

# Setup the arguments
parser = argparse.ArgumentParser(description='Decode a string of complex samples.', add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('sampleFile', help='Binary file with the complex samples.')
parser.add_argument('samplesPerSymbol', help='Number of samples per symbol.')
parser.add_argument('--preamble','-p', default='AAAAAAAA', help='Preample in hex, default AAAAAAAA.')
parser.add_argument('--minPower','-mp', default='0.9', help='Minimum bit power in float, default 0.9.')

# Parse the arguments
args = parser.parse_args()

print('# sampleFile:      ', args.sampleFile)
print('# samplePerSymbol: ', args.samplesPerSymbol)
print('# preamble:        ', args.preamble)
print('# min power:       ', args.minPower)

def gauss(n=8,sigma=1):
    x = range(-int(n/2),int(n/2))
    r = list()
    for i in x:
    	r.append(i+0.5)

    return [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]

def decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield raw

def addBytes(packet, data, samplesPerSymbol=8):
	
	# Add the data
	dataLen = 4*len(data)
	dataInt = int(data, 16)

	dataBin = ""
	for i in range(dataLen):
		if(dataInt & 1 << i):
			dataBin = "1" + dataBin
		else:
			dataBin = "0" + dataBin

	for bit in dataBin:
		for j in range(int(samplesPerSymbol)):
			packet = packet + bit

	return packet

# Import the samples
samples = ""
with open(args.sampleFile, 'r') as csvfile:

    reader = csv.reader(decomment(csvfile))

    # Iterate over each row in the csv using reader object
    for row in reader:
    	samples = (str(row[0]))


print('# samples:         ', samples)

# Convert samples to list of ints
samplesInt = list()
for digit in samples:
	if(digit == "1"):
		samplesInt.append(1)
	else:
		samplesInt.append(-1)

weightMask = gauss(int(args.samplesPerSymbol))

# Create the mask for the preamble
preambleMask = ""
preambleMask = addBytes(preambleMask, args.preamble, args.samplesPerSymbol)

# Convert to ints of -1 and 1
preambleMaskInt = list()
for digit in preambleMask:
	if(digit == "1"):
		preambleMaskInt.append(1)
	else:
		preambleMaskInt.append(-1)

# Apply the mask to the preamble
for i in range(0,int(args.samplesPerSymbol)*4*len(args.preamble),int(args.samplesPerSymbol)):
	preambleMaskInt[i:i+int(args.samplesPerSymbol)] = numpy.multiply(preambleMaskInt[i:i+int(args.samplesPerSymbol)], weightMask)

# Find the index with the max power
preambleMaxPower = -100
preambleMaxIndex = 0
for i in range(0,len(samplesInt)-len(preambleMaskInt)):
	power = numpy.dot(preambleMaskInt, samplesInt[i:i+len(preambleMaskInt)])

	if(power > preambleMaxPower):
		preambleMaxPower = power
		preambleMaxIndex = i

print("# max preamble power: ", preambleMaxPower)
print("# preamble index:     ", preambleMaxIndex)

minPreamblePower = float(args.minPower) * 4 * len(args.preamble)
print("# min preamble power: ",minPreamblePower)

if(preambleMaxPower < minPreamblePower):
	print("error: preamble not found")
	sys.exit(1)

data = 0
for i in range(preambleMaxIndex,len(samplesInt)-len(args.samplesPerSymbol)-7, int(args.samplesPerSymbol)):
	power = numpy.dot(weightMask, samplesInt[i:i+int(args.samplesPerSymbol)])
	# print(power)
	if(abs(power) < float(args.minPower)):
		break
	data = data << 1
	if(power > 0):
		data = data | 1

# Convert 
print("0x%X" % data)
sys.exit(0)
