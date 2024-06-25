from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from .models import CompaniesName, CompaniesPrice, UserPortfolio, CompaniesDividend
from .forms import EditStockForm 
from datetime import datetime

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('portfolio')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def portfolio(request):
    portfolio = UserPortfolio.objects.filter(user=request.user)
    
    for stock in portfolio:
        try:
            # Fetch current price from CompaniesPrice
            current_price_obj = CompaniesPrice.objects.get(ticker=stock.ticker.ticker)
            stock.current_price = float(current_price_obj.price)
            
            # Calculate current value
            stock.current_value = round(stock.quantity * stock.current_price,2)
            
            # Calculate profit
            stock.profit = float(stock.current_value) - (float(stock.average_purchase_price) * float(stock.quantity))
            stock.profit = round(stock.profit, 2)
            
            # Calculate percentage
            if stock.average_purchase_price != 0:
                stock.percentage = (float(stock.profit) / (float(stock.average_purchase_price) * float(stock.quantity))) * 100
            else:
                stock.percentage = 0
            stock.percentage = round(stock.percentage,2)
                
            # Determine profit/loss color
            if stock.profit >= 0:
                stock.profit_color = 'green'
            else:
                stock.profit_color = 'red'
        
        except CompaniesPrice.DoesNotExist:
            stock.current_price = 0.0
            stock.current_value = 0.0
            stock.profit = 0.0
            stock.percentage = 0.0
            stock.profit_color = 'black'  # Handle missing price
        
    return render(request, 'portfolio.html', {'portfolio': portfolio})

@login_required
def add_stock(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        quantity = int(request.POST['quantity'])
        average_purchase_price = float(request.POST['average_purchase_price'])
        company = CompaniesName.objects.get(ticker=ticker)
        portfolio_item, created = UserPortfolio.objects.get_or_create(
            user=request.user, ticker=company,
            defaults={'quantity': quantity, 'average_purchase_price': average_purchase_price}
        )
        if not created:
            portfolio_item.quantity += quantity
            portfolio_item.average_purchase_price = (
                (portfolio_item.average_purchase_price * portfolio_item.quantity + average_purchase_price * quantity)
                / (portfolio_item.quantity + quantity)
            )
            portfolio_item.save()
        return redirect('portfolio')
    else:
        companies = CompaniesName.objects.all()
        return render(request, 'add_stock.html', {'companies': companies})

def autocomplete_companies(request):
    term = request.GET.get('term')
    companies = CompaniesName.objects.filter(name__icontains=term)[:10]  # Filter companies containing the search term
    data = [{'id': company.ticker, 'label': f'{company.name}({company.ticker})', 'value': company.ticker} for company in companies]
    return JsonResponse(data, safe=False)

def dividends(request):
    # Get current year
    current_year = datetime.now().year
    
    # Retrieve user's portfolio with related ticker information
    portfolio = UserPortfolio.objects.filter(user=request.user).select_related('ticker')
    
    # Calculate total annual dividends and prepare data for table
    total_annual_dividends = 0
    dividend_table_data = []
    dividend_yield = 0
    number_of_dividends = 0
    
    for item in portfolio:
        # Query dividends for the current year and calculate total value for each ticker
        dividends = CompaniesDividend.objects.filter(ticker=item.ticker.ticker, date_of_dividend__year=current_year)
        total_dividend_value = dividends.aggregate(total=Sum('value_of_dividend'))['total'] or 0
        
        # Calculate monthly and daily dividends based on total dividend value
        monthly_dividend_value = total_dividend_value / 12
        daily_dividend_value = total_dividend_value / 365
        
        # Calculate dividend value based on quantity of stocks
        dividend_value_per_stock = item.quantity * total_dividend_value
    
        if total_dividend_value == 0:
            continue
        
        # Prepare data for dividend table
        dividend_table_data.append({
            'ticker': item.ticker.ticker,
            'name': item.ticker.name,
            'quantity': item.quantity,
            'annual_dividend_value': dividend_value_per_stock,
            'monthly_dividend_value': round(dividend_value_per_stock / 12,2),
            'daily_dividend_value': round(dividend_value_per_stock / 365,2),
        })
        
        
        # Accumulate total annual dividends
        total_annual_dividends += dividend_value_per_stock
        dividend_yield += (total_dividend_value / item.average_purchase_price) * 100
        number_of_dividends += 1

    dividend_yield /= number_of_dividends
    #dividend_yield = 0
    # Convert total annual dividends to monthly and daily values
    total_monthly_dividends = round(total_annual_dividends / 12,2)
    total_daily_dividends = round(total_annual_dividends / 365,2)
    
    context = {
        'dividend_table_data': dividend_table_data,
        'total_annual_dividends': total_annual_dividends,
        'total_monthly_dividends': total_monthly_dividends,
        'total_daily_dividends': total_daily_dividends,
        'dividend_yield': round(dividend_yield,2),
    }
    
    return render(request, 'dividends.html', context)

def company_info(request, ticker):
    company = get_object_or_404(CompaniesName, ticker=ticker)
    dividends = CompaniesDividend.objects.filter(ticker=ticker).order_by('-date_of_dividend')
    
    # Prepare data for the chart
    dividend_dates = [div.date_of_dividend.strftime('%Y-%m-%d') for div in dividends][::-1]
    dividend_values = [float(div.value_of_dividend) for div in dividends][::-1]
    print(dividend_dates, dividend_values)
    context = {
        'company': company,
        'dividends': dividends,
        'dividend_dates': dividend_dates,
        'dividend_values': dividend_values,
    }
    return render(request, 'company_info.html', context)

@login_required
def edit_stock(request, stock_id):
    stock = get_object_or_404(UserPortfolio, id=stock_id, user=request.user)

    if request.method == 'POST':
        form = EditStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('portfolio')
    else:
        form = EditStockForm(instance=stock)

    return render(request, 'edit_stock.html', {'form': form})

@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(UserPortfolio, id=stock_id, user=request.user)

    if request.method == 'POST':
        stock.delete()
        return redirect('portfolio')

    return render(request, 'confirm_delete.html', {'stock': stock})