from subprocess import call
import matplotlib.pyplot as plt
import sys


pwd = "/home/gurbir/kek/water-vapour-cmb/am/"
def pwv2trop(pwv):
	return (float(pwv)-0.0029)/1.8502

pwv1 = sys.argv[2]
pwv = 0
if pwv1 != '0':
	pwv = pwv1
else:
	pwv = 0.003
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
plt.xlabel("Frequency (GHz)")
plt.ylabel("Tb (K)")
plt.title("Radiation temperature vs Frequency for " + pwv1 + " mm PWV")
plt.savefig('Tb_vs_freq_' + pwv1 + '.png')
# plt.xlim(15,30)
plt.show()