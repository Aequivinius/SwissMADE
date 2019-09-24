import json

def findall(g):
	found = {}
	findall_inside(g,found)
	return found

def findall_inside(g,found):

	if isinstance(g,str):
		return

	if isinstance(g,list):
		for h in g:
			findall_inside(h,found)
		return

	if all(h in g.keys() for h in ['Titel','Text']):
		found[g['Titel']] = g['Text']
	elif all(h in g.keys() for h in ['Titel','Inhalt']):
		print('Found',g)
		found[g['Titel']] = g['Inhalt']
	for key, item in g.items():
		findall_inside(item,found)

def write_intermediary(intermediary,outfile):
	outstring = ''
	for key, item in intermediary.items():
			outstring += key + '\n'
			outstring += item + '\n\n'
	with open(outfile, 'w') as g:
		g.write(outstring.strip())

import os
for file in os.listdir("../data_200"):
	if file.endswith(".json"):

		f = os.path.join("../data", file)
		f = open(f)
		g = json.load(f)
		found = findall(g)
		write_intermediary(found,'../data_extracted/' + file)