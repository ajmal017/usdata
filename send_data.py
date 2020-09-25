import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "usdata.settings")
application = get_wsgi_application()

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

from datetime import datetime
import requests
import pandas as pd
from dotenv import load_dotenv

today = datetime.today().strftime('%Y%m%d')
api_token = os.getenv('API_TOKEN')

exchange_list_api = f'https://eodhistoricaldata.com/api/exchanges-list/?fmt=json&api_token={api_token}'


def save_tickers():
    ticker_list_api = f'https://eodhistoricaldata.com/api/exchange-symbol-list/US?fmt=json&api_token={api_token}'

    exists = Tickers.objects.filter(date=today).exists()
    if not exists:
        res = requests.get(ticker_list_api)
        t = Tickers(date=today, tickers=res.json())
        t.save()

def save_price():
    save_tickers()
    tickers = [d['Code'] for d in Tickers.objects.filter(date=today)[0].tickers]
    ticker_cnt = len(tickers)
    
    cnt = 1
    for ticker in tickers:
        existing_dates = [d.date for d in Price.objects.filter(code=ticker).all()]
        price_api = f'https://eodhistoricaldata.com/api/eod/{ticker}.US?fmt=json&api_token={api_token}'
        res = requests.get(price_api)
        res_json = res.json()
        data_points = []
        for data in res_json:
            if data['date'].replace('-', '') not in existing_dates:
                p = Price(
                    code=ticker,
                    date=data['date'].replace('-', ''),
                    open_p=data['open'],
                    high_p=data['high'],
                    low_p=data['low'],
                    close_p=data['close'],
                    adj_close=data['adjusted_close'],
                    volume=data['volume']
                )
                data_points.append(p)
        Price.objects.bulk_create(data_points)
        print(f'({cnt}/{ticker_cnt}) {ticker} DONE')
        cnt += 1

