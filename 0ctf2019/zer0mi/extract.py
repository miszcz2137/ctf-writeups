#!/usr/bin/python2

from save_encrypt_15 import *
from sys import argv

GFToIntTable = {}
for i in range(1, 256):
	GFToIntTable['(' + repr(GF256(i)) + ')'] = i


if len(argv) > 1:
	print("input %s" % argv[1])
	lines = open(argv[1], 'r').readlines()

lines[0] = lines[0].split('[')[1].split(']')[0]

parts = lines[0].split(',')
parts = map(lambda x:x.strip(), parts)



N = int(argv[2])
assert(len(parts) == N)
assert(len(GFToIntTable.keys()) == 255)


def divide(p):
	tab = p.split('(')
	tab = filter(lambda x: x.strip() != '', tab)
	tab = map (lambda x:'(' + x, tab)
	return tab

parts = map(divide, parts)

def decode(term):
	gf = term.split(')')[0] + ')'
	assert(gf in GFToIntTable)
	co = GFToIntTable[gf]
	rest = term.split(')')[1].split('+')[0]
	rest = rest.strip()
	if rest == '':
		return (co, (N, N))
	rest = rest.strip('*')
	if rest.find('*') == -1:
		if rest.find('^') == -1:
			return (co, (int(rest.split('x')[1]), N))
		else:
			rest = rest.split('^')[0]
			return (co, (int(rest.split('x')[1]), int(rest.split('x')[1])))
	else:
		rest1, rest2 = rest.split('*')
		nr1 = int(rest1.split('x')[1])
		nr2 = int(rest2.split('x')[1])
		return (co, (min(nr1, nr2), max(nr1, nr2)))
	

for i in range(len(parts)):
	parts[i] = map(decode, parts[i])


macierz = []
for i in range(len(parts)):
	macierz.append([[0 for _ in range(N)] for _ in range(N)])
	for a in parts[i]:
		macierz[-1][a[1][0]][a[1][1]] ^= a[0]


fout = open("matrixes", 'w')

for mat in macierz:
	for row in mat:
		for a in row:
			fout.write('%d ' % a)
		fout.write('\n')
	fout.write('\n')

cipher = lines[1].strip().decode('hex')
for a in cipher:
	fout.write("%d " % ord(a))

