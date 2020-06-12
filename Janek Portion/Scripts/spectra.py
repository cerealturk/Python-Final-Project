import json
import os
import matplotlib.pyplot as plt


def part(data):
	values = []

	i = 0
	for point in data:	
		readings = point[1]
		y = []
		x = []
		for value in readings:
			wave = float(value[0]) *1e10
			flux = float(value[1]) * 1e10 + 5*i
			x.append(wave)
			y.append(flux)

		i += 1
		z = {}
		z[0] = x
		z[1] = y
		values.append(z)

	return values

def plot(values):
	ax = plt.gca()
	ax.set_title("Spectra for SN1987A")
	ax.set_ylabel("Flux + offset")
	ax.set_xlabel("Wavelength (A)")

	p = 1
	color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

	l = len(values)

	for j in range(l-1, -1, -1):
		val = values[j]
		i = len(color) % p
		c = color[i]
		p += 1

		if p > len(color):
			p = 1

		plt.plot(val[0], val[1], c+'.', markersize=0.05) 

	plt.show()