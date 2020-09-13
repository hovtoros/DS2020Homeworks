!pip install dfply
!pip install scrapy
!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
from scrapy.http import TextResponse
import pandas as pd 
import numpy as np
from dfply import *

sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

CURRENCIES = ['EUR','USD','GBP','RUR']
YEARS = ['2020','2019','2018']
Currency=[]; Year=[]; Jan=[]; Feb=[]; Mar=[]; Apr=[]; May=[]; Jun=[]; Jul=[]; Aug=[]; Sep=[]; Oct=[]; Nov=[]; Dec=[]

wd = webdriver.Chrome('chromedriver', options=chrome_options)
wd.get("http://rate.am/am/armenian-dram-exchange-rates/central-bank-armenia")
wait = WebDriverWait(wd, 10)

year_id = 'ctl00_Content_dlYear'
currency_id = 'ctl00_Content_dlCurrency'

for y in YEARS:
  y_el = wait.until(EC.element_to_be_clickable((By.ID, year_id)))
  years_dd = Select(y_el)
  years_dd.select_by_value(y)
  wait.until(EC.visibility_of_element_located((By.ID, currency_id)))
  print(y)

  for c in CURRENCIES:
    c_el = wait.until(EC.element_to_be_clickable((By.ID, currency_id)))
    currencies_dd = Select(c_el)
    currencies_dd.select_by_value(c)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cb")))
    print(c)
    bd = wd.page_source
    response = TextResponse(body=bd, url=wd.current_url, encoding="utf-8")
    for row in response.xpath('//table[@class="cb"]//tbody//tr[not(@class="btm")]'):
      Currency.append(c)
      Year.append(y)
      Jan.append(row.xpath('td[2]//text()').extract_first())
      Feb.append(row.xpath('td[3]//text()').extract_first())
      Mar.append(row.xpath('td[4]//text()').extract_first())
      Apr.append(row.xpath('td[5]//text()').extract_first())
      May.append(row.xpath('td[6]//text()').extract_first())
      Jun.append(row.xpath('td[7]//text()').extract_first())
      Jul.append(row.xpath('td[8]//text()').extract_first())
      Aug.append(row.xpath('td[9]//text()').extract_first())
      Sep.append(row.xpath('td[10]//text()').extract_first())
      Oct.append(row.xpath('td[11]//text()').extract_first())
      Nov.append(row.xpath('td[12]//text()').extract_first())
      Dec.append(row.xpath('td[13]//text()').extract_first())

wd.close()

data = { 
    'Currency': Currency,
    'Year': Year,
    'Jan': Jan,
    'Feb': Feb,
    'Mar': Mar,
    'Apr': Apr,
    'May': May,
    'Jun': Jun,
    'Jul': Jul,
    'Aug': Aug,
    'Sep': Sep,
    'Oct': Oct,
    'Nov': Nov,
    'Dec': Dec, 
}
df = pd.DataFrame.from_dict(data)

