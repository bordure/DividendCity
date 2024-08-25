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

class AddStockForm(forms.Form):
    ticker = forms.CharField(widget=forms.TextInput(attrs={'id': 'ticker'}))
    quantity = forms.DecimalField(max_digits=8) 
    average_purchase_price = forms.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()

        ticker_value = cleaned_data.get('ticker')
        quantity = cleaned_data.get('quantity')
        average_purchase_price = cleaned_data.get('average_purchase_price')

        if ticker_value and not CompaniesName.objects.filter(ticker=ticker_value).exists():
            raise forms.ValidationError("Company with this ticker does not exist.")
        
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError("Quantity cannot be equal to 0 or less")
        
        if average_purchase_price is not None and average_purchase_price <= 0:
            raise forms.ValidationError("Average purchase price cannot be equal to 0 or less")
        
        return cleaned_data