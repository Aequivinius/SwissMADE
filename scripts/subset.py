import csv
import os
import json
from jsonpath_ng.ext import parse
import pandas
import random
import sys

ICD10_CODE = parse('$..CodeList[?(@.Kat=="ICD10")].Code')


def file_to_code(json_file):
    with open(json_file) as jf:
        data = json.load(jf)
        return [match.value for match in ICD10_CODE.find(data)]


def excel_to_codes(excel_file='codes/Code_Lists_ETEV_Hemo_ETEA_20200228.xlsx'):
    icd10codes = []
    icd10_2_codes = []
    sheets = pandas.read_excel(excel_file, sheet_name=None)

    for name, sheet in sheets.items():
        try:
            icd10codes.extend(sheet['ICD10GM_code'].tolist())
            icd10_2_codes.extend(sheet['ICD10GM2_code2'].tolist())
        except KeyError:
            print('No codes in', name)

    pandas.DataFrame(icd10codes).to_csv('codes/icd10_codes.tsv',
                                        index=False)
    pandas.DataFrame(icd10_2_codes).to_csv('codes/icd10_2_codes.tsv',
                                           index=False)
    return set(icd10codes) | set(icd10_2_codes)


def count(json_directory='data_json'):
    total_diagnoses_counter = 0
    matching_diagnoses_counter = 0
    diagnoses_counter = {}
    all_codes = excel_to_codes()

    for report in os.listdir(json_directory):
        if not report.endswith(".json"):
            continue

        print('processing report ', report)

        codes = file_to_code(os.path.join(json_directory, report))

        total_diagnoses_counter += len(codes)
        matching_diagnoses = set(codes) & all_codes
        matching_diagnoses_counter += len(matching_diagnoses)
        for match in matching_diagnoses:
            if match in diagnoses_counter:
                diagnoses_counter[match] += 1
            else:
                diagnoses_counter[match] = 1

    w = csv.writer(open("count.csv", "w"))
    w.writerow(['total diagnoses', total_diagnoses_counter])
    w.writerow(['matching diagnoses', matching_diagnoses_counter])
    for key, val in diagnoses_counter.items():
        w.writerow([key, val])


def construct_subset(data='test_data', counts='count.csv', size=300):

    diagnoses = codes_to_documents(data)

    counts = pandas.read_csv(counts, index_col=0, squeeze=True).to_dict()
    counts.pop('total diagnoses')
    total = counts.pop('matching diagnoses')
    factor = size/int(total)

    subset = []

    for diagnosis, count in counts.items():
        number = int(count * factor) + 1

        if number > len(diagnoses[diagnosis]):
            number = len(diagnoses[diagnosis])

        subset.extend(random.sample(diagnoses[diagnosis], number))

    subset = set(subset)
    with open('subset.txt', 'w') as outfile:
        outfile.write("\n".join(subset))
    print(subset)


def codes_to_documents(inpath='test_data'):
    with open('codes/allcodes.tsv') as f:
        all_codes = set(f.read().splitlines())
    diagnoses = {}

    for report in os.listdir(inpath):
        if not report.endswith(".json"):
            continue
        print('processing report ', report)

        codes = file_to_code(os.path.join(inpath, report))

        matching_diagnoses = set(codes) & all_codes
        for match in matching_diagnoses:
            if match in diagnoses:
                diagnoses[match].append(report)
            else:
                diagnoses[match] = [report]

    print(diagnoses)
    return diagnoses


def predict_ade(codes, haystack):
    classification = []

    vte = any(code in haystack['vte_codes'] for code in codes)
    vte = vte or any(
        code.startswith(tuple(haystack['vte_codes_expand'])) for code in codes)

    if vte:

        pe = any(code in haystack['pe_codes'] for code in codes)
        pe = pe or any(
            code.startswith(
                 tuple(haystack['pe_codes_expand'])) for code in codes)
        if pe:
            classification.append('pe')

        stroke = any(code in haystack['stroke_codes'] for code in codes)
        stroke = stroke or any(
            code.startswith(
                 tuple(haystack['stroke_codes_expand'])) for code in codes)
        if stroke:
            classification.append('stroke')

        ami = any(code in haystack['ami_codes'] for code in codes)
        ami = ami or any(
            code.startswith(
                 tuple(haystack['ami_codes_expand'])) for code in codes)
        if ami:
            classification.append('ami')

    ade_hemo = any(code in haystack['ade_hemo_codes'] for code in codes)
    # not necessary, there are not _ in the ade_hemo codes

    if ade_hemo:

        sev_hemo = any(code in haystack['sev_hemo_codes'] for code in codes)
        sev_hemo = sev_hemo or any(
            code.startswith(
                 tuple(haystack['sev_hemo_codes_expand'])) for code in codes)
        if sev_hemo:
            classification.append('sev_hemo')

    if len(classification) < 1:
        classification = []

    return classification

    # if doesn't yield enough, try adding Hemo & ( transfu | death )


def get_codes(infile):
    codes = open(infile).read().splitlines()
    codes = [code.split('!')[0] for code in codes]
    codes_expand = [code.split('_')[0] for code in codes if '_' in code]
    codes = [code for code in codes if '_' not in code]

    return codes, codes_expand


def file_to_codes(json_file):
    with open(json_file) as jf:
        data = json.load(jf)
        return [match.value for match in ICD10_CODE.find(data)]


def predict_directory(inpath='subset_300/*.json'):

    haystack = {'pe_codes': [], 'pe_codes_expand': [],
                'vte_codes': [], 'vte_codes_expand': [],
                'stroke_codes': [], 'stroke_codes_expand': [],
                'ami_codes': [], 'ami_codes_expand': [],
                'ade_hemo_codes': [], 'ade_hemo_codes_expand': [],
                'sev_hemo_codes': [], 'sev_hemo_codes_expand': []}

    haystack['pe_codes'], \
        haystack['pe_codes_expand'] = get_codes('codes/PE.txt')
    haystack['vte_codes'], \
        haystack['vte_codes_expand'] = get_codes('codes/ADE_VTE.txt')
    haystack['stroke_codes'], \
        haystack['stroke_codes_expand'] = get_codes('codes/Stroke.txt')
    haystack['ami_codes'], \
        haystack['ami_codes_expand'] = get_codes('codes/AMI.txt')
    haystack['ade_hemo_codes'], \
        haystack['ade_hemo_codes_expand'] = get_codes('codes/ADE_Hemo.txt')
    haystack['sev_hemo_codes'], \
        haystack['sev_hemo_codes_expand'] = get_codes('codes/Sev_Hemo.txt')

    classified = {'stroke': [],
                  'sev_hemo': [],
                  'ami': [],
                  'pe': []}

    import glob
    import os.path

    for report in glob.glob(inpath):
        codes = file_to_codes(report)

        classifications = predict_ade(codes, haystack)
        if classifications != []:

            for classification in classifications:
                classified[classification].append(os.path.split(report)[1])

    for ade, documents in classified.items():
        with open(ade + '.txt', 'w') as f:
            f.write("\n".join(documents))
            f.write("\n")

if __name__ == '__main__':
    predict_directory(sys.argv[1])
