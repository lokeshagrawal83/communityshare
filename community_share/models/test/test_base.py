import unittest

from community_share.models.base import Serializable


class TestClass(Serializable):
    STANDARD_READABLE_FIELDS = ['mundane_data', 'mundane_custom_data']
    ADMIN_READABLE_FIELDS = STANDARD_READABLE_FIELDS + ['secret_data', 'secret_custom_data']

    custom_serializers = {
        'mundane_custom_data': lambda self, _: self.mundane_custom_data * 2,
        'secret_custom_data': lambda self, _: self.secret_custom_data * 2
    }

    def __init__(self):
        self.mundane_data = 'mundane_value'
        self.secret_data = 'secret_value'
        self.mundane_custom_data = 'mundane_value'
        self.secret_custom_data = 'secret_value'


class Requester:
    def __init__(self, is_administrator=False):
        self.is_administrator = is_administrator


class BaseSerializeTest(unittest.TestCase):

    def test_no_requester(self):
        d = TestClass().serialize(None)
        self.assertEqual(None, d)

    def test_standard(self):
        d = TestClass().serialize(Requester())
        self.assertDictEqual({
            'mundane_data': 'mundane_value',
            'mundane_custom_data': 'mundane_value' * 2
        }, d)

    def test_admin(self):
        d = TestClass().serialize(Requester(is_administrator=True))
        self.assertDictEqual({
            'mundane_data': 'mundane_value',
            'mundane_custom_data': 'mundane_value' * 2,
            'secret_data': 'secret_value',
            'secret_custom_data': 'secret_value' * 2
        }, d)

    def test_standard_with_exclude(self):
        d = TestClass().serialize(Requester(), exclude=['mundane_data'])
        self.assertDictEqual({
            'mundane_custom_data': 'mundane_value' * 2
        }, d)

    def test_admin_with_exclude(self):
        d = TestClass().serialize(
            Requester(is_administrator=True),
            exclude=['mundane_data', 'secret_custom_data']
        )
        self.assertDictEqual({
            'mundane_custom_data': 'mundane_value' * 2,
            'secret_data': 'secret_value',
        }, d)

if __name__ == '__main__':
    unittest.main()
