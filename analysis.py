import matplotlib.pyplot as plt
import csv
from pprint import pprint
import numpy as np


power = []
xvalues = []
for k in range(15):
	filename = "Trace_000" + str(k) + ".csv"
	bandwidth = 10000000000
	x = []
	y = []
	z = []
	i = 0
	with open(filename) as csvfile:						# open file as csvfile
		reader = csv.DictReader(csvfile, ['frequency', 'power'])		# read file as dict
		for row in reader:
			i = i +1
			if i<46:
				continue
			x.append(float(row['frequency']))								# append list of x
			y.append(float(row['power']))							# append list of y
	i = i - 45
	for j in range(i):
		z.append(float(0.001*(10**(y[j]/10))))

	power.append(z)
	xvalues.append(x)
delf = float(bandwidth)/i;

tnoise = []
for k in range(6):
	dum = []
	for j in range(i):
		dum.append((300.0*power[2*k+1][j] - 77*power[2*k][j])/(power[2*k][j] - power[2*k+1][j]))
	tnoise.append(dum)

tnoiseAvg = []
for j in range(i):
	tnoiseAvg.append((tnoise[0][j] + tnoise[1][j] + tnoise[2][j] + tnoise[3][j] + tnoise[4][j] + tnoise[5][j])/6)


gain = []
for k in range(6):
	dum = []
	for j in range(i):
		dum.append(power[2*k][j]/(1.38*10**(-23)*delf*(300.0 + tnoise[k][j])))
	gain.append(dum)

gainAvg = []
for j in range(i):
	gainAvg.append((gain[0][j] + gain[1][j] + gain[2][j] + gain[3][j] + gain[4][j] + gain[5][j])/6)

tsky = []
for k in range(3):
	dum = []
	for j in range(i):
		dum.append(power[12+k][j]/(gainAvg[j]*1.38*10**(-23)*delf) - tnoiseAvg[j])
	tsky.append(dum)

f = plt.figure()
plotNum = 1
for k in range(3):
	ax = f.add_subplot(2, 2, plotNum)
	plt.plot(xvalues[0], tsky[k])
	plt.title("Observation " + str(k+1))
	plt.xlabel("Frequency")
	plt.ylabel("Tsky")
	plt.ylim((-100, 150))	
	plotNum = plotNum + 1
plt.show()

tskyHist = []
for k in range(3):
	dum = [np.mean(tsky[k][j:j+40]) for j in range(0, i, 40)]
	tskyHist.append(dum)

xvalueHist = [np.mean(xvalues[0][j:j+40]) for j in range(0, i, 40)]

sd = []
for k in range(3):
	dum = [np.std(tsky[k][j:j+40]) for j in range(0, i, 40)]
	sd.append(dum)

f = plt.figure()
plotNum = 1
for k in range(3):
	ax = f.add_subplot(2, 2, plotNum)
	plt.errorbar(xvalueHist, tskyHist[k], yerr=sd[k], fmt='o')
	plt.title("Observation " + str(k+1))
	plt.xlabel("Frequency")
	plt.ylabel("Tsky")
	plt.ylim((-100, 150))	
	plotNum = plotNum + 1
plt.show()