# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""
import geopandas as gpd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from selenium.webdriver.common.by import By
import re
import numpy as np
import tqdm
import time
import warnings
warnings.simplefilter(action='ignore', category=Warning)
from selenium.webdriver.common.action_chains import ActionChains

def extract_first_table_to_dataframe(tables_in_new_panel):
    """
    Extracts the first table from a list of tables in a new panel and returns it as a Pandas DataFrame.

    Args:
    - tables_in_new_panel (list): List of Selenium WebElement tables.

    Returns:
    - pandas DataFrame or None: DataFrame containing the data from the first table, or None if no tables are available.
    """
    # Check if there are tables available
    if not tables_in_new_panel:
        return None
    
    # Select the first table (table 0)
    table = tables_in_new_panel[0]

    # Initialize lists for column headers and values
    column_headers = []
    values = []

    # Iterate through rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        # Get the cells from the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        # If no cells found, look for header cells (`<th>`)
        if not cells:
            cells = row.find_elements(By.TAG_NAME, 'th')

        # Ensure there are at least two cells (columns) in the row
        if len(cells) >= 2:
            # Extract and clean the text content of each cell
            column_name = cells[0].text.strip()  # First cell is the column name
            value = cells[1].text.strip()  # Second cell is the value
            
            # Append the column name and value to respective lists
            column_headers.append(column_name)
            values.append(value)

    # Create a Pandas DataFrame using the column headers and values
    df = pd.DataFrame([values], columns=column_headers)

    # Return the DataFrame
    return df
    
    
def extract_protok_data_range(text):
    """
    Extracts the data range from the provided text.

    Args:
    - text (str): Text containing the "PROTOK Ekstremi" section.

    Returns:
    - str or np.nan: Data range extracted from the text or np.nan if no data range is found.
    """
    # Step 1: Locate the "PROTOK Ekstremi" section
    pattern_protok_section = r'PROTOK Ekstremi\n(.*?)\n(?=(?:VODOMJERENJA|PROFILI|$))'
    match_protok_section = re.search(pattern_protok_section, text, re.DOTALL)

    # If the "PROTOK Ekstremi" section is found
    if match_protok_section:
        protok_section = match_protok_section.group(1)  # Extract the section content

        # Step 2: Search for "Godine mjerenja:" and extract the following data
        pattern_data_range = r'Godine mjerenja:\n([\d-]+(?:\n[\d-]+)*)'
        match_data_range = re.search(pattern_data_range, protok_section)

        # If the data range is found, return it
        if match_data_range:
            return match_data_range.group(1)
        else:
            # Return np.nan if no data range is found
            return np.nan
    else:
        # Return np.nan if the "PROTOK Ekstremi" section is not found
        return np.nan


def get_metadata_HR(num_stations):
    """
    Retrieves station information from https://hidro.dhz.hr.

    Args:
    - num_stations (int): Number of stations to retrieve information for.

    Returns:
    - pandas DataFrame: Station information including names, codes, and years of streamflow data.
    """
    
    # Initialize a dictionary to hold data from each table
    tables_dict_1 = {}
    tables_dict_2 = {}

    # Retrieve the name and code for all stations (help to manually extract the years)
    URL = "https://hidro.dhz.hr"
    
    # Path to the Chrome driver executable
    chrome_driver_path = 'code\python\E_complementary_streamflow_data\chromedriver.exe'

    # Create a WebDriver instance with the specified path
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    path = URL
    # First we get the URL:
    driver.get(path)

    driver.implicitly_wait(10)

    # Here we click to switch to the data information:
    driver.find_element_by_xpath('//*[@id="ext-gen139"]/em/span/span/span').click()

    # Here we click on the historic data part:
    button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[3]/a[2]/em/span/span")
    driver.execute_script("arguments[0].click();", button)

    # Here we accept the terms:
    button = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button")
    driver.execute_script("arguments[0].click();", button)

    for station in tqdm.tqdm(range(1, num_stations + 1)):

        # Select the station:
        driver.find_element_by_xpath(f'//*[@id="ext-gen239"]/div[{station}]').click()

        # It is always safe to increase the implicit waiting time:
        driver.implicitly_wait(1)

        # Locate the iframe using its XPath
        iframe_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/iframe'  # Adjust as needed
        iframe_element = driver.find_element(By.XPATH, iframe_xpath)
        driver.switch_to.frame(iframe_element)

        tables_in_new_panel = driver.find_elements(By.TAG_NAME, 'table')

        # Call the function to extract the first table and convert it to a DataFrame
        first_table_df = extract_first_table_to_dataframe(tables_in_new_panel)

        # You can now work with the DataFrame
        tables_dict_1[station] = first_table_df
        tables_dict_2[station] = tables_in_new_panel[1].text

        # Once you're done, switch back to the default content
        driver.switch_to.default_content()

    # Extract the DataFrames from the dictionary
    dataframes_list = list(tables_dict_1.values())

    # Concatenate all the DataFrames into a single DataFrame
    stations_infos = pd.concat(dataframes_list, ignore_index=True)

    # Add years of streamflow data to the DataFrame
    for i in tqdm.tqdm(range(1, num_stations + 1)):
        stations_infos.loc[i - 1, "years_streamflow"] =  extract_protok_data_range(tables_dict_2[i])

    return stations_infos

