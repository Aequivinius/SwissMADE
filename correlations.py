import os
import json

medis = {}
medis_names = {}
diag_names = {}
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
						
						if not c['Code'] in diag_names.keys():
							diag_names[c['Code']] = c['Name']
						
			
			for m in g['ZsfgKG']['MediEintritt']['Medis']['List']:
				if not m['ATC'] in medis.keys():
					medis[m['ATC']] = document_d_codes
				else:
					medis[m['ATC']].extend(document_d_codes)
					
				if not m['ATC'] in medis_names.keys():
					medis_names[m['ATC']] = m['oWirkstoff']
		except:
			# print('Error in ', fname)
			error_counter += 1

print('Error filtes: ', error_counter)

if '' in medis.keys():	
	del medis['']

print_dict = {}
for m , c in medis.items():
	counts = {}
	d_codes = set(c)
	
		
	for d in d_codes:
		
		count = c.count(d)
		
		if count > 100:
			counts[diag_names[d]] = c.count(d)
	
	if len(counts) > 0:
		counts_sorted = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
		
		print_dict[medis_names[m]] = counts_sorted
	

		
with open('out.txt','w') as g:
	g.write(json.dumps(print_dict,sort_keys=True,indent=4))
				
	
		


