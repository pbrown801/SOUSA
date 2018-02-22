# csvToAscii.py
import os.path
import sys
import itertools
import csv

with open('RandomAv.txt','w') as output:
	with open('RandomAv1.csv') as csvinp:
		reader = csv.reader(csvinp,delimiter = ',')
		for row in reader:
			for col in row:
				output.write(str(col) + ' ')
			output.write('\n')
