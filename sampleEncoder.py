#!/usr/bin/env python3

import sys
import argparse
import random

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

# Setup the arguments
parser = argparse.ArgumentParser(description='Encode a string of complex samples. Payload of random bytes with random string pre and post packet', 
	add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('sampleFile', help='Binary file with the complex samples.')
parser.add_argument('samplesPerSymbol', help='Number of samples per symbol.')
parser.add_argument('--preamble','-p', default='AAAAAAAA', help='Preample in hex, default AAAAAAAA.')
parser.add_argument('--address','-a', default='8E89BED6', help='Access addres in hex, default 8E89BED6.')
parser.add_argument('--len','-l', default='32', help='Lenght of packet in decimal, default 32.')

# Parse the arguments
args = parser.parse_args()

print('# sampleFile:       ', args.sampleFile)
print('# samplesPerSymbol: ', args.samplesPerSymbol)
print('# preamble:         ', args.preamble)
print('# address:          ', args.address)
print('# length:           ', args.len)

samples = ""

# Add some random samples at the start
for i in range(random.randrange(512, 1024)):
	samples = samples + str(random.randrange(0,2))

# Add the preamble
samples = addBytes(samples, args.preamble, int(args.samplesPerSymbol))

# Add the access address
samples = addBytes(samples, args.address, int(args.samplesPerSymbol))

# Add the payload
payload = ""
for i in range(int(args.len)*2):
	payload = payload + "%0.1X" % random.randrange(0,16)

print("# payload:          ",payload)
samples = addBytes(samples, payload, int(args.samplesPerSymbol))

# Add some random samples at the end
for i in range(random.randrange(512, 1024)):
	samples = samples + str(random.randrange(0,2))

print(samples)

sys.exit(0)
