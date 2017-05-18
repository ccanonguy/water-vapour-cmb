import matplotlib.pyplot as plt
import csv
from pprint import pprint
import numpy as np
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
from subprocess import call


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

xvalueHist = xvalueHist[8:]
tskyHist[0] = tskyHist[0][8:]
tskyHist[1] = tskyHist[1][8:]
tskyHist[2] = tskyHist[2][8:]
sd[0] = sd[0][8:]
sd[1] = sd[1][8:]
sd[2] = sd[2][8:]

np.asarray(xvalueHist, dtype=np.float64)
np.asarray(tskyHist, dtype=np.float64)
np.asarray(sd)

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

pwd = "/home/gurbir/kek/water-vapour-cmb/am/"
def pwv2trop(pwv):
	return (float(pwv)-0.0029)/1.8502

def residual(p, x, data, sd):
	pwv = p['pwv']
	trop_h20_scale = pwv2trop(pwv)
	call("am " + pwd + "northern_midlatitude_MAM.amc 18198349174.587299 Hz" + 
		" 26602551275.637801 Hz 200100050.025 Hz 0 deg " +  str(trop_h20_scale) +
		" > amModel.out", shell=True)
	f = open('amModel.out', 'r')
	y = []
	for line in f:
		words = line.split(' ')
		y.append(words[1])
	y = np.asarray(y, dtype=np.float64)
	return np.divide(np.subtract(y, data), sd)

final = []
bestfit = []
for k in range(3):
	params = Parameters()
	params.add('pwv', value=2., min=0.1, max=10)

	minner = Minimizer(residual, params, fcn_args=(xvalueHist, tskyHist[k], sd[k]))
	result = minner.minimize(method='nelder')
	bestfit.append(result.params['pwv'].value)

	final.append(tskyHist[k] + np.multiply(result.residual, sd[k]))

	report_fit(result)

f = plt.figure()
plotNum = 1
for k in range(3):
	ax = f.add_subplot(2, 2, plotNum)
	plt.errorbar(xvalueHist, tskyHist[k], yerr=sd[k], fmt='o')
	plt.plot(xvalueHist, final[k])
	ax.text(0.4, 0.1, str(bestfit[k]) + ' mm PWV', transform=ax.transAxes)
	plt.title("Observation " + str(k+1))
	plt.xlabel("Frequency")
	plt.ylabel("Tsky")
	plotNum = plotNum + 1
plt.show()
