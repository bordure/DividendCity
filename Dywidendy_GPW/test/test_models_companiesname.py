from django.test import TestCase
from Dywidendy_GPW.models import CompaniesName

class CompaniesNameModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_name = CompaniesName.objects.create(
            ticker='AAPL',
            name='Apple Inc.'
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.company_name.delete()
        super().tearDownClass()
    
    def test_string_representation(self):
        self.assertEqual(str(self.company_name), 'AAPL: Apple Inc.')
    
    def test_ticker_field(self):
        self.assertEqual(self.company_name.ticker, 'AAPL')
    
    def test_name_field(self):
        self.assertEqual(self.company_name.name, 'Apple Inc.')
