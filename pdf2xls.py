from pypdf import PdfReader
from glob import glob
from pandas import DataFrame as dt
import re
import os


def evaluate(data: list):
    result = []
    for line in data:
        en1 = bool(re.search('Bases', line))
        en2 = bool(re.search('Lista', line))
        en3 = bool(re.search('Peso', line))
        en4 = bool(re.search('Total', line))
        en5 = bool(re.search('Descripci', line))
        di2 = bool(re.search(r'^[\d]{2}\s+', line))
        di3 = bool(re.search(r'^[\d]{3}\s+', line))
        di4 = bool(re.search(r'^[\d]{4}\s+', line))
        di6 = bool(re.search(r'^[\d]{6}\s+\d', line))
        if any([en1, en2, en3, en4, en5, di2, di3, di4]):
            pass
        elif di6:
            result.append(' '.join(line.split()).rstrip().replace('. ', '.'))
        else:
            result[-1] += ' ' + \
                ' '.join(line.split()).rstrip().replace('. ', '.')
    return result


def organize(lines: list):
    dbase = [['COD', 'MO', 'EQ', 'PT', 'MAT', 'SMAT', 'TOT', 'UM', 'DESC']]
    pattern = re.compile(r'^[A-Z]')
    for line in lines:
        spl = line.split(' ')
        for ind, word in enumerate(spl):
            if pattern.match(word):
                if ind == 8:
                    op = spl[7]
                else:
                    op = f'{spl[7]} {spl[8]}'
                dbase.append([spl[0], c(spl[1]), c(spl[2]), c(spl[3]), c(
                    spl[4]), c(spl[5]), c(spl[6]), op, ' '.join(spl[ind:])])
                break
    return dbase


def organize2(lines: list):
    dbase = [['COD', 'MO', 'EQ', 'PT', 'MAT', 'SMAT', 'TOT', 'UM', 'DESC']]
    pattern = re.compile(r'^[A-Z]')
    for line in lines:
        spl = line.split(' ')
        for ind, word in enumerate(spl):
            if pattern.match(word):
                desc = ' '.join(spl[ind:])
                dbase.append([spl[0], c(spl[1]), c(spl[2]), c(
                    spl[3]), c(spl[4]), c(spl[5]), c(spl[6]), '', desc])
                break
    return dbase


def c(num):
    return num.replace(',', '')



with open('unidades.txt') as f:
    unidades=f.readline()
    print(unidades)

lines = []
pdfs = glob('*.pdf')

for num, file in enumerate(pdfs):
    reader = PdfReader(file)
    for page in reader.pages:
        clean_txt = re.sub(r'^\s+', '', page.extract_text(),
                           flags=re.MULTILINE)
        result = evaluate(clean_txt.split('\n'))
        lines += result
        # print(f'file: {file} ({num+1}/{len(pdfs)}) \n')


# with open('eval.txt','w') as f:
#     f.write('\n'.join(lines))

separated = organize2(lines)

dt(separated).to_excel(f'{pdfs[0][:-4]}-{pdfs[-1][:-4]}.xlsx')
