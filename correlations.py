import os
import json

medis = {}
medis_counts = {}
error_counter = 0

for file in os.listdir("../18k"):
	if file.endswith(".json"):

		fname = os.path.join("../18k", file)
		f = open(fname)
		# print(fname)
		
		g = json.load(f)
		
		document_d_codes = []
		
		try:
			for d in g['Bericht']['Diagnose']['Diagnose']['DiagnList']:
				if not d['CodeList'] == '':
					for c in d['CodeList']:
						document_d_codes.append(c['Code'])
						
			
			for m in g['ZsfgKG']['MediEintritt']['Medis']['List']:
				if not m['ATC'] in medis.keys():
					medis[m['ATC']] = document_d_codes
				else:
					medis[m['ATC']].extend(document_d_codes)
		except:
			# print('Error in ', fname)
			error_counter += 1

print('Error filtes: ', error_count)		
del medis['']

for m , c in medis.items():
	counts = {}
	d_codes = set(c)
	
		
	for d in d_codes:
		
		count = c.count(d)
		
		if count > 100:
			counts[d] = c.count(d)
	
	if len(counts) > 0:
		counts_sorted = sorted(counts.items(), key=lambda kv: kv[1]).reverse()
		medis_counts[m] = counts_sorted
	

		
with open('out.txt','w') as g:
	g.write(json.dumps(medis_counts,sort_keys=True,indent=4))
				
	
		


