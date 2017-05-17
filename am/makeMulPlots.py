from subprocess import call
import matplotlib.pyplot as plt
import sys


pwd = "/home/gurbir/kek/water-vapour-cmb/am/"
def pwv2trop(pwv):
	return (float(pwv)-0.0029)/1.8502

plt.figure()
filename = sys.argv[1]
for j in range(int(sys.argv[2])):
	pwv1 = sys.argv[3+j]
	pwv = 0
	if pwv1 != '0':
		pwv = pwv1
	else:
		pwv = 0.003
	trop_h20_scale = pwv2trop(pwv)
	call("am " + pwd + filename + " 0 GHz 200 GHz 10 MHz 0 deg " +  str(trop_h20_scale) + " > out"+str(j), shell=True)
	f = open('out'+str(j), 'r')
	x = []
	y = []
	for line in f:
		words = line.split(' ')
		x.append(words[0])
		y.append(words[1])

	plt.plot(x, y, label=pwv1 + " mm")
	# plt.xlim(15,30)
plt.legend(loc='upper right', bbox_to_anchor=(0.95,0.6))
plt.xlabel("Frequency (GHz)")
plt.ylabel("Tb (K)")
plt.title("Radiation temperature vs Frequency for different PWV")
plt.savefig('Tb_vs_freq_0_5_10_20_50.png')
plt.show()