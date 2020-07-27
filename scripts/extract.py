import json
import os

def findall_wrapper(g):
    found = {}
    findall(g,found)
    return found

def findall(g,found):

    if isinstance(g, str):
        return

    if isinstance(g, list):
        for h in g:
            findall(h,found)
        return

    if all(h in g.keys() for h in ['Titel', 'Text']):
        found[g['Titel']] = g['Text']
    if all(h in g.keys() for h in ['Titel', 'Inhalt']):
        if isinstance(g['Inhalt'], str):
            found[g['Titel']] = g['Inhalt']

    for key, item in g.items():
        findall(item,found)

def write_intermediary(intermediary,outfile):
    outstring = ''
    for key, item in intermediary.items():
            outstring += key + '\n'
            outstring += item + '\n\n'
    with open(outfile, 'w') as g:
        g.write(outstring.strip())

def json_to_txt(inpath, outpath):
    f = open(inpath)
    g = json.load(f)
    found = findall_wrapper(g)
    write_intermediary(found, outpath)

def json_to_txt_wrapper(inpath, outpath):
    errors = open('errors_log.txt', 'w')

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for fname in os.listdir(inpath):

        if os.path.isdir(os.path.join(inpath,fname)):
            new_inpath = os.path.join(inpath, fname)
            new_outpath = os.path.join(outpath, fname)
            json_to_txt_wrapper(new_inpath, new_outpath)

        if fname.endswith(".json"):
            new_inpath = os.path.join(inpath,fname)
            new_outpath = os.path.join(outpath, os.path.basename(fname[:-5] + '.txt'))

            try:
                json_to_txt(new_inpath, new_outpath)
            except Exception as e:
                errors.write(fname + '\n')
                print(new_inpath)
                print(e)