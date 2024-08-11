from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def clean(self):
        if self.quantity < 0 and self.average_purchase_price < 0:
            raise ValidationError('Quantity and average purchase price cannot be negative.')
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative')
        if self.average_purchase_price < 0:
            raise ValidationError('Average purchase price cannot be negative')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.ticker.ticker}: {self.quantity} shares at {self.average_purchase_price}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_dividend_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if self.monthly_dividend_goal < 0:
            raise ValidationError('Monthly dividend goal cannot be negative.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username