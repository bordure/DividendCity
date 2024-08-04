from django.test import TestCase
from Dywidendy_GPW.models import CompaniesDividend

class CompaniesDividendModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_dividend = CompaniesDividend.objects.create(
            ticker='AAPL',
            date_of_dividend='2023-12-31',
            ex_dividend_date='2023-11-30',
            value_of_dividend=5.00,
            price_of_dividend=151616
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.company_dividend.delete()
        super().tearDownClass()
    
    def test_string_representation(self):
        self.assertEqual(str(self.company_dividend), 'AAPL 2023-12-31 2023-11-30 5.0 151616')
    
    def test_ticker_field(self):
        self.assertEqual(self.company_dividend.ticker, 'AAPL')
    
    def test_value_of_dividend_field(self):
        self.assertEqual(self.company_dividend.value_of_dividend, 5.00)
    
    def test_price_of_dividend_field(self):
        self.assertEqual(self.company_dividend.price_of_dividend, 151616)
