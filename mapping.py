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

