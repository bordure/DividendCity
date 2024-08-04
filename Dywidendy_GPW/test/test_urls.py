from django.test import SimpleTestCase
from django.urls import resolve, reverse
from Dywidendy_GPW import views

class UrlsTest(SimpleTestCase):

    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        self.assertEqual(resolve(url).func.__module__, 'django.contrib.admin.sites')

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.user_logout)

    def test_portfolio_url_resolves(self):
        url = reverse('portfolio')
        self.assertEqual(resolve(url).func, views.portfolio)

    def test_add_stock_url_resolves(self):
        url = reverse('add_stock')
        self.assertEqual(resolve(url).func, views.add_stock)

    def test_autocomplete_companies_url_resolves(self):
        url = reverse('autocomplete_companies')
        self.assertEqual(resolve(url).func, views.autocomplete_companies)

    def test_dividends_url_resolves(self):
        url = reverse('dividends')
        self.assertEqual(resolve(url).func, views.dividends)

    def test_company_info_url_resolves(self):
        url = reverse('company_info', args=['AAPL'])
        self.assertEqual(resolve(url).func, views.company_info)

    def test_edit_stock_url_resolves(self):
        url = reverse('edit_stock', args=[1])
        self.assertEqual(resolve(url).func, views.edit_stock)

    def test_delete_stock_url_resolves(self):
        url = reverse('delete_stock', args=[1])
        self.assertEqual(resolve(url).func, views.delete_stock)

    def test_dividend_calendar_url_resolves(self):
        url = reverse('dividend_calendar')
        self.assertEqual(resolve(url).func, views.dividend_calendar)

    def test_set_dividend_goal_url_resolves(self):
        url = reverse('set_dividend_goal')
        self.assertEqual(resolve(url).func, views.set_dividend_goal)

    def test_simulate_dividend_results_url_resolves(self):
        url = reverse('simulate_dividend_results')
        self.assertEqual(resolve(url).func, views.simulate_dividend_results)

    def test_input_investment_url_resolves(self):
        url = reverse('input_investment')
        self.assertEqual(resolve(url).func, views.input_investment)

    def test_main_page_url_resolves(self):
        url = reverse('main_page')
        self.assertEqual(resolve(url).func, views.main_page)
