from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('autocomplete_companies/', views.autocomplete_companies, name='autocomplete_companies'),
    path('dividends/', views.dividends, name='dividends'),
    path('company/<str:ticker>/', views.company_info, name='company_info'),
    path('edit_stock/<int:stock_id>/', views.edit_stock, name='edit_stock'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('dividend_calendar/', views.dividend_calendar, name='dividend_calendar'),
    path('set_dividend_goal/', views.set_dividend_goal, name='set_dividend_goal'),
    path('simulate_dividend_results/', views.simulate_dividend_results, name='simulate_dividend_results'),
    path('input_investment/', views.input_investment, name='input_investment'),
    path('search/', views.search_companies, name='search'),
    path('', views.main_page, name='main_page'),
]
