import unittest
import os
from main import Data
import photometry
import spectra
import xray

class TestSum(unittest.TestCase):

	def test_photo_size(self):
		data = Data()
		dataset = data.body["SN1987A"]["photometry"]
		types, _ = photometry.part(dataset)
		length = len(types)
		self.assertEqual(length, 5)

	def test_spect_size(self):
		data = Data()
		dataset = data.body["SN1987A"]["spectra"]
		values = spectra.part(dataset)
		length = len(values)
		self.assertEqual(length, 36)

	def test_xray_size(self):
		data = Data()
		dataset = data.body["SN1987A"]["xray"]
		dt, _ = xray.part(dataset)
		length = len(dt)
		self.assertEqual(length, 105)

	def test_xray_size(self):
		data = Data()
		dataset = data.body["SN1987A"]["xray"]
		_, flux = xray.part(dataset)
		length = len(flux)
		self.assertEqual(length, 105)

if __name__ == '__main__':
    unittest.main()