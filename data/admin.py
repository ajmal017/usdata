from django.contrib import admin

from data.models import (
    Tickers,
    Price,
    General,
    Highlights,
    Valuation,
    SharesStats,
    ESGScores,
    Earnings,
    Financials
)

admin.site.register(Tickers)
admin.site.register(Price)
admin.site.register(General)
admin.site.register(Highlights)
admin.site.register(Valuation)
admin.site.register(SharesStats)
admin.site.register(ESGScores)
admin.site.register(Earnings)
admin.site.register(Financials)