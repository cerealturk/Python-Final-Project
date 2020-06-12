import json
import os
import numpy as py
import matplotlib.pyplot as plt
import spectra
import photometry
import xray
import velocity
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
		data, bodies = velocity.pull(self.master)
		values = velocity.read()
		#data = py.append(data, avg)
		#bodies = py.append(bodies, "Fireball")
		velocity.plot(data, bodies, values)

	def spectra(self):
		logging.info("Creating plot for spectral data")
		data = self.body[self.name]["spectra"]
		values = spectra.part(data)
		spectra.plot(values)

	def photometry(self):
		logging.info("Creating plot for photometry data")
		data = self.body[self.name]["photometry"]
		types, ptypes = photometry.part(data)
		photometry.plot(types, ptypes)

	def xray(self):
		logging.info("Creating plot for xray data")
		data = self.body[self.name]["xray"]
		dt, flux = xray.part(data)
		xray.plot(dt, flux)

	def venus(self):
		logging.info("Creating plot for photometry data")
		data = self.body[self.name]["photometry"]
		types, ptypes = photometry.partAbsolute(data)
		photometry.venus(types, ptypes)

class Processor:
	def __init__(self, data):
		logging.info("Processor object created")
		self.data = data

	def printSpectra(self):
		self.data.spectra()

	def printPhotometry(self):
		self.data.photometry()

	def printXray(self):
		self.data.xray()

	def printVelocity(self):
		self.data.velocity()

	def plotVenus(self):
		self.data.venus()


def arg_parser():
	logging.info("Building argument parser")
	parser = argparse.ArgumentParser(description="Plot data on supernova")
	parser.add_argument('-p', '-photometry', dest='photo', action='store_true', default=False, help="plot photometry data")
	parser.add_argument('-s', '-spectra', dest='spec', action='store_true', default=False, help="plot spectral data")
	parser.add_argument('-x', '-xray', dest='ray', action='store_true', default=False, help="plot xray data")
	parser.add_argument('-v', '-velocity', dest='vel', action='store_true', default=False, help="plot velocity scatter plot")
	parser.add_argument('-b', '-brightness', dest='bright', action='store_true', default=False, help="plot velocity scatter plot")

	logging.info("Parsing arguments")
	args = parser.parse_args()
	return args

def load_logging():
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	fh = logging.FileHandler("autompg2.log", 'w')
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

	if args.spec:
		logging.info("initiating Spectral plot...")
		process.printSpectra()

	if args.photo:
		logging.info("initiating Photometry plot...")
		process.printPhotometry()

	if args.ray:
		logging.info("initiating X-Ray plot...")
		process.printXray()

	if args.vel:
		logging.info("initiating X-Ray plot...")
		process.printVelocity()

	if args.bright:
		logging.info("initiating X-Ray plot...")
		process.plotVenus()


if __name__ == '__main__':
	main()