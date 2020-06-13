import numpy as py
import json
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def read():
	with open('../data/fireball_data.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

		cnt = 0
		sumv = 0
		values = py.array([])

		for row in spamreader:
			val = row[4]

			if len(values) == 24:
				break

			try:
				sumv += float(val)
				cnt += 1
				values = py.append(values, float(val))
			except:
				continue

			if (val.isdigit()) == True:
				sumv += float(val)
				cnt += 1

		avg = py.round(sumv/cnt, 3)
		return values

def pull(data):

	objs = py.array([])
	vels = py.array([])
	i = 0

	for objt in data:
		nova = data[objt]
		obj = int(nova["velocity"][0]["value"])
		vels = py.append(vels, obj)
		objs = py.append(objs, str(i))
		i += 1

	return (vels, objs)

def plot(vels, objs, values):
	plt.plot(objs, vels, 'r.', markersize=5)
	plt.plot(values, 'b.', markersize=5)

	ax = plt.gca()

	ax.set_title("Speed Comparison of Supernova to Fireball")
	ax.set_ylabel("Velocity (km/s)")
	ax.set_xlabel("Object")

	red_patch = mpatches.Patch(color='red', label="supernova")
	blue_patch = mpatches.Patch(color='blue', label="fireball")
	plt.legend(handles=[red_patch, blue_patch])

	plt.show() 