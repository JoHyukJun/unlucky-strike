from django.db import models

class Project(models.Model):
    pass

class ETF(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ETF 이름
    ticker = models.CharField(max_length=20, unique=True) # 종목 코드

    def __str__(self):
        return f"{self.name} ({self.ticker})"

class Dividend(models.Model):
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE, related_name='dividends')
    amount = models.DecimalField(max_digits=16, decimal_places=6)  # 배당금
    paid_date = models.DateField()  # 배당 지급일
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)  # 통화

    def __str__(self):
        return f"{self.etf.name} - {self.paid_date}: {self.amount} {self.currency}"

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 통화 코드 (예: USD, EUR)
    name = models.CharField(max_length=100)              # 통화 이름 (예: US Dollar)

    def __str__(self):
        return f"{self.name} ({self.code})"