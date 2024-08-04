from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
from .models import CompaniesName, CompaniesPrice, UserPortfolio, CompaniesDividend, UserProfile
from .forms import EditStockForm, DividendGoalForm, InvestmentForm
from datetime import datetime
from datetime import timedelta, date    

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not hasattr(user, 'userprofile'):
                    UserProfile.objects.create(user=user)
                login(request, user)
                return redirect("portfolio")
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def portfolio(request):
    portfolio = UserPortfolio.objects.filter(user=request.user)
    total_holdings_value = 0
    total_profit_percentage = 0
    total_purchase_price = 0
    total_profit_pln = 0
    
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

            #calculate total holdings value
            total_holdings_value += float(stock.quantity) * float(stock.current_price)
            total_purchase_price += float(stock.quantity) * float(stock.average_purchase_price)

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

        total_profit_percentage = (total_holdings_value - total_purchase_price) / total_purchase_price * 100
        total_profit_pln = total_holdings_value - total_purchase_price

        context = {
            'portfolio': portfolio,
            'total_holdings_value': round(total_holdings_value,2),
            'total_profit_percentage': round(total_profit_percentage,2),
            'total_profit_pln': round(total_profit_pln, 2),
        }
        
    return render(request, 'portfolio.html', context)

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
    current_year = datetime.now().year
    portfolio = UserPortfolio.objects.filter(user=request.user).select_related('ticker')
    profile = UserProfile.objects.get(user=request.user)
    monthly_goal = profile.monthly_dividend_goal
    
    total_annual_dividends = 0
    dividend_table_data = []
    dividend_yield = 0
    number_of_dividends = 0
    
    for item in portfolio:
        dividends = CompaniesDividend.objects.filter(ticker=item.ticker.ticker, date_of_dividend__year=current_year)
        total_dividend_value = dividends.aggregate(total=Sum('value_of_dividend'))['total'] or 0
        monthly_dividend_value = total_dividend_value / 12
        daily_dividend_value = total_dividend_value / 365
        dividend_value_per_stock = item.quantity * total_dividend_value
    
        if total_dividend_value == 0:
            continue
        
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
    total_monthly_dividends = round(total_annual_dividends / 12,2)
    total_daily_dividends = round(total_annual_dividends / 365,2)
    percentage_accomplished = (total_monthly_dividends / monthly_goal) * 100 if monthly_goal > 0 else 0
    remaining_percentage = 100 - percentage_accomplished
    remaining_goal = monthly_goal - total_monthly_dividends

    context = {
        'dividend_table_data': dividend_table_data,
        'total_annual_dividends': total_annual_dividends,
        'total_monthly_dividends': total_monthly_dividends,
        'total_daily_dividends': total_daily_dividends,
        'dividend_yield': round(dividend_yield,2),
        'dividend_goal': monthly_goal,
        'percentage_accomplished': percentage_accomplished,
        'remaining_percentage': remaining_percentage,
        'remaining_goal': remaining_goal,
    }
    
    return render(request, 'dividends.html', context)

