### csvofx_cc.py
# Script to convert BofA activity or statement generated in csv (BofA calls it 
# Excel) into an ofx file for import into Moneydance
## Converts credit card csv file from BofA into ofx to import into Moneydance
## Note:
# -------------
# Assumes csv file exported from BofA is called stmt.csv
# Outputs file bofa.ofx ready for import into Moneydance
# Both files in the current directory
# The mapping file, mapping_cc.py, differs from the checking mapping file
#----------------------------------
##########
import csv
import itertools as it
from meza.io import IterStringIO
from csv2ofx.ofx import OFX
from csv2ofx import utils
from mapping_cc import mapping

import csv

import csv

def cleaned_card_dicts(path_in):
    with open(path_in, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            date   = (row.get('Posted Date') or '').strip()
            amount = (row.get('Amount') or '').strip()
            payee  = (row.get('Payee') or '').strip()

            if not date or not amount:
                # skip any summary/blank rows
                continue

            yield {
                'Posted Date': date,
                'Amount': amount,
                'Payee': payee,
            }


# 1. Preprocess CSV here: sed-like cleaning, header renaming, etc.
# Assume the stmt.csv file is the raw csv file from BofA

csv_path = 'stmt_cc.csv'
records = cleaned_card_dicts(csv_path)

ofx = OFX(mapping)
groups = ofx.gen_groups(records)
trxns = ofx.gen_trxns(groups)
cleaned_trxns = ofx.clean_trxns(trxns)
data = utils.gen_data(cleaned_trxns)

content = it.chain(
    [ofx.header()],
    ofx.gen_body(data),
    [ofx.footer()],
)

with open('bofa.ofx', 'w', encoding='utf-8') as f:
    for line in IterStringIO(content):
        # line is bytes, decode to str
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        f.write(line)


