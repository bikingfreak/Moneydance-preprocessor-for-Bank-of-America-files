
### csvofx.py
# Script to convert BofA activity or statement generated in csv (BofA calls it 
# Excel) into an ofx file for import into Moneydance
## Converts csv file from BofA into ofx to import into Moneydance
## Note:
# -------------
# Assumes csv file exported from BofA is called stmt.csv
# Outputs file bofa.ofx ready for import into Moneydance
# Both files in the current directory
#----------------------------------
##########
import csv
import itertools as it
from meza.io import IterStringIO
from csv2ofx.ofx import OFX
from csv2ofx import utils
from mapping import mapping

import csv

def cleaned_dicts(path_in):
    with open(path_in, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        # 1) Drop first 6 lines (summary + blank)
        for _ in range(6):
            next(reader, None)

        # 2) Header row, drop "Running Bal." column (assumed 4th col)
        header = next(reader)              # e.g. ["Date","Description","Amount","Running Bal."]
        keep_idx = [0, 1, 2]               # keep Date, Description, Amount
        new_header = [header[i] for i in keep_idx]

        # 3) Data rows: drop 4th col, skip blanks and rows missing date/amount
        for row in reader:
            if not row or all(c.strip() == '' for c in row):
                continue
            row = [row[i] for i in keep_idx]
            rec = dict(zip(new_header, row))

            date   = (rec.get('Date')   or '').strip()
            amount = (rec.get('Amount') or '').strip()
            if not date or not amount:
                # skip summary/blank or malformed rows
                continue

            rec['Date'] = date
            rec['Amount'] = amount
            yield rec


# 1. Preprocess CSV here: sed-like cleaning, header renaming, etc.
# Assume the stmt.csv file is the raw csv file from BofA

csv_path = 'stmt.csv'
records = cleaned_dicts(csv_path)

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


