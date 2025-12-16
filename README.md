# Moneydance-preprocessor-for-Bank-of-America-files
This repository supports the processing and conversion of Bank of America checking account activity/statement files into an OFX file for clean import into Moneydance
The environment is Python. THe requirements are as follows:
1. Create a Python virtual environment: python3 -m venv venv
2. Activate the virtual environment: source venv/bin/activate
3. Install csvofx and meza in the environment: pip3 install csvofx meze
4. Create a mapping file with the following contents, which assumes the BofA file has the following columns (as per the heading line, line 7) Date, Amount, Description:
from operator import itemgetter

mapping = {
    'has_header': True,
    'delimiter': ',',
    'bank': 'Bank of America',
    'account': 'Bank of America Checking',
    'date': itemgetter('Date'),
    'amount': itemgetter('Amount'),
    'desc': itemgetter('Description'),
}
5. Run the script:
python3 csvofx.py
6. The output file is named bofa.ofx and is in the same directory. The input file is assumed to be named stmt.csv and is also in the same directory.
