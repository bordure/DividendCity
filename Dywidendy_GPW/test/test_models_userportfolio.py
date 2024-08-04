from django.test import TestCase
from django.contrib.auth.models import User
from Dywidendy_GPW.models import UserPortfolio, CompaniesName

class UserPortfolioModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.company_name = CompaniesName.objects.create(
            ticker='AAPL',
            name='Apple Inc.'
        )
        cls.user_portfolio = UserPortfolio.objects.create(
            user=cls.user,
            ticker=cls.company_name,
            quantity=10,
            average_purchase_price=100.00
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.user_portfolio.delete()
        cls.company_name.delete()
        cls.user.delete()
        super().tearDownClass()
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.user_portfolio),
            'testuser - AAPL: 10 shares at 100.0'
        )
    
    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            UserPortfolio.objects.create(
                user=self.user,
                ticker=self.company_name,
                quantity=20,
                average_purchase_price=110.00
            )

    def test_quantity_field(self):
        self.assertEqual(self.user_portfolio.quantity, 10)
    
    def test_average_purchase_price_field(self):
        self.assertEqual(self.user_portfolio.average_purchase_price, 100.00)
