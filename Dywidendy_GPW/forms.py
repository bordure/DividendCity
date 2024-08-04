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
