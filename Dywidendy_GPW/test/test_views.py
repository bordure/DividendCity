from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from Dywidendy_GPW.models import UserPortfolio, CompaniesName, CompaniesPrice, CompaniesDividend, UserProfile
from django.db.models.signals import post_save
from Dywidendy_GPW.signals import create_user_profile, save_user_profile

class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.factory = RequestFactory()

        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)

        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=cls.user, monthly_dividend_goal=500)

        company = CompaniesName.objects.create(ticker="AAPL", name="Apple Inc.")
        UserPortfolio.objects.create(user=cls.user, ticker=company, quantity=10, average_purchase_price=100)
        CompaniesPrice.objects.create(ticker="AAPL", price=150)
        CompaniesDividend.objects.create(
            ticker="AAPL",
            value_of_dividend=5,
            date_of_dividend="2023-12-31",
            ex_dividend_date="2023-11-30",
            price_of_dividend=151616
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def login(self):
        self.client.login(username='testuser', password='testpassword')

    def test_user_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_user_login_post(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('portfolio'))

    def test_user_logout(self):
        self.login()
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_portfolio_view(self):
        self.login()
        response = self.client.get(reverse('portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('portfolio', response.context)
        self.assertIn('total_holdings_value', response.context)
        self.assertIn('total_profit_percentage', response.context)
        self.assertIn('total_profit_pln', response.context)

    def test_add_stock_get(self):
        self.login()
        response = self.client.get(reverse('add_stock'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('companies', response.context)

    def test_add_stock_post(self):
        self.login()
        CompaniesName.objects.create(ticker="TCKT", name="Test ticker")
        response = self.client.post(reverse('add_stock'), {
            'ticker': 'TCKT',
            'quantity': 10,
            'average_purchase_price': 100
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('portfolio'))

    def test_autocomplete_companies(self):
        self.login()
        response = self.client.get(reverse('autocomplete_companies'), {'term': 'Apple'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': 'AAPL', 'label': 'Apple Inc.(AAPL)', 'value': 'AAPL'}])

    def test_dividends_view(self):
        self.login()
        response = self.client.get(reverse('dividends'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('dividend_table_data', response.context)
        self.assertIn('total_annual_dividends', response.context)
        self.assertIn('total_monthly_dividends', response.context)
        self.assertIn('dividend_yield', response.context)
        self.assertIn('dividend_goal', response.context)

    def test_company_info_view(self):
        self.login()
        response = self.client.get(reverse('company_info', args=['AAPL']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('company', response.context)
        self.assertIn('dividends', response.context)
        self.assertIn('dividend_dates', response.context)
        self.assertIn('dividend_values', response.context)
        self.assertIn('in_portfolio', response.context)
        self.assertIn('portfolio_stock', response.context)

    def test_edit_stock_get(self):
        self.login()
        stock = UserPortfolio.objects.get(ticker__ticker='AAPL')
        response = self.client.get(reverse('edit_stock', args=[stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('stock', response.context)

    def test_edit_stock_post(self):
        self.login()
        stock = UserPortfolio.objects.get(ticker__ticker='AAPL')
        response = self.client.post(reverse('edit_stock', args=[stock.id]), {
            'quantity': 15,
            'average_purchase_price': 110
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('portfolio'))

    def test_delete_stock(self):
        self.login()
        stock = UserPortfolio.objects.get(ticker__ticker='AAPL')
        response = self.client.post(reverse('delete_stock', args=[stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('portfolio'))

    def test_dividend_calendar_view(self):
        self.login()
        response = self.client.get(reverse('dividend_calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('forthcoming_dividends', response.context)
    
    def test_main_page_view(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
    
        
    def test_set_dividend_goal_get(self):
        self.login()
        response = self.client.get(reverse('set_dividend_goal'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_set_dividend_goal_post(self):
        self.login()
        response = self.client.post(reverse('set_dividend_goal'), {'monthly_dividend_goal': 600})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dividends'))
        user_profile = UserProfile.objects.get(user__username='testuser')
        self.assertEqual(user_profile.monthly_dividend_goal, 600)
    

    def test_input_investment_get(self):
        self.login()
        response = self.client.get(reverse('input_investment'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_input_investment_post(self):
        self.login()
        response = self.client.post(reverse('input_investment'), {'monthly_investment': 1000})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('simulate_dividend_results'))
        self.assertEqual(self.client.session['monthly_investment'], 1000)

    def test_simulate_dividend_results(self):
        self.login()
        session = self.client.session
        session['monthly_investment'] = 1000
        session.save()

        response = self.client.get(reverse('simulate_dividend_results'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.context)
        self.assertIn('years_to_reach_goal', response.context)
        self.assertIn('goal', response.context)
        self.assertIn('dividend_yield', response.context)
        self.assertIn('total_monthly_dividends', response.context)
        self.assertIn('monthly_investment', response.context)

        results = response.context['results']
        self.assertTrue(len(results) > 0)