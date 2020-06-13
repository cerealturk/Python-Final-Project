# Isaac & Janek Combined Work
# Janek did velocity & brightness
# Isaac did altitude distribution

import json
import os
import numpy as py
import matplotlib.pyplot as plt

import velocity
import brightness
import altitude

import argparse
import logging

class Data: 
	def __init__(self):
		logging.info("Data object created")
		self.name = "SN1987A"
		file = "../data/data.json"
		fopen = open(file,)
		self.body = json.load(fopen)
		fopen.close()

		file = "../data/master.json"
		fopen = open(file,)
		self.master = json.load(fopen)
		fopen.close()

	def velocity(self):
		logging.info("Creating plot velocity data")		
		data, bodies = velocity.pull(self.master)
		values = velocity.read()
		velocity.plot(data, bodies, values)

	def brightness(self):
		logging.info("Creating plot for brightness data")
		data = self.body[self.name]["photometry"]
		types, ptypes = brightness.part(data)
		brightness.plot(types, ptypes)
		
	def altitude(self):
		logging.info("Creating plot for distance data")
		data, bodies = altitude.pull_alt(self.master)
		bins = py.arange(py.amin(data)-0.5, py.amax(data)+0.5)
		fb = altitude.fb_alt()
		plt.hist(data, alpha=0.5,label='Supernovae')
		plt.title("Altitude Distribution of Fireball and Supernovae")
		plt.xlabel("Altitude")
		plt.ylabel("Count")
		plt.legend(loc='upper right')
		plt.show()

class Processor:
	def __init__(self, data):
		logging.info("Processor object created")
		self.data = data

	def printVelocity(self):
		self.data.velocity()

	def printBrightness(self):
		self.data.brightness()
		
	def printAltitude(self):
		self.data.altitude()


def arg_parser():
	logging.info("Building argument parser")
	parser = argparse.ArgumentParser(description="Plot data on supernova")
	parser.add_argument('-v', '-velocity', dest='vel', action='store_true', default=False, help="plot velocity scatter plot")
	parser.add_argument('-b', '-brightness', dest='bright', action='store_true', default=False, help="plot brightness comparison plot")
	parser.add_argument('-a', '-altitude', dest='alt',action='store_true',default=False,help="plot altitude distribution of fireballs and Supernovae")

	logging.info("Parsing arguments")
	args = parser.parse_args()
	return args

def load_logging():
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	fh = logging.FileHandler("log.log", 'w')
	fh.setLevel(logging.DEBUG)
	logger.addHandler(fh)

	sh = logging.StreamHandler()
	sh.setLevel(logging.INFO)
	logger.addHandler(sh)

def main():
	load_logging()
	args = arg_parser()

	data = Data()
	process = Processor(data)

	logging.info("Reading selection...")

	if args.vel:
		logging.info("initiating Velocity plot...")
		process.printVelocity()

	if args.bright:
		logging.info("initiating Brightness plot...")
		process.printBrightness()
		
	if args.alt:
		logging.info("initiating Altitude plot.. ")
		process.printAltitude()


if __name__ == '__main__':
	main()
