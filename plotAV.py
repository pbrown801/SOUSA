# plotAV.py

import numpy as np
import matplotlib.pyplot as plt
import os.path
def plotData(avData):
	avData = np.asarray(avData)
	newAvData = np.zeros((5,len(avData)))
	# print(avData)
	fig = plt.figure()
	plt.subplot(2, 1, 1)
	col = ''


	labels = ['Center','North','East','South','West']
	for i in range(0,len(avData)):
		for j in range(0,5):
			newAvData[j][i] = avData[i][j]
	for i in range(1,5):
		if i == 1:
			col = 'g'
		elif i == 2:
			col = 'r'
		elif i == 3:
			col = 'k'
		elif i == 4:
			col = 'b'
		plt.scatter(newAvData[0,:],newAvData[i,:], color = col ,label = labels[i],s = 25)
	plt.legend(loc='best',prop = {'size':6})
	plt.title('Center Av vs 20 Arcminutes')
	plt.ylabel('Av at 20 Arcminutes')
	plt.tight_layout(pad = 2)
	plt.subplot(2, 1, 2)

	for i in range(1,5):
		if i == 1:
			col = 'g'
		elif i == 2:
			col = 'r'
		elif i == 3:
			col = 'k'
		elif i == 4:
			col = 'b'
		plt.scatter(newAvData[0,:], np.divide(newAvData[i,:],newAvData[0,:]), color =col,label = labels[i], s = 25)
	# plt.title('Center Av vs 20 Arcminutes/Center Av')
	plt.ylabel('Av at 20 Arcminutes/Center Av')
	plt.xlabel('Center Av')
	plt.legend(loc='best',prop = {'size':6})
	plt.show()
	fig.savefig(os.path.join('Pictures',"randomGal.png"))

import csv
currData = [None] * 5
avData=[]
with open('RandomAv.csv') as csvinp:
	reader = csv.reader(csvinp,delimiter = ',')
	count = 3
	count2 = 0
	count3 = 0
	for row in reader:
		count2 +=1
		if count != 0:
			count-=1
		elif count2%2 == 0:
			for j in range(0,5):
				currData[j] = row[j]
			currData = currData[:]
			avData.append(currData)
			count3+=1
plotData(avData)

