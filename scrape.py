#import all the necessary packages
import urllib
import html5lib
import requests
import pandas as pd

#load Selenium Webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
import time
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
driver = webdriver.Chrome('/Applications/Python 3.6/chromedriver-2') #here you need to specify the directory where you store the driver

#list the OKTMOs for all the municipalities that you are interested in. I use an example of one of them
oktmo=["01701000"]

for i in list(range(len(oktmo))):
    
    link1="http://www.gks.ru/scripts/db_inet2/passport/pass.aspx?base=munst"
    link2=oktmo[i][0:2]
    link3="&r="
    link4=oktmo[i]
    link=link1+link2+link3+link4
    driver.get(link)

    time.sleep(3)
    
    #specify the necessary years: hear I tag only the 2018, but it is going to be identical for any year
    try:
        year18=driver.find_element_by_xpath("//td/input[@value='2018']").click()
    except NoSuchElementException:
        continue

    untag=driver.find_element_by_xpath("//td/input[@onclick='all_pok_check()']").click()
    time.sleep(1)
    try:
        budget=driver.find_element_by_xpath("//*[text()='Местный бюджет']").click()
    except NoSuchElementException:  
        continue
    time.sleep(1)
    try:
        expen=driver.find_element_by_id("check_8013002").click()
    except ElementNotVisibleException:
        continue
    show=driver.find_element_by_name("Button_Table").click()
    
    time.sleep(5)
    
    html=driver.page_source
    df_list = pd.read_html(html)
    
    data=df_list[1]

    #data.columns = data.iloc[0]
    data=data.drop(data.index[0])
    data=data.drop(data.index[0])
    data=data.reset_index()
    del data['index']
    data=data.drop(data.columns[1], axis=1)
    #data.rename(columns={'0':''}, inplace=True)
    data=data.transpose()
    
    data.columns = data.iloc[0]
    data=data.drop(data.index[0])
    
    #print the scraped data
    print(data)



