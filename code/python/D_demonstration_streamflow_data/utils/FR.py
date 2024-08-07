# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""
import geopandas as gpd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def download_data_FR(Code):
    """
    Downloads streamflow data from the French national hydrology database (eaufrance.fr) for a specified station code.
    
    Args:
    - Code (str): Station code
    
    Returns:
    - None
    """
    # URL for accessing the hydrological data for a specific station
    URL = "https://www.hydro.eaufrance.fr/stationhydro/station_name/series"
    station = Code

    # Path to the Chrome driver executable
    chrome_driver_path = 'code/python/D_demonstration_streamflow_data/chromedriver.exe'

    # Configure Chrome options
    options = Options()
    #options.add_argument('--headless')  # Run Chrome in headless mode (optional)
    #options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    #options.add_argument('--no-sandbox')  # Bypass OS security model (optional)

    # Set up the service
    service = Service(chrome_driver_path)

    # Create a WebDriver instance with the specified path
    driver = webdriver.Chrome(service=service, options=options)

    path = URL.replace("station_name", station)
    
    # Access the URL
    driver.get(path)
    
    # Handling cases where the station might be deprecated
    try:
        # Set the start and end date for the data retrieval
        driver.find_element(By.XPATH, '//*[@id="hydro_series_startAt"]').send_keys("01/09/1840")
        driver.find_element(By.XPATH, '//*[@id="hydro_series_endAt"]').send_keys("30/09/2023")
        
        # Refresh the page
        driver.find_element(By.XPATH, '//*[@id="hydro_series_endAt"]').send_keys(Keys.RETURN)
    
        # Selecting options and clicking buttons
        driver.find_element(By.XPATH, '//*[@id="hydro_series_variableType_1"]').click()
        driver.find_element(By.XPATH, '//*[@id="hydro_series_dailyVariable"]/option[3]').click()
        driver.find_element(By.XPATH, '//*[@id="hydro_series_step"]').send_keys("1")

        # Click the search button
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/div/div[1]/div[2]/div/form/div[5]/button').click()

        # Set a longer wait time to ensure all elements are loaded
        driver.implicitly_wait(10)
        
        # Perform actions to configure units, change to table format, and download data
        button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[4]/div/div[1]/div/div[1]/div/button[1]")
        driver.execute_script("arguments[0].click();", button)

        button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/a[2]")
        driver.execute_script("arguments[0].click();", button)

        button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[5]/div[1]/button")
        driver.execute_script("arguments[0].click();", button)
        
        # Wait for the download to complete
        time.sleep(2)  # Increase the sleep time if necessary
        #while not any(fname.endswith('.csv') for fname in os.listdir(download_dir)):
        #    time.sleep(1)
        
    except Exception as e:
        
        try:
            # Refresh the system to search for old stations
            driver.get("https://www.hydro.eaufrance.fr/rechercher/entites-hydrometriques")
            driver.find_element(By.XPATH, '//*[@id="shortcut-0"]').click()
            driver.find_element(By.XPATH, '//*[@id="hydro_entities_search_code"]').send_keys(station)
            driver.find_element(By.XPATH, '//*[@id="form-search"]/form/div[1]/div/div[4]/button[1]').click()
        
            # Refresh the page and try again
            driver.get(path)
        
            # Set the start and end date for the data retrieval
            driver.find_element(By.XPATH, '//*[@id="hydro_series_startAt"]').send_keys("01/01/1840")
            driver.find_element(By.XPATH, '//*[@id="hydro_series_endAt"]').send_keys("31/12/2023")
        
            # Refresh the page
            driver.find_element(By.XPATH, '//*[@id="hydro_series_endAt"]').send_keys(Keys.RETURN)
    
            # Selecting options and clicking buttons
            driver.find_element(By.XPATH, '//*[@id="hydro_series_variableType_1"]').click()
            driver.find_element(By.XPATH, '//*[@id="hydro_series_dailyVariable"]/option[3]').click()
            driver.find_element(By.XPATH, '//*[@id="hydro_series_step"]').send_keys("1")

            # Click the search button
            driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/div/div[1]/div[2]/div/form/div[5]/button').click()

            # Set a longer wait time to ensure all elements are loaded
            driver.implicitly_wait(10)
        
            # Perform actions to configure units, change to table format, and download data
            button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[4]/div/div[1]/div/div[1]/div/button[1]")
            driver.execute_script("arguments[0].click();", button)

            button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/a[2]")
            driver.execute_script("arguments[0].click();", button)

            button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[5]/div[1]/button")
            driver.execute_script("arguments[0].click();", button)     
        
        except Exception as e:
            print(f"Failed to download data for station {station} after retry. Exception: {str(e)}")
        else:
            pass

    else:
        pass
