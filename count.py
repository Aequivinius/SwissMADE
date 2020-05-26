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


def construct_subset(counts='count.csv', size=300):

    diagnoses = codes_to_documents()

    counts = pandas.read_csv('output.csv', index_col=0, squeeze=True).to_dict()
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
    all_codes = excel_to_codes()
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

    return diagnoses


if __name__ == '__main__':
    codes_to_documents(sys.argv[1])
