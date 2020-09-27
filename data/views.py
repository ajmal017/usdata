from django.shortcuts import render

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

from data.serializers import (
    TickersSerializer,
    PriceSerializer,
    GeneralSerializer,
    HighlightsSerializer,
    ValuationSerializer,
    SharesStatsSerializer,
    ESGScoresSerializer,
    EarningsSerializer,
    FinancialsSerializer
)

from rest_framework import pagination
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter


class StandardResultPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    # max_page_size = 1000


class TickersAPIView(generics.ListAPIView):
    queryset = Tickers.objects.all()
    serializer_class = TickersSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Tickers.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        if date_by:
            queryset = queryset.filter(date=date_by)
        return queryset


class PriceAPIView(generics.ListAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Price.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        date_by = self.request.GET.get('date')
        if code_by:
            queryset = queryset.filter(code=code_by)
        if date_by:
            queryset = queryset.filter(date=date_by)
        return queryset


class GeneralAPIView(generics.ListAPIView):
    queryset = General.objects.all()
    serializer_class = GeneralSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = General.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class HighlightsAPIView(generics.ListAPIView):
    queryset = Highlights.objects.all()
    serializer_class = HighlightsSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Highlights.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class ValuationAPIView(generics.ListAPIView):
    queryset = Valuation.objects.all()
    serializer_class = ValuationSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Valuation.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class SharesStatsAPIView(generics.ListAPIView):
    queryset = SharesStats.objects.all()
    serializer_class = SharesStatsSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = SharesStats.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class ESGScoresAPIView(generics.ListAPIView):
    queryset = ESGScores.objects.all()
    serializer_class = ESGScoresSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = ESGScores.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class EarningsAPIView(generics.ListAPIView):
    queryset = Earnings.objects.all()
    serializer_class = EarningsSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Earnings.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class FinancialsAPIView(generics.ListAPIView):
    queryset = Financials.objects.all()
    serializer_class = FinancialsSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Financials.objects.all().order_by('id')
        code_by = self.request.GET.get('code')
        date_by = self.request.GET.get('date')
        financial_type_by = self.request.GET.get('financial_type')
        period_by = self.request.GET.get('period')
        if code_by:
            queryset = queryset.filter(code=code_by)
        if date_by:
            queryset = queryset.filter(date=date_by)
        if financial_type_by:
            queryset = queryset.filter(financial_type=financial_type_by)
        if period_by:
            queryset = queryset.filter(period=period_by)
        return queryset