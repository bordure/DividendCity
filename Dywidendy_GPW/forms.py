from django import forms
from .models import UserPortfolio, UserProfile

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