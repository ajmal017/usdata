import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "usdata.settings")
application = get_wsgi_application()

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

import sys
from datetime import datetime
import time
import redis
import requests
import pandas as pd
from dotenv import load_dotenv
from slacker import Slacker
from sensitives import SLACK_TOKEN

# Redis related functions
def cache_conn():
    redis_client = redis.Redis(host=cache_host, port=6379, password=cache_pw)
    return redis_client

def set_list(redis_client, data):
    response = redis_client.rpush(data[0], *data[1:])
    return response # returns 1 or 0

def get_list(redis_client, key, type='str'):
    response = redis_client.lrange(key, 0, -1)
    temp = response
    if type == 'int':
        try:
            is_int = int(response[0])
            response = list(map(lambda x: int(x), response))
        except ValueError:
            response = temp
    elif type == 'str':
        response = list(map(lambda x: x.decode('utf-8'), response))
    return response

def add_to_list(redis_client, key, data):
    response = redis_client.rpush(key, data)
    return response # returns 1 or 0

skip_num = int(sys.argv[1]) if len(sys.argv) >= 2 else 1

today = datetime.today().strftime('%Y-%m-%d')

cache_host = os.getenv('CACHE_HOST')
cache_pw = os.getenv('CACHE_PW')
api_token = os.getenv('API_TOKEN')

slack = Slacker(SLACK_TOKEN)
redis_client = cache_conn()


