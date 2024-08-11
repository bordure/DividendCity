from django.test import TestCase
from django.contrib.auth.models import User
from Dywidendy_GPW.models import UserPortfolio, CompaniesName
from django.core.exceptions import ValidationError

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
    
    def test_negative_quantity_raises_validation_error(self):
        with self.assertRaises(ValidationError) as cm:
            UserPortfolio.objects.create(
                user=self.user,
                ticker=self.company_name,
                quantity=-5,
                average_purchase_price=100.00
            )
        self.assertIn('Quantity cannot be negative', cm.exception.messages)

    def test_negative_average_purchase_price_raises_validation_error(self):
        with self.assertRaises(ValidationError) as cm:
            UserPortfolio.objects.create(
                user=self.user,
                ticker=self.company_name,
                quantity=10,
                average_purchase_price=-100.00  
            )
        self.assertIn('Average purchase price cannot be negative', cm.exception.messages)
    
    def test_negative_quantity_and_price_raises_validation_error(self):
        with self.assertRaises(ValidationError) as cm:
            UserPortfolio.objects.create(
                user=self.user,
                ticker=self.company_name,
                quantity=-5,
                average_purchase_price=-100.00
            )
        self.assertIn('Quantity and average purchase price cannot be negative.', cm.exception.messages)
