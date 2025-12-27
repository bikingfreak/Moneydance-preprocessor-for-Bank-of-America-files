
from operator import itemgetter

mapping = {
    'has_header': True,
    'delimiter': ',',
    'bank': 'Bank of America',
    'account': 'Bank of America Credit Card',
    'date': itemgetter('Posted Date'),
    'amount': itemgetter('Amount'),
    'desc': itemgetter('Payee'),
}

