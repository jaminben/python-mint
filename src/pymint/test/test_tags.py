import unittest
from mint.tags import Tag, TagSet
import mint

TEST_TAGSET = [
    {'id' : 1, 'value' : 'Mom & Dad'},
    {'id' : 2, 'value' : 'Reimbursable'},
    {'id' : 3, 'value' : 'Tax Deduction'},
]


class Test(unittest.TestCase):
    def test_tagset(self):
        tagset = TagSet.from_json(TEST_TAGSET, mint.mint)
        assert len(tagset.parse('Reimbursable Mom & Dad')) == 2

    def test_tags(self):       
        tagset1 = TagSet.from_json(TEST_TAGSET, mint.mint)
        tagset2 = TagSet.from_json(TEST_TAGSET, mint.mint)
        assert tagset1 != tagset2
        for tag in tagset1:
            assert id(tag) == id(tagset2[tag.name])