def extract_years_from_ranges(range_str):
    """
    Convert a range string (e.g., "1953-2012\n2014\n2016-2018\n2021-2022") into a single list encompassing all years in the specified ranges.
    """
    # Initialize an empty list to store all the years
    all_years = []

    # Split the range string by '\n' to handle multiple ranges and individual years
    ranges = range_str.split('\n')

    # Iterate over each range part
    for range_part in ranges:
        # Check if the part contains a hyphen (indicating a range)
        if '-' in range_part:
            # Split the range at the hyphen to extract the start and end years
            start_year, end_year = map(int, range_part.split('-'))
            
            # Generate a list of years from start to end year (inclusive)
            years = list(range(start_year, end_year + 1))
        else:
            # The part contains a single year (no hyphen)
            years = [int(range_part)]

        # Extend the all_years list with the years from this range or single year
        all_years.extend(years)
    
    # Sort the list of years in ascending order
    all_years.sort()

    return all_years
    
    
def download_data_HR(network_HR, PATH_EXP):
    """
    Downloads data from a specific website for HR (Croatia) region.

    Args:
        network_HR (pandas.DataFrame): DataFrame containing network information.
        PATH_EXP (str): Path to export the downloaded data.

    Returns:
        None
    """
    # URL of the website
    URL = "https://hidro.dhz.hr"
    
    # Path to the Chrome driver executable
    chrome_driver_path = 'code\python\E_complementary_streamflow_data\chromedriver.exe'

    # Create a WebDriver instance with the specified path
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    path = URL
    
    # First we get the URL:
    driver.get(path)

    # Wait for 10 seconds for elements to appear on the page
    driver.implicitly_wait(10)

    # Click to switch to the data information section
    driver.find_element_by_xpath('//*[@id="ext-gen139"]/em/span/span/span').click()

    # Click on the historic data section
    button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[3]/a[2]/em/span/span")
    driver.execute_script("arguments[0].click();", button)

    # Accept terms
    button = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button")
    driver.execute_script("arguments[0].click();", button)

    # Select the station
    driver.find_element_by_xpath('//*[@id="ext-gen239"]/div[7]').click()

    # Click to switch to streamflow (m3/s)
    driver.find_element_by_xpath('//*[@id="prik_tippod"]').click()

    # Expand the table
    button = driver.find_element_by_xpath('//*[@id="ext-gen355"]')
    driver.execute_script("arguments[0].click();", button)

    # XPath pattern to locate stations
    xpath_i = '//*[@id="ext-gen239"]/div[number]'

    # Loop through each station
    for z, station in tqdm.tqdm(enumerate(network_HR.num)):
        
        # Create an empty DataFrame to store data for the station    
        timeseriesfinal = pd.DataFrame(index = pd.date_range('01-01-1926','12-31-2023', freq='D'))

        # DataFrame to accumulate data
        dados_full = pd.DataFrame()

        # Extract station name
        namestation = network_HR.iloc[z, 1]

        # Generate XPath for the current station
        xpath = xpath_i.replace("number", str(station))

        # Click to open station data
        time.sleep(2)
        driver.find_element_by_xpath(xpath).click()

        # Extract years from the range
        years = extract_years_from_ranges(network_HR.iloc[z, -2])
        years.reverse()

        # Loop through each year
        for ano in years:
            time.sleep(2)

            # Click on the year
            element = driver.find_element_by_xpath('//*[@id="izbgod_b1"]')
            action = ActionChains(driver)
            action.click(on_element=element)
            action.perform()

            # Extract table HTML
            tbl = driver.find_element_by_xpath('//*[@id="ext-gen331"]').get_attribute('outerHTML')
            df = pd.read_html(tbl, decimal=',', thousands='.')

            # Convert HTML table to DataFrame
            dados_pluv = pd.DataFrame(index=range(len(df)), columns=[0, 1])

            for i in range(len(df)):
                dados_pluv.iloc[i, :] = df[i]

            # Combine date and year
            dados_pluv["dates"] = dados_pluv[0].astype(str) + str(ano)
            dados_pluv["dates"] = dados_pluv["dates"].astype(str)
            dados_pluv["dates"].replace({'00:00': ''}, regex=True, inplace=True)
            dados_pluv["dates"].replace({' ': ''}, regex=True, inplace=True)

            # Append data to the accumulation DataFrame
            dados_full = dados_full.append(dados_pluv, ignore_index=True)

        # Clean up the DataFrame
        dados_full.drop(0, axis=1, inplace=True)
        dados_full["dates"] = pd.to_datetime(dados_full['dates'], format='%d.%m.%Y')
        dados_full.columns = ["Qm3_s", "dates"]
        dados_full.set_index("dates", inplace=True)
        dados_full.replace('---', np.nan, inplace=True)
        dados_full = dados_full.astype(float)
        
        # Add station data to the final DataFrame
        timeseriesfinal.loc[:, int(namestation)] = dados_full.Qm3_s
        
        # Export data to CSV file
        timeseriesfinal.to_csv(f'{PATH_EXP}/Qm3s_{station}_{namestation}.csv')
