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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def extract_first_table_to_dataframe(tables_in_new_panel):
    # Check if there are tables available
    if not tables_in_new_panel:
        return None

    table = tables_in_new_panel[0]
    column_headers = []
    values = []

    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if not cells:
            cells = row.find_elements(By.TAG_NAME, 'th')

        if len(cells) >= 2:
            column_name = cells[0].text.strip()
            value = cells[1].text.strip()
            column_headers.append(column_name)
            values.append(value)

    df = pd.DataFrame([values], columns=column_headers)
    return df

def extract_protok_data_range(text):
    pattern_protok_section = r'PROTOK Ekstremi\n(.*?)\n(?=(?:VODOMJERENJA|PROFILI|$))'
    match_protok_section = re.search(pattern_protok_section, text, re.DOTALL)

    if match_protok_section:
        protok_section = match_protok_section.group(1)
        pattern_data_range = r'Godine mjerenja:\n([\d-]+(?:\n[\d-]+)*)'
        match_data_range = re.search(pattern_data_range, protok_section)
        if match_data_range:
            return match_data_range.group(1)
        else:
            return np.nan
    else:
        return np.nan

def get_metadata_HR(num_stations):
    tables_dict_1 = {}
    tables_dict_2 = {}

    URL = "https://hidro.dhz.hr"
    chrome_driver_path = 'code/python/D_demonstration_streamflow_data/chromedriver.exe'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(URL)
    driver.implicitly_wait(10)
    
    driver.find_element(By.XPATH, '//*[@id="ext-gen139"]/em/span/span/span').click()
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[3]/a[2]/em/span/span")
    driver.execute_script("arguments[0].click();", button)
    button = driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button")
    driver.execute_script("arguments[0].click();", button)

    for station in tqdm.tqdm(range(1, num_stations + 1)):
        driver.find_element(By.XPATH, f'//*[@id="ext-gen239"]/div[{station}]').click()
        driver.implicitly_wait(1)

        iframe_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/iframe'
        iframe_element = driver.find_element(By.XPATH, iframe_xpath)
        driver.switch_to.frame(iframe_element)

        tables_in_new_panel = driver.find_elements(By.TAG_NAME, 'table')
        first_table_df = extract_first_table_to_dataframe(tables_in_new_panel)
        tables_dict_1[station] = first_table_df
        tables_dict_2[station] = tables_in_new_panel[1].text

        driver.switch_to.default_content()

    dataframes_list = list(tables_dict_1.values())
    stations_infos = pd.concat(dataframes_list, ignore_index=True)

    for i in tqdm.tqdm(range(1, num_stations + 1)):
        stations_infos.loc[i - 1, "years_streamflow"] = extract_protok_data_range(tables_dict_2[i])

    return stations_infos

def extract_years_from_ranges(range_str):
    all_years = []
    ranges = range_str.split('\n')

    for range_part in ranges:
        if '-' in range_part:
            start_year, end_year = map(int, range_part.split('-'))
            years = list(range(start_year, end_year + 1))
        else:
            years = [int(range_part)]
        all_years.extend(years)
    
    all_years.sort()
    return all_years

def download_data_HR(network_HR, PATH_EXP):
    URL = "https://hidro.dhz.hr"
    chrome_driver_path = 'code/python/D_demonstration_streamflow_data/chromedriver.exe'
    
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(URL)
    driver.implicitly_wait(10)
    
    driver.find_element(By.XPATH, '//*[@id="ext-gen139"]/em/span/span/span').click()
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[3]/a[2]/em/span/span")
    driver.execute_script("arguments[0].click();", button)
    button = driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button")
    driver.execute_script("arguments[0].click();", button)
    driver.find_element(By.XPATH, '//*[@id="ext-gen239"]/div[7]').click()
    driver.find_element(By.XPATH, '//*[@id="prik_tippod"]').click()
    button = driver.find_element(By.XPATH, '//*[@id="ext-gen355"]')
    driver.execute_script("arguments[0].click();", button)

    xpath_i = '//*[@id="ext-gen239"]/div[number]'

    for z, station in tqdm.tqdm(enumerate(network_HR.num)):
        timeseriesfinal = pd.DataFrame(index=pd.date_range('01-01-1926', '12-31-2023', freq='D'))
        dados_full = pd.DataFrame()
        namestation = network_HR.iloc[z, 1]
        xpath = xpath_i.replace("number", str(station))
        time.sleep(2)
        driver.find_element(By.XPATH, xpath).click()
        years = extract_years_from_ranges(network_HR.iloc[z, -2])
        years.reverse()
    
        for ano in years:
            time.sleep(2)
            element = driver.find_element(By.XPATH, '//*[@id="izbgod_b1"]')
            action = ActionChains(driver)
            action.click(on_element=element)
            action.perform()
            tbl = driver.find_element(By.XPATH, '//*[@id="ext-gen331"]').get_attribute('outerHTML')
            df = pd.read_html(tbl, decimal=',', thousands='.')
            dados_pluv = pd.DataFrame(index=range(len(df)), columns=[0, 1])

            for i in range(len(df)):
                dados_pluv.iloc[i, :] = df[i].iloc[:, :2].values
            

            dados_pluv["dates"] = dados_pluv[0].astype(str) + str(ano)
            dados_pluv["dates"] = dados_pluv["dates"].astype(str)
            dados_pluv["dates"].replace({'00:00': ''}, regex=True, inplace=True)
            dados_pluv["dates"].replace({' ': ''}, regex=True, inplace=True)
            dados_full = pd.concat([dados_full, dados_pluv], ignore_index=True)
            

        dados_full.drop(0, axis=1, inplace=True)
        dados_full["dates"] = pd.to_datetime(dados_full['dates'], format='%d.%m.%Y')
        dados_full.columns = ["Qm3_s", "dates"]
        dados_full.set_index("dates", inplace=True)
        dados_full.replace('---', np.nan, inplace=True)
        dados_full = dados_full.astype(float)
        timeseriesfinal.loc[:, int(namestation)] = dados_full.Qm3_s
        timeseriesfinal.to_csv(f'{PATH_EXP}/Qm3s_{station}_{namestation}.csv')