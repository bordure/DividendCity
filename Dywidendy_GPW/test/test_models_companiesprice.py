from django.test import TestCase
from Dywidendy_GPW.models import CompaniesPrice

class CompaniesPriceModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_price = CompaniesPrice.objects.create(
            ticker='AAPL',
            price='150.00',
            dividend_consecutive_years=2,
            dividend_growing_consecutive_years=0
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.company_price.delete()
        super().tearDownClass()
    
    def test_string_representation(self):
        self.assertEqual(str(self.company_price), 'AAPL 150.00 2 0')
    
    def test_ticker_field(self):
        self.assertEqual(self.company_price.ticker, 'AAPL')
    
    def test_price_field(self):
        self.assertEqual(self.company_price.price, '150.00')

    def test_dividend_consecutive_years_field(self):
        self.assertEqual(self.company_price.dividend_consecutive_years, 2)
    
    def test_dividend_growing_consecutive_years_field(self):
        self.assertEqual(self.company_price.dividend_growing_consecutive_years, 0)