from django.contrib.postgres.fields import ArrayField
from django.db import models


# all tickers done on that date
class MetaDate(models.Model):
    date = models.CharField(max_length=20, blank=True, null=True)
    updated_date = models.CharField(max_length=30, blank=True, null=True)
    tickers = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    price = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    general = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    highlights = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    valuation = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    shares_stats = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    esg_scores = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    earnings = ArrayField(models.CharField(max_length=30, blank=True, null=True))
    financials = ArrayField(models.CharField(max_length=30, blank=True, null=True))


# all dates done for that ticker
class MetaData(models.Model):
    ticker = models.CharField(max_length=30, blank=True, null=True)
    price = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    general = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    highlights = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    valuation = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    shares_stats = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    esg_scores = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    earnings = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    financials = ArrayField(models.CharField(max_length=20, blank=True, null=True))


class Tickers(models.Model):
    date = models.CharField(max_length=20, blank=True, null=True)
    tickers = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.date


class Price(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    open_p = models.FloatField(blank=True, null=True)
    high_p = models.FloatField(blank=True, null=True)
    low_p = models.FloatField(blank=True, null=True)
    close_p = models.FloatField(blank=True, null=True)
    adj_close = models.FloatField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.date} {self.code}'


class BulkPrice(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.code


class General(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    sec_type = models.CharField(max_length=50, blank=True, null=True)
    exchange = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=50, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    currency_symbol = models.CharField(max_length=50, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    country_iso = models.CharField(max_length=50, blank=True, null=True)
    isin = models.CharField(max_length=50, blank=True, null=True)
    cusip = models.CharField(max_length=50, blank=True, null=True)
    cik = models.CharField(max_length=50, blank=True, null=True)
    employer_id_number = models.CharField(max_length=50, blank=True, null=True)
    fiscal_year_end = models.CharField(max_length=50, blank=True, null=True)
    ipo_date = models.CharField(max_length=50, blank=True, null=True)
    international_domestic = models.CharField(max_length=50, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    gic_sector = models.CharField(max_length=100, blank=True, null=True)
    gic_group = models.CharField(max_length=100, blank=True, null=True)
    gic_industry = models.CharField(max_length=100, blank=True, null=True)
    gic_subindustry = models.CharField(max_length=100, blank=True, null=True)
    home_category = models.CharField(max_length=50, blank=True, null=True)
    is_delisted = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    listings = models.JSONField(blank=True, null=True)
    officers = models.JSONField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    web_url = models.CharField(max_length=50, blank=True, null=True)
    logo_url = models.CharField(max_length=50, blank=True, null=True)
    fulltime_employee = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.updated_at}: [{self.code}] {self.name}'


class Highlights(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    market_capitalization = models.BigIntegerField(blank=True, null=True)
    market_capitalization_mln = models.FloatField(blank=True, null=True)
    ebitda = models.BigIntegerField(blank=True, null=True)
    pe_ratio = models.FloatField(blank=True, null=True)
    peg_ratio = models.FloatField(blank=True, null=True)
    wallstreet_target_price = models.FloatField(blank=True, null=True)
    book_value = models.FloatField(blank=True, null=True)
    dividend_share = models.FloatField(blank=True, null=True)
    dividend_yield = models.FloatField(blank=True, null=True)
    earnings_share = models.FloatField(blank=True, null=True)
    eps_estimate_current_year = models.FloatField(blank=True, null=True)
    eps_estimate_next_year = models.FloatField(blank=True, null=True)
    eps_estimate_next_quarter = models.FloatField(blank=True, null=True)
    eps_estimate_current_quarter = models.FloatField(blank=True, null=True)
    most_recent_quarter = models.CharField(max_length=50, blank=True, null=True)
    profit_margin = models.FloatField(blank=True, null=True)
    operating_margin_ttm = models.FloatField(blank=True, null=True)
    roa_ttm = models.FloatField(blank=True, null=True)
    roe_ttm = models.FloatField(blank=True, null=True)
    revenue_ttm = models.BigIntegerField(blank=True, null=True)
    revenue_per_share_ttm = models.FloatField(blank=True, null=True)
    quarterly_revenue_growth_yoy = models.FloatField(blank=True, null=True)
    gross_profit_ttm = models.BigIntegerField(blank=True, null=True)
    diluted_eps_ttm = models.FloatField(blank=True, null=True)
    quarterly_earnings_growth_yoy = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.code}'


class Valuation(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    trailing_pe = models.FloatField(blank=True, null=True)
    forward_pe = models.FloatField(blank=True, null=True)
    price_sales_ttm = models.FloatField(blank=True, null=True)
    price_book_mrq = models.FloatField(blank=True, null=True)
    enterprise_value_revenue = models.FloatField(blank=True, null=True)
    enterprise_value_ebitda = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.code}'


class SharesStats(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    shares_outstanding = models.BigIntegerField(blank=True, null=True)
    shares_float = models.BigIntegerField(blank=True, null=True)
    percent_insiders = models.FloatField(blank=True, null=True)
    percent_institutions = models.FloatField(blank=True, null=True)
    shares_short = models.BigIntegerField(blank=True, null=True)
    shares_short_prior_month = models.BigIntegerField(blank=True, null=True)
    short_ratio = models.FloatField(blank=True, null=True)
    short_percent_outstanding = models.FloatField(blank=True, null=True)
    short_percent_float = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.code}'


class Technicals(models.Model):
    pass


class SplitsDividends(models.Model):
    pass


class AnalystRatings(models.Model):
    pass


class Holders(models.Model):
    pass


class ESGScores(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    rating_date = models.CharField(max_length=50, blank=True, null=True)
    total_esg = models.FloatField(blank=True, null=True)
    total_esg_percentile = models.FloatField(blank=True, null=True)
    environment_score = models.FloatField(blank=True, null=True)
    environment_score_percentile = models.FloatField(blank=True, null=True)
    social_score = models.FloatField(blank=True, null=True)
    social_score_percentile = models.FloatField(blank=True, null=True)
    governance_score = models.FloatField(blank=True, null=True)
    governance_score_percentile = models.FloatField(blank=True, null=True)
    controversy_level = models.IntegerField(blank=True, null=True)
    activities_involvement = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.code}'


class OutstandingShares(models.Model):
    pass


class Earnings(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    history = models.JSONField(blank=True, null=True)
    trend = models.JSONField(blank=True, null=True)
    annual = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.code}'


class Financials(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    financial_type = models.CharField(max_length=50, blank=True, null=True)
    currency_symbol = models.CharField(max_length=20, blank=True, null=True)
    period = models.CharField(max_length=20, blank=True, null=True) # yearly, quarterly
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.data} - {self.code}'