# Slack related functions
def send_slack(task, msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        slack.chat.post_message('#general', f'({now}) [{task.upper()}]: {msg}')
    except:
        print(f'({now}) [{task.upper()}]: {msg}')


# Tasks
def save_tickers():
    ticker_list_api = f'https://eodhistoricaldata.com/api/exchange-symbol-list/US?fmt=json&api_token={api_token}'

    if not Tickers.objects.filter(date=today.replace('-', '')).exists():
        res = requests.get(ticker_list_api)
        t = Tickers(date=today.replace('-', ''), tickers=res.json())
        t.save()
        send_slack('tickers', f'Saved {today} tickers.')
    else:
        send_slack('tickers', f'{today} tickers already exist.')


def sync_db_and_meta():
    print('Syncing DB and cache Meta information')
    db_tickers = list(Price.objects.values_list('code', flat=True).distinct())
    ticker_cnt = len(db_tickers)
    print(f'DB total tickers count: {ticker_cnt}')
    
    cnt = 1
    for ticker in db_tickers:
        start = time.time()
        price_dates = list(Price.objects.filter(code=ticker).values_list('date', flat=True))
        key_name = f'{ticker}_PRICE_DONE'
        redis_client.delete(key_name)
        set_list(redis_client, [key_name] + price_dates)
        end = time.time()
        print(f'[SYNC DB] ({cnt} / {ticker_cnt}) {ticker} synced : took {end - start}s')
        cnt += 1

    
def save_bulk_data():
    save_tickers()

    tickers = [d['Code'] for d in Tickers.objects.filter(date=today.replace('-', '')).first().tickers]
    ticker_cnt = len(tickers)
    send_slack('data', f'starting {today} price data save. Total tickers count: {ticker_cnt}')

    cnt = 1
    for ticker in tickers:
        if cnt > skip_num:
            # price
            if not BulkPrice.objects.filter(code=ticker).exists():
                price_api = f'https://eodhistoricaldata.com/api/eod/{ticker}.US?fmt=json&api_token={api_token}'
                res = requests.get(price_api)
                res_json = res.json()
                p = BulkPrice(code=ticker, data=res_json)
                p.save()
            else:
                bulk_price = BulkPrice.objects.filter(code=ticker).first()
                if (bulk_price.data[-1]['date'] != today):
                    price_api = f'https://eodhistoricaldata.com/api/eod/{ticker}.US?fmt=json&api_token={api_token}'
                    res = requests.get(price_api)
                    res_json = res.json()
                    BulkPrice.objects.filter(code=ticker).update(data=res_json)
            # financials
            save_financials(ticker)
        if cnt % 250 == 0:
            send_slack('data', f'({cnt}/{ticker_cnt}) DATA DONE')
        print(f'({cnt}/{ticker_cnt}) {ticker} DATA DONE')
        cnt += 1


def save_financials(ticker):
    fundamental_api = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US?fmt=json&api_token={api_token}'
    res = requests.get(fundamental_api)
    res_json = res.json()

    try:
        general = res_json['General']
    except:
        general = None
    
    try:
        highlights = res_json['Highlights']
    except:
        highlights = None

    try:
        valuation = res_json['Valuation']
    except:
        valuation = None

    try:
        shares_stats = res_json['SharesStats']
    except:
        shares_stats = None

    try:
        esg_scores = res_json['ESGScores']
    except:
        esg_scores = None

    try:
        earnings = res_json['Earnings']
    except:
        earnings = None

    try:
        financials = res_json['Financials']
    except:
        financials = None
    
    # General
    if general != None:
        if not General.objects.filter(code=ticker).exists():
            g = General(
                code=general.get('Code'),
                name=general.get('Name'),
                sec_type=general.get('Type'),
                exchange=general.get('Exchange'),
                currency_code=general.get('CurrencyCode'),
                currency_name=general.get('CurrencyName'),
                currency_symbol=general.get('CurrencySymbol'),
                country_name=general.get('CountryName'),
                country_iso=general.get('CountryISO'),
                isin=general.get('ISIN'),
                cusip=general.get('CUSIP'),
                cik=general.get('CIK'),
                employer_id_number=general.get('EmployerIdNumber'),
                fiscal_year_end=general.get('FiscalYearEnd'),
                ipo_date=general.get('IPODate'),
                international_domestic=general.get('InternationalDomestic'),
                sector=general.get('Sector'),
                industry=general.get('Industry'),
                gic_sector=general.get('GicSector'),
                gic_group=general.get('GicGroup'),
                gic_industry=general.get('GicIndustry'),
                gic_subindustry=general.get('GicSubIndustry'),
                home_category=general.get('HomeCategory'),
                is_delisted=general.get('IsDelisted'),
                description=general.get('Description'),
                address=general.get('Address'),
                listings=general.get('Listings'),
                officers=general.get('Officers'),
                phone=general.get('Phone'),
                web_url=general.get('WebURL'),
                logo_url=general.get('LogoURL'),
                fulltime_employee=general.get('FullTimeEmployees'),
                updated_at=general.get('UpdatedAt')
            )
            g.save()
        else:
            General.objects.filter(code=ticker).update(
                code=general.get('Code'),
                name=general.get('Name'),
                sec_type=general.get('Type'),
                exchange=general.get('Exchange'),
                currency_code=general.get('CurrencyCode'),
                currency_name=general.get('CurrencyName'),
                currency_symbol=general.get('CurrencySymbol'),
                country_name=general.get('CountryName'),
                country_iso=general.get('CountryISO'),
                isin=general.get('ISIN'),
                cusip=general.get('CUSIP'),
                cik=general.get('CIK'),
                employer_id_number=general.get('EmployerIdNumber'),
                fiscal_year_end=general.get('FiscalYearEnd'),
                ipo_date=general.get('IPODate'),
                international_domestic=general.get('InternationalDomestic'),
                sector=general.get('Sector'),
                industry=general.get('Industry'),
                gic_sector=general.get('GicSector'),
                gic_group=general.get('GicGroup'),
                gic_industry=general.get('GicIndustry'),
                gic_subindustry=general.get('GicSubIndustry'),
                home_category=general.get('HomeCategory'),
                is_delisted=general.get('IsDelisted'),
                description=general.get('Description'),
                address=general.get('Address'),
                listings=general.get('Listings'),
                officers=general.get('Officers'),
                phone=general.get('Phone'),
                web_url=general.get('WebURL'),
                logo_url=general.get('LogoURL'),
                fulltime_employee=general.get('FullTimeEmployees'),
                updated_at=general.get('UpdatedAt')
            )

    # Highlights
    if highlights != None:
        if not Highlights.objects.filter(code=ticker).exists():
            h = Highlights(
                code=ticker,
                market_capitalization=highlights.get('MarketCapitalization'),
                market_capitalization_mln=highlights.get('MarketCapitalizationMln'),
                ebitda=highlights.get('EBITDA'),
                pe_ratio=highlights.get('PERatio'),
                peg_ratio=highlights.get('PEGRatio'),
                wallstreet_target_price=highlights.get('WallStreetTargetPrice'),
                book_value=highlights.get('BookValue'),
                dividend_share=highlights.get('DividendShare'),
                dividend_yield=highlights.get('DividendYield'),
                earnings_share=highlights.get('EarningsShare'),
                eps_estimate_current_year=highlights.get('EPSEstimateCurrentYear'),
                eps_estimate_next_year=highlights.get('EPSEstimateNextYear'),
                eps_estimate_next_quarter=highlights.get('EPSEstimateNextQuarter'),
                eps_estimate_current_quarter=highlights.get('EPSEstimateCurrentQuarter'),
                most_recent_quarter=highlights.get('MostRecentQuarter'),
                profit_margin=highlights.get('ProfitMargin'),
                operating_margin_ttm=highlights.get('OperatingMarginTTM'),
                roa_ttm=highlights.get('ReturnOnAssetsTTM'),
                roe_ttm=highlights.get('ReturnOnEquityTTM'),
                revenue_ttm=highlights.get('RevenueTTM'),
                revenue_per_share_ttm=highlights.get('RevenuePerShareTTM'),
                quarterly_revenue_growth_yoy=highlights.get('QuarterlyRevenueGrowthYOY'),
                gross_profit_ttm=highlights.get('GrossProfitTTM'),
                diluted_eps_ttm=highlights.get('DilutedEpsTTM'),
                quarterly_earnings_growth_yoy=highlights.get('QuarterlyEarningsGrowthYOY')
            )
            h.save()
        else:
            Highlights.objects.filter(code=ticker).update(
                code=ticker,
                market_capitalization=highlights.get('MarketCapitalization'),
                market_capitalization_mln=highlights.get('MarketCapitalizationMln'),
                ebitda=highlights.get('EBITDA'),
                pe_ratio=highlights.get('PERatio'),
                peg_ratio=highlights.get('PEGRatio'),
                wallstreet_target_price=highlights.get('WallStreetTargetPrice'),
                book_value=highlights.get('BookValue'),
                dividend_share=highlights.get('DividendShare'),
                dividend_yield=highlights.get('DividendYield'),
                earnings_share=highlights.get('EarningsShare'),
                eps_estimate_current_year=highlights.get('EPSEstimateCurrentYear'),
                eps_estimate_next_year=highlights.get('EPSEstimateNextYear'),
                eps_estimate_next_quarter=highlights.get('EPSEstimateNextQuarter'),
                eps_estimate_current_quarter=highlights.get('EPSEstimateCurrentQuarter'),
                most_recent_quarter=highlights.get('MostRecentQuarter'),
                profit_margin=highlights.get('ProfitMargin'),
                operating_margin_ttm=highlights.get('OperatingMarginTTM'),
                roa_ttm=highlights.get('ReturnOnAssetsTTM'),
                roe_ttm=highlights.get('ReturnOnEquityTTM'),
                revenue_ttm=highlights.get('RevenueTTM'),
                revenue_per_share_ttm=highlights.get('RevenuePerShareTTM'),
                quarterly_revenue_growth_yoy=highlights.get('QuarterlyRevenueGrowthYOY'),
                gross_profit_ttm=highlights.get('GrossProfitTTM'),
                diluted_eps_ttm=highlights.get('DilutedEpsTTM'),
                quarterly_earnings_growth_yoy=highlights.get('QuarterlyEarningsGrowthYOY')
            )


    # Valuation
    if valuation != None:
        if not Valuation.objects.filter(code=ticker).exists():
            v = Valuation(
                code=ticker,
                trailing_pe=valuation.get('TrailingPE'),
                forward_pe=valuation.get('ForwardPE'),
                price_sales_ttm=valuation.get('PriceSalesTTM'),
                price_book_mrq=valuation.get('PriceBookMRQ'),
                enterprise_value_revenue=valuation.get('EnterpriseValueRevenue'),
                enterprise_value_ebitda=valuation.get('EnterpriseValueEbitda')
            )
            v.save()
        else:
            Valuation.objects.filter(code=ticker).update(
                code=ticker,
                trailing_pe=valuation.get('TrailingPE'),
                forward_pe=valuation.get('ForwardPE'),
                price_sales_ttm=valuation.get('PriceSalesTTM'),
                price_book_mrq=valuation.get('PriceBookMRQ'),
                enterprise_value_revenue=valuation.get('EnterpriseValueRevenue'),
                enterprise_value_ebitda=valuation.get('EnterpriseValueEbitda')
            )

    # SharesStats
    if shares_stats != None:
        if not SharesStats.objects.filter(code=ticker).exists():
            s = SharesStats(
                code=ticker,
                shares_outstanding=shares_stats.get('SharesOutstanding'),
                shares_float=shares_stats.get('SharesFloat'),
                percent_insiders=shares_stats.get('PercentInsiders'),
                percent_institutions=shares_stats.get('PercentInstitutions'),
                shares_short=shares_stats.get('SharesShort'),
                shares_short_prior_month=shares_stats.get('SharesShortPriorMonth'),
                short_ratio=shares_stats.get('ShortRatio'),
                short_percent_outstanding=shares_stats.get('ShortPercentOutstanding'),
                short_percent_float=shares_stats.get('ShortPercentFloat')
            )
            s.save()
        else:
            SharesStats.objects.filter(code=ticker).update(
                code=ticker,
                shares_outstanding=shares_stats.get('SharesOutstanding'),
                shares_float=shares_stats.get('SharesFloat'),
                percent_insiders=shares_stats.get('PercentInsiders'),
                percent_institutions=shares_stats.get('PercentInstitutions'),
                shares_short=shares_stats.get('SharesShort'),
                shares_short_prior_month=shares_stats.get('SharesShortPriorMonth'),
                short_ratio=shares_stats.get('ShortRatio'),
                short_percent_outstanding=shares_stats.get('ShortPercentOutstanding'),
                short_percent_float=shares_stats.get('ShortPercentFloat')
            )

    # ESGScores
    if esg_scores != None:
        if not ESGScores.objects.filter(code=ticker).exists():
            esg = ESGScores(
                code=ticker,
                rating_date=esg_scores.get('RatingDate'),
                total_esg=esg_scores.get('TotalEsg'),
                total_esg_percentile=esg_scores.get('TotalEsgPercentile'),
                environment_score=esg_scores.get('EnvironmentScore'),
                environment_score_percentile=esg_scores.get('EnvironmentScorePercentile'),
                social_score=esg_scores.get('SocialScore'),
                social_score_percentile=esg_scores.get('SocialScorePercentile'),
                governance_score=esg_scores.get('GovernanceScore'),
                governance_score_percentile=esg_scores.get('GovernanceScorePercentile'),
                controversy_level=esg_scores.get('ControversyLevel'),
                activities_involvement=esg_scores.get('ActivitiesInvolvement')
            )
            esg.save()
        else:
            ESGScores.objects.filter(code=ticker).update(
                code=ticker,
                rating_date=esg_scores.get('RatingDate'),
                total_esg=esg_scores.get('TotalEsg'),
                total_esg_percentile=esg_scores.get('TotalEsgPercentile'),
                environment_score=esg_scores.get('EnvironmentScore'),
                environment_score_percentile=esg_scores.get('EnvironmentScorePercentile'),
                social_score=esg_scores.get('SocialScore'),
                social_score_percentile=esg_scores.get('SocialScorePercentile'),
                governance_score=esg_scores.get('GovernanceScore'),
                governance_score_percentile=esg_scores.get('GovernanceScorePercentile'),
                controversy_level=esg_scores.get('ControversyLevel'),
                activities_involvement=esg_scores.get('ActivitiesInvolvement')
            )

    # Earnings
    if earnings != None:
        if not Earnings.objects.filter(code=ticker).exists():
            e = Earnings(
                code=ticker,
                history=earnings.get('History'),
                trend=earnings.get('Trend'),
                annual=earnings.get('Annual')
            )
            e.save()
        else:
            Earnings.objects.filter(code=ticker).update(
                code=ticker,
                history=earnings.get('History'),
                trend=earnings.get('Trend'),
                annual=earnings.get('Annual')
            )

    # Financials
    if financials != None:
        if not BulkFinancials.objects.filter(code=ticker).exists():
            bf = BulkFinancials(
                code=ticker,
                data=financials
            )
            bf.save()
        else:
            BulkFinancials.objects.filter(code=ticker).update(
                code=ticker,
                data=financials
            )

    # Financials
    # for key in financials.keys():
    #     f = Financials(
    #         code=ticker,
    #         date=today,
    #         financial_type=key,
    #         currency_symbol=financials[key]['currency_symbol'],
    #         period='quarterly',
    #         data=financials[key]['quarterly']
    #     )
    #     f.save()

    #     f2 = Financials(
    #         code=ticker,
    #         date=today,
    #         financial_type=key,
    #         currency_symbol=financials[key]['currency_symbol'],
    #         period='yearly',
    #         data=financials[key]['yearly']
    #     )
    #     f2.save()


if __name__ == "__main__":
    save_bulk_data()

