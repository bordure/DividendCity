from django.db import models
from django.contrib.auth.models import User

class CompaniesPrice(models.Model):
    ticker = models.CharField(max_length=255, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dividend_consecutive_years = models.IntegerField(default=0)
    dividend_growing_consecutive_years = models.IntegerField(default=0)

    class Meta:
        db_table = 'companies_price'

    def __str__(self):
        return f"{self.ticker} {self.price} {self.dividend_consecutive_years} {self.dividend_growing_consecutive_years}"

class CompaniesName(models.Model):
    ticker = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'companies_name'

    def __str__(self):
        return f"{self.ticker}: {self.name}"

class CompaniesDividend(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=255)
    date_of_dividend = models.DateField()
    ex_dividend_date = models.DateField()
    value_of_dividend = models.DecimalField(max_digits=10, decimal_places=2)
    price_of_dividend = models.BigIntegerField()

    class Meta:
        db_table = 'companies_dividend'

    def __str__(self):
        return f"{self.ticker} {self.date_of_dividend} {self.ex_dividend_date} {self.value_of_dividend} {self.price_of_dividend}"

class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.ForeignKey(CompaniesName, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    average_purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'ticker')

    def __str__(self):
        return f"{self.user.username} - {self.ticker.ticker}: {self.quantity} shares at {self.average_purchase_price}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_dividend_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username