df.Jan = np.where(df.Jan.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Jan.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Feb = np.where(df.Feb.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Feb.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Mar = np.where(df.Mar.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Mar.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Apr = np.where(df.Apr.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Apr.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.May = np.where(df.May.str.contains(r'\d+.*\d*'), pd.to_numeric(df.May.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Jun = np.where(df.Jun.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Jun.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Jul = np.where(df.Jul.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Jul.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Aug = np.where(df.Aug.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Aug.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Sep = np.where(df.Sep.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Sep.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Oct = np.where(df.Oct.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Oct.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Nov = np.where(df.Nov.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Nov.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.Dec = np.where(df.Dec.str.contains(r'\d+.*\d*'), pd.to_numeric(df.Dec.str.extract(r'(\d+.*\d*)')[0]), np.nan)
df.dropna(thresh=3, inplace=True)

def calc_annual_variation_for_currency(df, curr, year):
  df = df >> filter_by(X.Currency == curr, X.Year == year)
  return df.Jan.iloc[0] - df.Dec.iloc[-1]

for curr in CURRENCIES:
  for year in ['2019','2018']:
    print(f"The annual variation for {curr} in {year} is " + str(calc_annual_variation_for_currency(df, curr, year)))

def calc_month_to_month_diff(df, curr, year):
  df = (df >> 
        group_by('')
        filter_by(X.Currency == curr, X.Year == year)
  )
  return df.Jan.iloc[0] - df.Dec.iloc[-1]

"""**Problem 2**"""

!pip install quandl

import quandl
import datetime

start = datetime.datetime(2018,1,1)
end = datetime.date.today()
tsla_str = "TSLA"

tsla = quandl.get("WIKI/" + tsla_str, start_date=start, end_date=end, authtoken='wrfMqieUbGyrPDSLsSo-', transform="rdiff")

print(f"The average daily percentage change of the opening price for {tsla_str}: {tsla.Open.mean()}")

tsla['high_low_range'] = tsla.High - tsla.Low

print(f"The median daily percentage change of range between highest andlowest daily prices for {tsla_str}: {tsla.high_low_range.median()}")



"""**Problem 3**"""

!pip install dbnomics

from dbnomics import fetch_series

armenia_df = fetch_series('IMF/DOT/A.AM.TMG_CIF_USD.W00')

print(f"Armenia experienced the highest value of imports for the year {(armenia_df >> arrange(X.value, ascending=False) >> head(1)).original_period}")

armenia_georgia_df = fetch_series('IMF/DOT/A.AM.TMG_CIF_USD.GE')

# Tendency of Armenian imports from Georgia
armenia_georgia_lines = armenia_georgia_df.plot.line(x='original_period', y='value')

"""**Problem 4**"""

!pip install -U googlemaps

import googlemaps 
import time

marzkentrons = ['Yerevan, Armenia',
                'Ashtarak, Armenia',
                'Artashat, Armenia',
                'Armavir, Armenia',
                'Gavar, Armenia',
                'Hrazdan, Armenia',
                'Vanadzor, Armenia',
                'Gyumri, Armenia',
                'Kapan, Armenia',
                'Ijevan, Armenia',
                'Yeghegnadzor, Armenia']
gmaps = googlemaps.Client(key='AIzaSyC6OToUFdY3fdsgYhKhCMpD8y_hFvN0Sb4')

for kent1 in marzkentrons:
  for kent2 in marzkentrons:
    print(f"The distance between {kent1} and {kent2} is: {gmaps.distance_matrix(kent1,kent2)['rows'][0]['elements'][0]['distance']['text']}")
    time.sleep(1)

"""**Problem 5**"""

import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

class MenuAmScraper(scrapy.Spider):
    name = 'MenuAmScraper'
    #allowed_domains = ['www.menu.am']
    start_urls = ['https://www.menu.am/']

    def __init__(self):
        self.driver =  webdriver.Chrome('chromedriver', options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        self.driver.get(response.url)
        all_restaurants = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.last')))
        all_restaurants.click()

        while True:
            try:
                more = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.show_more_rests_button')))
                more.click()
            except:
                break
        
        response = TextResponse(body=self.driver.page_source, url=self.driver.current_url, encoding="utf-8")
        yield {
            'name': response.css('a.title').extract(),
            'openning_hour': response.css('span.new_list_time_block_inner').re(r'^(\d\d:\d\d)'),
            'closing_hour': response.css('span.new_list_time_block_inner').re(r'(\d\d:\d\d)$'),
            'openning_hour': response.css('span.new_list_time_block_inner').re(r'^(\d\d:\d\d)'),
            'rating': response.css('div.new_rates_block').extract(),
            'category': response.css('span.restType').extract(),
            'hyperlink': response.css('a.title::attr(href)').extract(),
        }

        self.driver.close()

process = CrawlerProcess(settings={
    "FEEDS": {
        "menu.csv": {"format": "csv"},
    },
    "USER_AGENT": 'MenuAmScraper',
    "ROBOTSTXT_OBEY": True,
    "CONCURRENT_REQUESTS": 8,
    "DOWNLOAD_DELAY": 0.5,
    "RANDOMIZE_DOWNLOAD_DELAY": True
})
process.crawl(MenuAmScraper)
process.start()

restaurants_df = pd.read_csv('menu.csv')

print(f"The category of restaurants with top rating is {(restaurants_df >> group_by('category') >> arrange(X.rating, ascending=False) >> head(1)).category}")