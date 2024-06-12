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
import re

def download_data_ITIS(station_code, PATH_EXP):
    """
    Fetches streamflow time series data for a single station code.
    
    Args:
    - station_code (str): Station code
    - PATH_EXP (str): Path to export the downloaded data
    
    Returns:
    - None
    """
    # Define the URL pattern for fetching data
    URL = "http://hydroserver.ddns.net/italia/REGION/index.php/default/services/cuahsi_1_1.asmx/GetValuesObject?authToken=&location=STATION&variable=REGION:Discharge"
    
    # Replace placeholders in the URL with the current station code
    url = URL.replace("STATION", station_code)
    url = url.replace("REGION", station_code[0:7])
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Initialize variable to store time series data
    time_series_df = None
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML content
        root = ET.fromstring(response.text)

        # Initialize lists to store data
        date_times = []
        values = []
        quality_control_levels = []

        # Iterate through the 'value' elements in the XML and extract relevant data
        for value_elem in root.findall('.//{http://www.cuahsi.org/waterML/1.1/}value'):
            date_time = value_elem.get('dateTime')
            value = float(value_elem.text)
            quality_control_level = int(value_elem.get('qualityControlLevelCode'))
            date_times.append(date_time)
            values.append(value)
            quality_control_levels.append(quality_control_level)

        # Create a DataFrame from the extracted time series data
        time_series_df = pd.DataFrame({'dateTime': date_times, 'Value': values, 'QualityControlLevelCode': quality_control_levels})
        # Modify the station code if necessary
        modified_station_code = re.sub(r'[^\w]', '_', station_code)
        # Export data to CSV file
        time_series_df.to_csv(f'{PATH_EXP}/qm3s_{modified_station_code}.csv', index=False)


def download_metadata_ITIS(station_code, PATH_EXP):
    """
    Fetches metadata for a single station code.
    
    Args:
    - station_code (str): Station code
    - PATH_EXP (str): Path to export the downloaded data
    
    Returns:
    - None
    """
    # Define the URL pattern for fetching data
    URL = "http://hydroserver.ddns.net/italia/REGION/index.php/default/services/cuahsi_1_1.asmx/GetValuesObject?authToken=&location=STATION&variable=REGION:Discharge"
    
    # Replace placeholders in the URL with the current station code
    url = URL.replace("STATION", station_code)
    url = url.replace("REGION", station_code[0:7])
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Initialize variable to store metadata
    metadata_series = None
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML content
        root = ET.fromstring(response.text)

        # Extract metadata from the XML
        source_info_elem = root.find('.//{http://www.cuahsi.org/waterML/1.1/}sourceInfo')
        if source_info_elem is not None:
            site_name = source_info_elem.find('{http://www.cuahsi.org/waterML/1.1/}siteName').text
            site_code = source_info_elem.find('{http://www.cuahsi.org/waterML/1.1/}siteCode').text
            site_id = source_info_elem.find('{http://www.cuahsi.org/waterML/1.1/}siteCode').get('siteID')
            latitude = source_info_elem.find('.//{http://www.cuahsi.org/waterML/1.1/}latitude').text
            longitude = source_info_elem.find('.//{http://www.cuahsi.org/waterML/1.1/}longitude').text

            # Create a DataFrame for the metadata
            metadata_df = pd.DataFrame({
                'siteName': [site_name],
                'code': [station_code],
                'siteCode': [site_code],
                'siteID': [site_id],
                'latitude': [latitude],
                'longitude': [longitude]
            })
            # Modify the station code if necessary
            modified_station_code = re.sub(r'[^\w]', '_', station_code)
            
            # Export data to CSV file
            metadata_df.to_csv(f'{PATH_EXP}/metadata_{modified_station_code}.csv', index=False)