def save_financials():
    save_tickers()
    tickers = [d['Code'] for d in Tickers.objects.filter(date=today)[0].tickers]
    ticker = tickers[0]

    fundamental_api = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US?fmt=json&api_token={api_token}'
    res = requests.get(fundamental_api)
    res_json = res.json()

    general = res_json['General']
    highlights = res_json['Highlights']
    valuation = res_json['Valuation']
    shares_stats = res_json['SharesStats']
    esg_scores = res_json['ESGScores']
    earnings = res_json['Earnings']
    financials = res_json['Financials']
    
    # General
    g = General(
        code=general['Code'],
        name=general['Name'],
        sec_type=general['Type'],
        exchange=general['Exchange'],
        currency_code=general['CurrencyCode'],
        currency_name=general['CurrencyName'],
        currency_symbol=general['CurrencySymbol'],
        country_name=general['CountryName'],
        country_iso=general['CountryISO'],
        isin=general['ISIN'],
        cusip=general['CUSIP'],
        cik=general['CIK'],
        employer_id_number=general['EmployerIdNumber'],
        fiscal_year_end=general['FiscalYearEnd'],
        ipo_date=general['IPODate'],
        international_domestic=general['InternationalDomestic'],
        sector=general['Sector'],
        industry=general['Industry'],
        gic_sector=general['GicSector'],
        gic_group=general['GicGroup'],
        gic_industry=general['GicIndustry'],
        gic_subindustry=general['GicSubIndustry'],
        home_category=general['HomeCategory'],
        is_delisted=general['IsDelisted'],
        description=general['Description'],
        address=general['Address'],
        listings=general['Listings'],
        officers=general['Officers'],
        phone=general['Phone'],
        web_url=general['WebURL'],
        logo_url=general['LogoURL'],
        fulltime_employee=general['FullTimeEmployees'],
        updated_at=general['UpdatedAt']
    )
    g.save()

    # Highlights
    h = Highlights(
        code=ticker,
        market_capitalization=highlights['MarketCapitalization'],
        market_capitalization_mln=highlights['MarketCapitalizationMln'],
        ebitda=highlights['EBITDA'],
        pe_ratio=highlights['PERatio'],
        peg_ratio=highlights['PEGRatio'],
        wallstreet_target_price=highlights['WallStreetTargetPrice'],
        book_value=highlights['BookValue'],
        dividend_share=highlights['DividendShare'],
        dividend_yield=highlights['DividendYield'],
        earnings_share=highlights['EarningsShare'],
        eps_estimate_current_year=highlights['EPSEstimateCurrentYear'],
        eps_estimate_next_year=highlights['EPSEstimateNextYear'],
        eps_estimate_next_quarter=highlights['EPSEstimateNextQuarter'],
        eps_estimate_current_quarter=highlights['EPSEstimateCurrentQuarter'],
        most_recent_quarter=highlights['MostRecentQuarter'],
        profit_margin=highlights['ProfitMargin'],
        operating_margin_ttm=highlights['OperatingMarginTTM'],
        roa_ttm=highlights['ReturnOnAssetsTTM'],
        roe_ttm=highlights['ReturnOnEquityTTM'],
        revenue_ttm=highlights['RevenueTTM'],
        revenue_per_share_ttm=highlights['RevenuePerShareTTM'],
        quarterly_revenue_growth_yoy=highlights['QuarterlyRevenueGrowthYOY'],
        gross_profit_ttm=highlights['GrossProfitTTM'],
        diluted_eps_ttm=highlights['DilutedEpsTTM'],
        quarterly_earnings_growth_yoy=highlights['QuarterlyEarningsGrowthYOY']
    )
    h.save()


    # Valuation
    v = Valuation(
        code=ticker,
        trailing_pe=valuation['TrailingPE'],
        forward_pe=valuation['ForwardPE'],
        price_sales_ttm=valuation['PriceSalesTTM'],
        price_book_mrq=valuation['PriceBookMRQ'],
        enterprise_value_revenue=valuation['EnterpriseValueRevenue'],
        enterprise_value_ebitda=valuation['EnterpriseValueEbitda']
    )
    v.save()

    # SharesStats
    s = SharesStats(
        code=ticker,
        shares_outstanding=shares_stats['SharesOutstanding'],
        shares_float=shares_stats['SharesFloat'],
        percent_insiders=shares_stats['PercentInsiders'],
        percent_institutions=shares_stats['PercentInstitutions'],
        shares_short=shares_stats['SharesShort'],
        shares_short_prior_month=shares_stats['SharesShortPriorMonth'],
        short_ratio=shares_stats['ShortRatio'],
        short_percent_outstanding=shares_stats['ShortPercentOutstanding'],
        short_percent_float=shares_stats['ShortPercentFloat']
    )
    s.save()

    # ESGScores
    esg = ESGScores(
        code=ticker,
        rating_date=esg_scores['RatingDate'],
        total_esg=esg_scores['TotalEsg'],
        total_esg_percentile=esg_scores['TotalEsgPercentile'],
        environment_score=esg_scores['EnvironmentScore'],
        environment_score_percentile=esg_scores['EnvironmentScorePercentile'],
        social_score=esg_scores['SocialScore'],
        social_score_percentile=esg_scores['SocialScorePercentile'],
        governance_score=esg_scores['GovernanceScore'],
        governance_score_percentile=esg_scores['GovernanceScorePercentile'],
        controversy_level=esg_scores['ControversyLevel'],
        activities_involvement=esg_scores['ActivitiesInvolvement']
    )
    esg.save()

    # Earnings
    e = Earnings(
        code=ticker,
        history=earnings['History'],
        trend=earnings['Trend'],
        annual=earnings['Annual']
    )
    e.save()

    # Financials
    for key in financials.keys():
        f = Financials(
            code=ticker,
            date=today,
            financial_type=key,
            currency_symbol=financials[key]['currency_symbol'],
            period='quarterly',
            data=financials[key]['quarterly']
        )
        f.save()

        f2 = Financials(
            code=ticker,
            date=today,
            financial_type=key,
            currency_symbol=financials[key]['currency_symbol'],
            period='yearly',
            data=financials[key]['yearly']
        )
        f2.save()


# save_price()
save_financials()