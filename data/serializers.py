from rest_framework import serializers
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

class TickersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickers
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = General
        fields = '__all__'

class HighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = '__all__'

class ValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = '__all__'

class SharesStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharesStats
        fields = '__all__'

class ESGScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESGScores
        fields = '__all__'

class EarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earnings
        fields = '__all__'

class FinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financials
        fields = '__all__'