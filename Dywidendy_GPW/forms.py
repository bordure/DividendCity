from django import forms
from .models import UserProfile, CompaniesName, UserPortfolio

class EditStockForm(forms.ModelForm):
    class Meta:
        model = UserPortfolio
        fields = ['quantity', 'average_purchase_price']

class DividendGoalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['monthly_dividend_goal']
        widgets = {
            'monthly_dividend_goal': forms.NumberInput(attrs={'class': 'form-control form-control-dark'}),
        }

class InvestmentForm(forms.Form):
    monthly_investment = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Monthly Investment (PLN)',
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount in PLN'})
    )

    def clean_monthly_investment(self):
        data = self.cleaned_data['monthly_investment']
        if data < 0:
            raise forms.ValidationError("Monthly investment must be a positive number.")
        return data

class AddStockForm(forms.ModelForm):
    ticker = forms.CharField(widget=forms.TextInput(attrs={'id': 'ticker'}))

    class Meta:
        model = UserPortfolio
        fields = ['ticker', 'quantity', 'average_purchase_price']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddStockForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(AddStockForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

    def clean_ticker(self):
        ticker_value = self.cleaned_data.get('ticker')
        print("ticker from forms", ticker_value)
        if not CompaniesName.objects.filter(ticker=ticker_value).exists():
            raise forms.ValidationError("Company with this ticker does not exist.")
        company = CompaniesName.objects.get(ticker=ticker_value)
        return company
