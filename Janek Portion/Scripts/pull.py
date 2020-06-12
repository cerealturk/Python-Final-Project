import requests
import json
import csv
from os import walk
from os import path
import numpy as np

def catObj(list_obj, word):
	list_total = ""

	for item in list_obj:
		if list_total == "":
			list_total = item[word]
		else:
			list_total += "|" + item[word] 

	return list_total

def objMeasure(response, word):
	obj = ""
	
	if "value" in response[word][0]:
		obj = response[word][0]["value"]
	
	return obj

def getRow(response):
	row = []
	name = response["name"][0]
	velocity = objMeasure(response, "velocity")
	bright = ""#"brightness"
	
	list_type = catObj(response["claimedtype"], "value")
	discovery = objMeasure(response, "discoverdate")
	lumdist = objMeasure(response, "lumdist")

	row.append(name)
	row.append(velocity)
	row.append(bright)
	row.append(list_type)
	row.append(discovery)
	row.append(lumdist)

	return row

def getTitle():
	row = []

	row.append("name")
	row.append("velocity (km/s)")
	row.append("brightness")
	row.append("type")
	row.append("discovery date")
	row.append("lumiance distance")
	row.append("energy (ergs/cm s^2)")

	return row

def readXrayData(file, name):
	fopen = open("./xray_data/" + file,)
	data = json.load(fopen)

	photo = data[name]["photometry"]

	val = 0
	for record in photo:
		val += float(record[1])

	if len(photo) > 1:
		val = val/len(photo)

#	val = np.round(val, 3)

	return val

def readData(name):
	row = []
	with open("./data/" + name + ".csv", newline='') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for data in datareader:
			row.append(data[0])
			row.append(data[1])
			row.append(data[2])
			row.append(data[3])
			row.append(data[4])
			row.append(data[5])
			break

	return row	

def pullAPI(file, name):
	url = "https://api.astrocats.space/catalog"
	schema = "httpts://github.com/astrocatalogs/schema/README.md"

	data = {
		name:{
			"schema": schema,
			"name": name
		}
	}

	data_json = json.dumps(data)
	print("Requesting data")
	response = requests.get(url, data=data_json)
	print("Parsing data pulled")
	response_json = response.json()	

	print("Parsing energy data")
	row = getRow(response_json[name])
	
	photo = readXrayData(file,name)
	row.append(str(photo))

	title = getTitle()
	with open('./data/'+ name + ".csv", "w", newline='') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow(title)
		writer.writerow(row)

	return row

def collectData(file):
	vals = file.split('.')
	name = vals[0]
	print(name)
	
	
	if path.exists('./data/' + name + ".csv"):
		row = readData(name)
	else:
		row = pullAPI(file, name)

	return row


def compileCSV(name, putTitle):
	print(response_json)
	title = getTitle()
	row = getRow(response)

	with open('data/'+ name, "w+") as file:
		writer = csv.writer(file)
		writer.writerows(title)
		writer.writerows(row)

def walkPath():
	folder = "./xray_data"
	files = []
	for (dirpath, dirnames, filenames) in walk(folder):
		files.extend(filenames)
		break

	rows = []	
	for name in files:
		row = collectData(name)
		rows.append(row)
		break

	title = getTitle()
	print(rows)
	with open('./combined.csv', "w", newline='') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow(title)
		writer.writerows(rows)

if __name__ == '__main__':
	#pullAPI("SN1987A")
	walkPath()