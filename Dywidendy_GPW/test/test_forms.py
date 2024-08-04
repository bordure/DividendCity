from django.test import TestCase
from Dywidendy_GPW.forms import EditStockForm, DividendGoalForm, InvestmentForm
from Dywidendy_GPW.models import User, UserPortfolio, CompaniesName, UserProfile
from Dywidendy_GPW.signals import create_user_profile, save_user_profile
from django.db.models.signals import post_save


class EditStockFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.company = CompaniesName.objects.create(ticker='AAPL', name='Apple Inc.')
        cls.portfolio = UserPortfolio.objects.create(user=cls.user, ticker=cls.company, quantity=10, average_purchase_price=100)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.company.delete()
        cls.portfolio.delete()
        super().tearDownClass()

    def test_valid_data(self):
        form = EditStockForm(data={
            'quantity': 20,
            'average_purchase_price': 150
        }, instance=self.portfolio)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = EditStockForm(data={
            'quantity': -5,
            'average_purchase_price': 'invalid'
        }, instance=self.portfolio)
        self.assertFalse(form.is_valid())

class DividendGoalFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.user_profile = UserProfile.objects.create(user=cls.user, monthly_dividend_goal=500)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.user_profile.delete()
        super().tearDownClass()

    def test_valid_data(self):
        form = DividendGoalForm(data={'monthly_dividend_goal': 600}, instance=self.user_profile)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = DividendGoalForm(data={'monthly_dividend_goal': 'invalid'}, instance=self.user_profile)
        self.assertFalse(form.is_valid())

class InvestmentFormTests(TestCase):

    def test_valid_data(self):
        form = InvestmentForm(data={'monthly_investment': 1000.00})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = InvestmentForm(data={'monthly_investment': 'invalid'})
        self.assertFalse(form.is_valid())

    def test_negative_investment(self):
        form = InvestmentForm(data={'monthly_investment': -1000.00})
        self.assertFalse(form.is_valid())
        self.assertIn('Monthly investment must be a positive number.', form.errors['monthly_investment'])
