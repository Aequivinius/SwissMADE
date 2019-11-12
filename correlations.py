import os
import json

medis = {}
medis_counts = {}

for file in os.listdir("../data_200"):
	if file.endswith(".json"):

		fname = os.path.join("../data_200", file)
		f = open(fname)
		print(fname)
		
		g = json.load(f)
		
		document_d_codes = []
		
		for d in g['Bericht']['Diagnose']['Diagnose']['DiagnList']:
			if not d['CodeList'] == '':
				for c in d['CodeList']:
					document_d_codes.append(c['Code'])
					
		
		for m in g['ZsfgKG']['MediEintritt']['Medis']['List']:
			if not m['ATC'] in medis.keys():
				medis[m['ATC']] = document_d_codes
			else:
				medis[m['ATC']].extend(document_d_codes)

for m , c in medis.items():
	counts = {}
	d_codes = set(c)
	
		
	for d in d_codes:
		
		counts[d] = c.count(d)
	
	medis_counts[m] = counts
		
with open('out.txt','w') as g:
	g.write(json.dumps(medis_counts,sort_keys=True,indent=4))
				
	
		


