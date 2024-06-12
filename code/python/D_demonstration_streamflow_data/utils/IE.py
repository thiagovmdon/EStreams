# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""
import geopandas as gpd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def download_data_IEEPA(code):  

    URL_station_i = "https://epawebapp.epa.ie/hydronet/#STATION"
    path_information_i = "/html/body/div/div/div/div[3]/div/div/div[2]/table/tbody/tr[ROWTOBEREPLACED]"
    path_download_i = "/html/body/div[1]/div/div/div[3]/div/div/div[3]/div/div/div/div[2]/table/tr[ROWTOBEREPLACED]/td[2]/a"
  
    # Path to the Chrome driver executable
    chrome_driver_path = 'code\python\E_complementary_streamflow_data\chromedriver.exe'

    # Create a WebDriver instance with the specified path
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    
    # Now we can select the station:
    URL_station = URL_station_i.replace("STATION", str(code))

    driver.get(URL_station)
    driver.implicitly_wait(3)
    
    try:
        # Here we can retrieve the full information in the format of a table:
        tbl3 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/table').get_attribute('outerHTML')
                                             
    except:
        tbl3 = driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div[2]/table').get_attribute('outerHTML')
                                             
    
    # Here we get the table to check the position of the "download" tab:
    df3  = pd.read_html(tbl3)
    info_row = df3[0]
    info_row.set_index(1, inplace = True)
    
    try:
        # Here we can get the row:
        row_number = info_row.index.get_loc('Download')

    
        path_information = path_information_i.replace("ROWTOBEREPLACED", str(row_number + 1))
    
        # Now we can switch to Download:
        button = driver.find_element_by_xpath(path_information)
        driver.execute_script("arguments[0].click();", button)
    
        driver.implicitly_wait(1)
    
        # Here we can click to download our dataset:
        # The solution since the products to download vary from station to station is to retreive the table, and select directly the row:

        # Here we can retrieve the full information in the format of a table:
        tbl2 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[3]/div/div/div/div[2]/table').get_attribute('outerHTML')
        df2  = pd.read_html(tbl2)
        info_download = df2[0]
        info_download.set_index(0, inplace = True)
    
        try:
            # Here we can get the row:
            row_number = info_download.index.get_loc('All data DayMean TS')
    
            # Here we substitute it:
            path_download = path_download_i.replace("ROWTOBEREPLACED", str(row_number + 1))
    
            # Finally we can download it:
            driver.find_element_by_xpath(path_download).click()
            
            print(f"Successfully downloaded data for station {code}")
        except:
            print(f"Failed to download data for station {code}")
    except: 
        print(f"Failed to download data for station {code}")
    
    
