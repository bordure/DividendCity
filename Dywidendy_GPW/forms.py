from django import forms
from .models import UserPortfolio

class EditStockForm(forms.ModelForm):
    class Meta:
        model = UserPortfolio
        fields = ['quantity', 'average_purchase_price']
