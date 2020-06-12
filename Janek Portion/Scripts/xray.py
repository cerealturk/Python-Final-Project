import json
import os
import matplotlib.pyplot as plt
from math import log

def part(data):
	i = 0

	dt = []
	flux = []
	for point in data:	
		flux.append(log(float(point[1]), 10))
		dt.append(float(point[0]))

	return (dt, flux)

def plot(dt, flux):
	ax = plt.gca()
	ax.set_title("X-ray Observations for SN1987A")
	ax.set_ylabel("Log Flux (ergs s^-1 cm^-1)")
	ax.set_xlabel("Time (Gregorian)")

	p = 1

	plt.plot(dt, flux, 'b.', markersize=2) 
	plt.show()
