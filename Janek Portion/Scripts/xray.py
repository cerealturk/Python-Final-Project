import json
import numpy as py
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from math import log

def part(data):
	i = 0

	types = {}
	ptypes = []

	for point in data:		
		ptype = str(point[4])

		if not ptype in types:
			types[ptype] = {}
			types[ptype]["values"] = []
			types[ptype]["timestamp"] = []
			ptypes.append(ptype)
			i += 1

		types[ptype]["values"].append(log(float(point[1]), 10))
		types[ptype]["timestamp"].append(float(point[0]))

	return (types, ptypes)

def plot(types, ptypes):
	timestamp_0 = types[ptypes[0]]["timestamp"]
	timestamp_1 = types[ptypes[1]]["timestamp"]
	timestamp_2 = types[ptypes[2]]["timestamp"]

	values_0 = types[ptypes[0]]["values"]
	values_1 = types[ptypes[1]]["values"]
	values_2 = types[ptypes[2]]["values"]

	xlower = min(timestamp_0)
	xupper = max(timestamp_0)
	ylower = min(values_0)
	yupper = max(values_0)

	ax = plt.gca()
	ax.set_title("X-ray Observations for SN1987A")
	ax.set_ylabel("Log Flux (ergs s^-1 cm^-1)")
	ax.set_xlabel("Time (Gregorian)")

	plt.plot(timestamp_0, values_0, 'r.', 
		timestamp_1, values_1, 'b.', 
		timestamp_2, values_2, 'g.', markersize=1)

	red_patch = mpatches.Patch(color='red', label=ptypes[0] + " eV")
	blue_patch = mpatches.Patch(color='blue', label=ptypes[1] + " eV")
	green_patch = mpatches.Patch(color='green', label=ptypes[2] + " eV")
	plt.legend(handles=[red_patch, blue_patch,green_patch])
	plt.show()