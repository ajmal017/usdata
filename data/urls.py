from django.urls import path

from data.views import (
    TickersAPIView,
    BulkPriceAPIView,
    PriceAPIView,
    GeneralAPIView,
    HighlightsAPIView,
    ValuationAPIView,
    SharesStatsAPIView,
    ESGScoresAPIView,
    EarningsAPIView,
    FinancialsAPIView
)


from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('tickers/', TickersAPIView.as_view()),
    path('raw-price/', BulkPriceAPIView.as_view()),
    path('price/', PriceAPIView.as_view()),
    path('general/', GeneralAPIView.as_view()),
    path('highlights/', HighlightsAPIView.as_view()),
    path('valuation/', ValuationAPIView.as_view()),
    path('shares/', SharesStatsAPIView.as_view()),
    path('esg/', ESGScoresAPIView.as_view()),
    path('earnings/', EarningsAPIView.as_view()),
    path('financials/', FinancialsAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)