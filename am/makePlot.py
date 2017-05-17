from subprocess import call
import matplotlib.pyplot as plt
import sys


pwd = "/home/gurbir/kek/water-vapour-cmb/am/"
def pwv2trop(pwv):
	return (float(pwv)-0.0029)/1.85

pwv = sys.argv[2]
filename = sys.argv[1]
trop_h20_scale = pwv2trop(pwv)
call("am " + pwd + filename + " 0 GHz 200 GHz 10 MHz 0 deg " +  str(trop_h20_scale) + " > out", shell=True)
f = open('out', 'r')
x = []
y = []
for line in f:
	words = line.split(' ')
	x.append(words[0])
	y.append(words[1])

plt.figure()
plt.plot(x, y)
# plt.xlim(15,30)
plt.show()