@login_required
def company_info(request, ticker):
    company = get_object_or_404(CompaniesName, ticker=ticker)
    dividends = CompaniesDividend.objects.filter(ticker=ticker).order_by('-date_of_dividend')
    
    # Prepare data for the chart
    dividend_dates = [div.date_of_dividend.strftime('%Y-%m-%d') for div in dividends][::-1]
    dividend_values = [float(div.value_of_dividend) for div in dividends][::-1]
    print(dividend_dates, dividend_values)
    
    # Check if the company is in the user's portfolio
    try:
        portfolio_stock = UserPortfolio.objects.get(user=request.user, ticker__ticker=ticker)
        in_portfolio = True
    except UserPortfolio.DoesNotExist:
        portfolio_stock = None
        in_portfolio = False

    context = {
        'company': company,
        'dividends': dividends,
        'dividend_dates': dividend_dates,
        'dividend_values': dividend_values,
        'in_portfolio': in_portfolio,
        'portfolio_stock': portfolio_stock,
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

    context = {
        'form': form,
        'stock': stock,
    }
    return render(request, 'edit_stock.html', context)

@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(UserPortfolio, id=stock_id, user=request.user)
    
    if request.method == 'POST':
        stock.delete()
        return redirect('portfolio')

    return redirect('portfolio')

@login_required
def dividend_calendar(request):
    portfolio = UserPortfolio.objects.filter(user=request.user)
    forthcoming_dividends = []

    for stock in portfolio:
        try:
            companies_dividends = CompaniesDividend.objects.filter(ticker=stock.ticker.ticker, date_of_dividend__gt=date.today()-timedelta(days=1)).order_by('date_of_dividend')
            company_name = CompaniesName.objects.get(ticker=stock.ticker.ticker).name
            
            for div in companies_dividends:
                forthcoming_dividends.append({
                    'name': company_name,
                    'ticker': stock.ticker.ticker,
                    'date_of_dividend': div.date_of_dividend,
                    'value_of_dividend': div.value_of_dividend,
                    'total_dividend': stock.quantity * div.value_of_dividend
                })
        except Exception as e:
            continue

    forthcoming_dividends.sort(key=lambda x: x['date_of_dividend'])

    context = {
        'forthcoming_dividends': forthcoming_dividends,
    }

    return render(request, 'dividend_calendar.html', context)

def main_page(request):
    return render(request, 'main_page.html')

@login_required
def set_dividend_goal(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = DividendGoalForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dividends')
    else:
        form = DividendGoalForm(instance=profile)
    return render(request, 'set_dividend_goal.html', {'form': form})

@login_required
def input_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            monthly_investment = float(form.cleaned_data['monthly_investment'])
            request.session['monthly_investment'] = monthly_investment
            return redirect('simulate_dividend_results')
    else:
        form = InvestmentForm()
    
    return render(request, 'input_investment.html', {'form': form})

@login_required
def simulate_dividend_results(request):
    monthly_investment = request.session.get('monthly_investment')
    
    if not monthly_investment:
        return redirect('input_investment')

    monthly_investment = float(monthly_investment) 

    current_year = datetime.now().year
    portfolio = UserPortfolio.objects.filter(user=request.user).select_related('ticker')
    profile = UserProfile.objects.get(user=request.user)
    monthly_goal = profile.monthly_dividend_goal


    total_annual_dividends = 0
    dividend_yield = 0
    number_of_dividends = 0

    for item in portfolio:
        dividends = CompaniesDividend.objects.filter(ticker=item.ticker.ticker, date_of_dividend__year=current_year)
        total_dividend_value = dividends.aggregate(total=Sum('value_of_dividend'))['total'] or 0
        dividend_value_per_stock = item.quantity * total_dividend_value

        if total_dividend_value == 0:
            continue

        total_annual_dividends += dividend_value_per_stock
        dividend_yield += (total_dividend_value / item.average_purchase_price) * 100
        number_of_dividends += 1

    if number_of_dividends > 0:
        dividend_yield /= number_of_dividends

    total_monthly_dividends = round(total_annual_dividends / 12, 2)
    
    dividend_yield = float(dividend_yield)
    goal = float(monthly_goal)

    portfolio_value = 0
    for item in portfolio:
        try:
            current_price_obj = CompaniesPrice.objects.get(ticker=item.ticker.ticker)
            current_price = float(current_price_obj.price)
            portfolio_value += item.quantity * current_price
        except CompaniesPrice.DoesNotExist:
            continue 

    results = []
    years = 0
    future_monthly_dividends = float(total_monthly_dividends)
    
    while future_monthly_dividends < goal:
        years += 1
        portfolio_value += float(monthly_investment) * 12 
        future_annual_dividends = float(portfolio_value) * (float(dividend_yield)/100)
        portfolio_value += float(future_annual_dividends)  
        future_monthly_dividends = round(future_annual_dividends / 12, 2)  

        results.append({
            'year': years,
            'portfolio_value': round(portfolio_value, 2),
            'monthly_dividends': future_monthly_dividends
        })

    context = {
        'results': results,
        'years_to_reach_goal': years,
        'goal': goal,
        'dividend_yield': round(dividend_yield, 2),
        'total_monthly_dividends': total_monthly_dividends,
        'monthly_investment': monthly_investment
    }

    request.session.pop('monthly_investment', None)

    return render(request, 'simulate_dividend_results.html', context)