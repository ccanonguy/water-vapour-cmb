import matplotlib.pyplot as plt
import csv
from pprint import pprint


power = []
xvalues = []
for k in range(9):
	filename = "trace_000" + str(k+1) + ".csv"
	bandwidth = 10000000000
	x = []
	y = []
	z = []
	i = 0
	with open(filename) as csvfile:						# open file as csvfile
		reader = csv.DictReader(csvfile, ['frequency', 'power'])		# read file as dict
		for row in reader:
			x.append(float(row['frequency']))								# append list of x
			y.append(float(row['power']))							# append list of y
			i = i +1

	for j in range(i):
		z.append(float(0.001*(10**(y[j]/10))))

	power.append(z)
	xvalues.append(x)
delf = float(bandwidth)/i;

tnoise = []
for k in range(3):
	dum = []
	for j in range(i):
		dum.append((300.0*power[2*k+1][j] - 77*power[2*k][j])/(power[2*k][j] - power[2*k+1][j]))
	tnoise.append(dum)

gain = []
for k in range(3):
	dum = []
	for j in range(i):
		dum.append(power[2*k][j]/(1.38*10**(-23)*delf*(300.0 + tnoise[k][j])))
	gain.append(dum)

tsky = []
for k in range(3):
	dum = []
	for j in range(i):
		dum.append(power[6+k][j]/(gain[k][j]*1.38*10**(-23)*delf) - tnoise[k][j])
	tsky.append(dum)

plt.figure()
plt.scatter(xvalues[0], tnoise[0])
plt.ylim(0, 5000)
plt.show()

f = plt.figure()
plotNum = 1
for k in range(3):
	ax = f.add_subplot(2, 2, plotNum)
	plt.plot(xvalues[0], tsky[k])
	plt.title("Observation " + str(k+1))
	plt.xlabel("Frequency")
	plt.ylabel("Tsky")
	plt.ylim((-100, 100))	
	plotNum = plotNum + 1
plt.show()