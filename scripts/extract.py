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
for fname in os.listdir("/Users/sazerac/Downloads/ade_400/ami_100"):
    if fname.endswith(".json"):

        fname = os.path.join("/Users/sazerac/Downloads/ade_400/ami_100", fname)
        f = open(fname)
        print(fname)

        errors = open('errors_log.txt', 'w')
        try:
            g = json.load(f)
            found = findall(g)
            write_intermediary(found,'../ami_100_txt/' + os.path.basename(fname[:-5] + '.txt'))
        except Exception as e:
            errors.write(fname + '\n')
            print(e)