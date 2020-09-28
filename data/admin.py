from django.contrib import admin

from data.models import (
    MetaDate,
    MetaData,
    Tickers,
    BulkPrice,
    Price,
    General,
    Highlights,
    Valuation,
    SharesStats,
    ESGScores,
    Earnings,
    Financials,
    BulkFinancials
)

# admin.site.register(MetaDate)
# admin.site.register(MetaData)
admin.site.register(Tickers)
admin.site.register(BulkPrice)
admin.site.register(Price)
admin.site.register(General)
admin.site.register(Highlights)
admin.site.register(Valuation)
admin.site.register(SharesStats)
admin.site.register(ESGScores)
admin.site.register(Earnings)
admin.site.register(Financials)
admin.site.register(BulkFinancials)
