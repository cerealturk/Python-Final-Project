import json
import os
import numpy as py
import matplotlib.pyplot as plt
import math

def part(data):
	i = 0
	types = {}
	ptypes = []
	
	for point in data:
		ptype = point[4]

		instance = [point[0], point[1]]

		if not ptype in types:
			types[ptype] = {}
			types[ptype]["values"] = []
			types[ptype]["timestamp"] = []
			ptypes.append(ptype)
			i += 1

		types[ptype]["values"].append(float(point[1]))
		types[ptype]["timestamp"].append(float(point[0]))
	
	return (types, ptypes)

def plot(types, ptypes):
	timestamp_0 = types[ptypes[0]]["timestamp"]
	timestamp_1 = types[ptypes[1]]["timestamp"]
	timestamp_2 = types[ptypes[2]]["timestamp"]
	timestamp_3 = types[ptypes[3]]["timestamp"]
	timestamp_4 = types[ptypes[4]]["timestamp"]

	values_0 = types[ptypes[0]]["values"]
	values_1 = types[ptypes[1]]["values"]
	values_2 = types[ptypes[2]]["values"]
	values_3 = types[ptypes[3]]["values"]
	values_4 = types[ptypes[4]]["values"]

	xlower = min(timestamp_0)
	xupper = max(timestamp_0)
	ylower = min(values_0)
	yupper = max(values_0)

	plt.axis([xlower-100, xupper+100, yupper+1, ylower-1])

	ax = plt.gca()
	ax.set_title("Photometry for SN1987A")
	ax.set_ylabel("Apparent Magnitude")
	ax.set_xlabel("Time (Gregorian)")

	plt.plot(timestamp_0, values_0, 'r.', 
		timestamp_1, values_1, 'b.', 
		timestamp_2, values_2, 'g.', 
		timestamp_3, values_3, 'y.', 
		timestamp_4, values_4, 'm.', markersize=1)


	red_patch = mpatches.Patch(color='red', label='Visual')
	blue_patch = mpatches.Patch(color='blue', label='Gamma')
	green_patch = mpatches.Patch(color='green', label='UV')
	yellow_patch = mpatches.Patch(color='yellow', label='Infrared')
	mag_patch = mpatches.Patch(color='magenta', label='Radio')
	plt.legend(handles=[red_patch, blue_patch,green_patch,yellow_patch,mag_patch])
	plt.show()