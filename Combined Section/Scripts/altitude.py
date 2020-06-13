# Isaac Burmingham

import numpy as np
import json
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from fireball import Fireball
import logging
import seaborn as sns


def pull_alt(data):

	objs = np.array([])
	alts = np.array([])
	i = 0

	for objt in data:
		nova = data[objt]
		obj = int(float(nova["comovingdist"][0]["value"]))
		alts = np.append(alts, obj)
		objs = np.append(objs, str(i))
		i += 1

	return (alts, objs)


def read_data():
    with open("fireball_data.csv",'r') as infile:
        logging.info("reading file...")
        reader = csv.reader(infile, delimiter=',', skipinitialspace=True)
        data = [data for data in reader]
    data_array = np.asarray(data)
    return data_array

def fb_alt():
    data_array = read_data()
    alt = data_array[1:,3]
    nan = np.array([''])
    alt = np.setdiff1d(alt,nan)
    alt = alt.astype(np.float)
    bins = np.arange(np.amin(alt)-0.5, np.amax(alt)+0.5)
    fb_alt = plt.hist(alt, bins=bins, alpha=0.5, label='Fireballs')
    return fb_alt
