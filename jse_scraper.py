from configparser import SafeConfigParser
from bs4 import BeautifulSoup as Soup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
import os
chrome_options = Options()
chrome_options.add_argument("--headless")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('scraper.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



class jse_scraper(object):

    

#    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
#    chrome_options.add_argument("--headless")
#    chrome_options.add_argument("--disable-dev-shm-usage")
#    chrome_options.add_argument("--no-sandbox")
#    driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

   driver = webdriver.Chrome('driver\chromedriver.exe')
   base_url = "https://www.jamstockex.com/market-data/"
   instruments_url = "instruments/?symbol="
   listed_companies_url = "listed-companies/"
   junior_market = "/junior-market"
   main_market = "/main-market"
   listed_table_xpath ="//*[@id='content']/div[2]/div/div/div/div/table[1]"
   '''/// baseurl for the stock ohlc data'''
   ohlc_url = "https://www.jamstockex.com/market-data/instruments/?symbol="

   def __init__(self,instrument):
       self.instrument = instrument
       

   def get_stockInstrument_page(self):
       self.base_url = self.base_url+'{}{}'.format(self.instruments_url,self.instrument)
       try:
           self.driver.get(self.base_url)
       except:
           logger.error(f'Could not load the baseUrl : {self.base_url}')
       else:
           time.sleep(5)
           stock_daily = self.driver.execute_script('return window.Highcharts.charts[2]'

          #temp3 = driver.execute_script('return window.Highcharts.charts[2]'
 #                               '.series[2].options.data')
                                '.series[0].options.data')
           temp2 = self.driver.execute_script('return window.Highcharts.charts[2]'
                                '.series[1].options.data')

       data1 = [item2 for item2 in temp2]
       volume_dic = {}
       for i, x in enumerate(data1,1):
           volume_dic[str(x[0])]={}
           volume_dic[str(x[0])] = x[1]
           vol_json_data = json.dumps(volume_dic)
           vol_json_data1 = json.loads(vol_json_data)

       data = [item for item in stock_daily]
       #test = self.instrument
       #test = {}
       new_dict = {}
       new_dict["Instrument"] = self.instrument
       new_dict["Data"]= []
       for i, x in enumerate(data,1):
           temp={
                   "Date":x[0],
                   "Open":x[1],
                   "High":x[2],
                   "Low":x[3],
                   "Close":x[4],
                   "Volume":vol_json_data1[str(x[0])]
               }
               
           new_dict["Data"].append(temp)

           json_data = json.dumps(new_dict)
           json_data1 = json.loads(json_data)

       return json_data1


   def get_Junior_listedCompany_page(self):
        logger.info(f'fetching the list of junior stocks from the JSE')
       # try:
        self.driver.get(self.base_url+'{}{}'.format(self.listed_companies_url,self.junior_market))
        #self.driver.get(self.base_url+'{}{}'.format(self.listed_companies_url,self.junior_market))
       # except:
        #    logger.error(f'Cound not load the Junior Market Index page of the JSE')
        #else:
         #   time.sleep(5)
        # table = self.browser.find_element_by_xpath(self.listed_table_xpath)

        html = self.driver.page_source

        #self.driver.find_element(By.i,'table table-striped table-hover');
        page_soup = Soup(html,"html.parser")
        table_body = page_soup.find("tbody")
        rows = table_body.findAll('tr')
        jsonAray = []
        #current = None
        for row in rows:
            if row.findAll('th'):
                header = row.findAll("th")
                jsonObj = {
                    'Name' : header[0].text.strip(),
                    'Instrument_code': header[1].text.strip(),
                    'Currency' : header[2].text.strip(),
                    'Sector': header[3].text.strip(),
                    'Type' : header[4].text.strip()
                }
                logger.info(f'{jsonObj}')
            else:
                cols = row.find_all('td')
                jsonObj = {
                    'Name' : cols[0].text.strip(),
                    'Instrument_Code' : cols[1].text.strip(),
                    'Currency' : cols[2].text.strip(),
                    'Sector' : cols[3].text.strip(),
                    'Type' : cols[4].text.strip()
                }
                logger.info(f'The following Junior Indext was added the list {jsonObj}')
                jsonAray.append(jsonObj)
                #abstract_text = json.dumps(abstract_list,separators=(',',':'))
                #print(jsonAray) 
        return jsonAray

   def get_Main_listedCompany_page(self):
        logger.info(f'fetching the list of junior stocks from the JSE')
        #try:
        self.driver.get(self.base_url+'{}{}'.format(self.listed_companies_url,self.main_market))
        #except:
        logger.error(f'Cound not load the Junior Market Index page of the JSE')
        #else:
        #    time.sleep(5)

        html = self.driver.page_source

        #self.driver.find_element(By.i,'table table-striped table-hover');
        page_soup = Soup(html,"html.parser")
        table_body = page_soup.find("tbody")
        rows = table_body.findAll('tr')
        jsonAray = []
        #current = None
        for row in rows:
            if row.findAll('th'):
                header = row.findAll("th")
                jsonObj = {
                    'Name' : header[0].text.strip(),
                    'Instrument_code': header[1].text.strip(),
                    'Currency' : header[2].text.strip(),
                    'Sector': header[3].text.strip(),
                    'Type' : header[4].text.strip()
                }
                print(jsonObj)
            else:
                cols = row.find_all('td')
                jsonObj = {
                    'Name' : cols[0].text.strip(),
                    'Instrument_Code' : cols[1].text.strip(),
                    'Currency' : cols[2].text.strip(),
                    'Sector' : cols[3].text.strip(),
                    'Type' : cols[4].text.strip()
                }
                jsonAray.append(jsonObj)
                #abstract_text = json.dumps(abstract_list,separators=(',',':'))
                #print(jsonAray) 
        return jsonAray


   def get_stock_page(self,stock_ticker):
        self.base_url = self.base_url+'{}'.format(stock_ticker)
        try:
            self.driver.get(self.base_url)
        except:
            logger.error(f'Could not load the Stock Page: {self.base_url}')
        else:
            time.sleep(10)
            stock_daily = self.driver.execute_script('return window.Highcharts.charts[2]'

        #temp3 = driver.execute_script('return window.Highcharts.charts[2]'
 #                               '.series[2].options.data')
                                '.series[0].options.data')
        temp2 = self.driver.execute_script('return window.Highcharts.charts[2]'
                                '.series[1].options.data')
        data1 = [item2 for item2 in temp2]
        volume_dic = {}
        for i, x in enumerate(data1,1):
            volume_dic[str(x[0])]={}
            volume_dic[str(x[0])] = x[1]
            vol_json_data = json.dumps(volume_dic)
            vol_json_data1 = json.loads(vol_json_data)

        data = [item for item in stock_daily]
        new_dict = {}
        for i, x in enumerate(data,1):
            new_dict[str(x[0])]={}
            new_dict[str(x[0])]['Date'] = x[0]
            new_dict[str(x[0])]['Open'] = x[1]
            new_dict[str(x[0])]['High'] = x[2]
            new_dict[str(x[0])]['Low'] = x[3]
            new_dict[str(x[0])]['Close'] = x[4]
            new_dict[str(x[0])]['Volume'] = vol_json_data1[str(x[0])]

            json_data = json.dumps(new_dict)
            json_data1 = json.loads(json_data)

        return json_data1 