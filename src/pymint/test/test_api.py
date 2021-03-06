from mint.api import Mint
from mint import mint
import unittest
from itertools import islice

class Test(unittest.TestCase):
    def xtest_export(self):
        results = mint.export_all()
        result = results.next()
        for key in 'Date,Description,Original Description,Amount,Transaction Type,Category,Account Name,Labels,Notes'.split(','):
            assert key in result
        
    def test_tags(self):
        for r in mint.tags:
            assert r.id > 0
            print r

    def xtest_transactions(self):
        import datetime
        old_date = datetime.datetime.now()
        for t in islice(mint.transactions, 40):
            assert t.date <= old_date
            old_date = t.date
#        assert False    
    
    def xtest_update(self):
        tx = mint.transactions.next()
        tx.add_tag(mint.tags['Home'])
        tx.update()
         
    def xtest_get_or_create_tag(self):
        test, created = mint.get_or_create_tag('XX Test')   
        if created:
            test.delete()
            assert False
        random, created = mint.get_or_create_tag('XXTESTTAG')
        random.delete()
        assert created == True
        
