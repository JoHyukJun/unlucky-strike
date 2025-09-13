from django.contrib import admin
from .models import ETF, Dividend, Currency

admin.site.register(ETF)
admin.site.register(Dividend)
admin.site.register(Currency)
