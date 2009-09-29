import datetime
import urlfetch
from mint.tags import Tag, TagSet
from mint.utils import parse_date

MAPPING = {
    'Description' : 'description',
    'Original Description' : 'original_description',
    'Amount' : 'amount',
    'Transaction Type' : 'transaction_type',
    'Category' : 'category',
    'Account Name' : 'account_name',
    'Notes' : 'notes',
}

JSON_KEYS = ['amount', 'id', 'note', 'merchant', 'omerchant', 'categoryId', 'category', 'fi', 'account']

class Transaction(object):
    @staticmethod
    def from_json(data, mint, year=None):
        d = {'mint' : mint}
        d['date'] = parse_date(data['date'], year or datetime.datetime.now().year)
        d['tags'] = TagSet.from_json(data['labels'], value_key='name', mint=mint)
        for key in JSON_KEYS:
            d[key] = data[key]
        return Transaction(**d)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Transaction: %s>' % unicode(self)

    def __unicode__(self):
        return "%s %s" % (self.merchant, self.date.strftime("%m-%d-%Y"))

    def add_tag(self, tag):
        if tag in self.tags:
            raise ValueError("Already have tag!")
        if tag not in self.mint.tags:
            raise ValueError("Tag does not exist!")
        self.tags.add(tag)

    def update(self):
        d = {'task' : 'txnedit', 'txnId' : "%s:false" % self.id, 'token' : self.mint.token}
        for tag in self.mint.tags:
            d['tag%d' % tag.id] = 2 if tag in self.tags else 0
        response = self.mint.fetch_url('updateTransaction.xevent', d, method=urlfetch.POST)
        return response

