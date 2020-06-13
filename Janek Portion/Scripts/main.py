import json
import os
import numpy as py
import matplotlib.pyplot as plt

import spectra
import photometry
import xray

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


def arg_parser():
	logging.info("Building argument parser")
	parser = argparse.ArgumentParser(description="Plot data on supernova")
	parser.add_argument('-p', '-photometry', dest='photo', action='store_true', default=False, help="plot photometry data")
	parser.add_argument('-s', '-spectra', dest='spec', action='store_true', default=False, help="plot spectral data")
	parser.add_argument('-x', '-xray', dest='ray', action='store_true', default=False, help="plot xray data")
	
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

	if args.spec:
		logging.info("initiating Spectral plot...")
		process.printSpectra()

	if args.photo:
		logging.info("initiating Photometry plot...")
		process.printPhotometry()

	if args.ray:
		logging.info("initiating X-Ray plot...")
		process.printXray()


if __name__ == '__main__':
	main()