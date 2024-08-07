# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""
import os
import time
import geopandas as gpd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def download_data_IEEPA(code):  
    URL_station_i = "https://epawebapp.epa.ie/hydronet/#STATION"
    path_information_i = "/html/body/div/div/div/div[3]/div/div/div[2]/table/tbody/tr[ROWTOBEREPLACED]"
    path_download_i = "/html/body/div/div/div/div[3]/div/div/div[3]/div/div/div/div[2]/table/tr[ROWTOBEREPLACED]/td[2]/a"
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    chrome_options = Options()
    prefs = {"download.default_directory": download_dir, "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs", prefs)

    # Path to the Chrome driver executable
    chrome_driver_path = 'code/python/D_demonstration_streamflow_data/chromedriver.exe'

    # Create a WebDriver instance with the specified path
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Now we can select the station:
    URL_station = URL_station_i.replace("STATION", str(code))

    driver.get(URL_station)
    driver.implicitly_wait(10)
    
    try:
        # Here we can retrieve the full information in the format of a table:
        tbl3 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div[2]/table').get_attribute('outerHTML')
    except Exception as e:
        print(f"Failed to retrieve the table with the first XPath: {e}")
        try:
            tbl3 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div[2]/table').get_attribute('outerHTML')
        except Exception as e:
            print(f"Failed to retrieve the table with the second XPath: {e}")
            driver.quit()
            return
        
    # Here we get the table to check the position of the "download" tab:
    df3  = pd.read_html(tbl3)
    info_row = df3[0]
    info_row.set_index(1, inplace=True)
    
    try:
        # Here we can get the row:
        row_number = info_row.index.get_loc('Download')
        path_information = path_information_i.replace("ROWTOBEREPLACED", str(row_number + 1))
        
        # Now we can switch to Download:
        button = driver.find_element(By.XPATH, path_information)
        driver.execute_script("arguments[0].click();", button)
    
        driver.implicitly_wait(10)
    
        # Here we can click to download our dataset:
        # The solution since the products to download vary from station to station is to retrieve the table, and select directly the row:
        tbl2 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div[3]/div/div/div/div[2]/table').get_attribute('outerHTML')
        df2  = pd.read_html(tbl2)
        info_download = df2[0]
        info_download.set_index(0, inplace=True)
    
        try:
            # Here we can get the row:
            row_number = info_download.index.get_loc('All data DayMean TS')
            path_download = path_download_i.replace("ROWTOBEREPLACED", str(row_number + 1))
    
            # Finally we can download it:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path_download))).click()
                        
            # Wait for download to complete
            time.sleep(5)
            print(f"Successfully downloaded data for station {code}")
    
        except Exception as e:
            print(f"Failed to find and click the download link: {e}")
    except Exception as e:
        print(f"Failed to find the download row: {e}")
    
    driver.quit()
    

    
