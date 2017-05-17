import matplotlib.pyplot as plt


f = open('example2.5.0-200.out', 'r')
x = []
y = []
for line in f:
	words = line.split(' ')
	x.append(words[0])
	y.append(words[2])

plt.figure()
plt.plot(x, y)
plt.show()