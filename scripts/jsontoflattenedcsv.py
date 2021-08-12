import os
import csv
import json
import flatten_json
from tqdm.auto import tqdm

def directory_to_csv(inpath, outpath):
    errors = open('errors_log.txt', 'w+')

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for fname in tqdm(os.listdir(inpath)):
        inpath_ = os.path.join(inpath,fname)
        outpath_ = os.path.join(outpath, os.path.basename(fname[:-5] + '.csv'))

        try:
            json_to_csv(inpath_, outpath_)
        except Exception as e:
            errors.write(fname + '\n')
            print(inpath_)
            print(e)

    errors.close()

def json_to_csv(inpath, outpath):

    with open(inpath, encoding="utf-8") as json_file, open(outpath, 'w') as csv_file:
        try:
            pruned = json_file.read().replace("'", "")
            j = json.loads(pruned)
            j = flatten_json.flatten(j)

            c = csv.DictWriter(csv_file, fieldnames=j.keys(), delimiter="\t")
            c.writeheader()
            c.writerow(j)
        except Exception as e:
            with open('errors_log.txt', 'w+') as error_file:
                error_file.write(e)
                print("Error during loading {}".format(json_file))
                
directory_to_csv('../ADE/18k.wk', '../transfer/18k.tsv')
