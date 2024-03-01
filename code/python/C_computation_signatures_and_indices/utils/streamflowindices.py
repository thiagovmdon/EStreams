#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""

import pandas as pd
import numpy as np 


def calculate_ct(streamflow, quality, hydro_year, threshould_days = 360):
    """
    This function calculates the Centre Timing (CT) which denotes the day of the year (DOY) at which 50 % 
    of the annual flow is reached. If hydro_year is set to calendar years, 1 denotes 1 January.

    Parameters
    ----------
    streamflow : np.array
        Array of daily streamflow measurements.
    quality : np.array
        Array containing the quality code for the daily streamflow measurements. 
        Data with good quality is "0", data with bad quality is "1"
    hydro_year : np.array
        Array expressing the hydrological year of the measurements.
    threshould_days : int
        This part considers only years with at least this threshould of daily measurements. 

    Returns
    -------
    dict
        'ct' : Centre timing for each year. 
    """
    

    # Define the CT function
    def calculate_ct_function(x):
        x = x['Q'].values
        if len(x) < 360:
            return np.nan
        else:
            # The +1 is needed to get the same definition of Addor
            return sum(x.cumsum() < 0.5*x.sum()) + 1

    # Construct a pandas DataFrame to filter
    data = pd.DataFrame(data=np.array([streamflow, quality]).transpose(),
                        index=hydro_year,
                        columns=['Q', 'QC'])

    data = data[data['QC'] == 0]
    
    # Check if data is empty
    if data.empty:
        ct = np.nan
    
    else:
        # Apply calculate_ct
        ct = data.groupby(data.index).apply(calculate_ct_function)
    
    return ct


def calculate_min_streamflow_day(streamflow, quality, hydro_year, threshould_days=360):
    """
    This function calculates the day of the year (DOY) with the minimum streamflow.

    Parameters
    ----------
    streamflow : np.array
        Array of daily streamflow measurements.
    quality : np.array
        Array containing the quality code for the daily streamflow measurements. 
        Data with good quality is "0", data with bad quality is "1"
    hydro_year : np.array
        Array expressing the hydrological year of the measurements.
    threshould_days : int
        This part considers only years with at least this threshould of daily measurements. 

    Returns
    -------
    int or np.nan
        Day of the year with the minimum streamflow for each year. 
    """
    
    # Define the function to calculate the day of minimum streamflow
    def calculate_min_streamflow_day_function(x):
        x = x['Q'].values
        if len(x) < threshould_days:
            return np.nan
        else:
            return x.argmin() + 1  # +1 to get the day of the year
    
    # Construct a pandas DataFrame to filter
    data = pd.DataFrame(data=np.array([streamflow, quality]).transpose(),
                        index=hydro_year,
                        columns=['Q', 'QC'])

    data = data[data['QC'] == 0]
    
    # Check if data is empty
    if data.empty:
        min_streamflow_day = np.nan
    
    else:
        # Apply calculate_min_streamflow_day_function
        min_streamflow_day = data.groupby(data.index).apply(calculate_min_streamflow_day_function)
    
    return min_streamflow_day


def calculate_max_streamflow_day(streamflow, quality, hydro_year, threshould_days=360):
    """
    This function calculates the day of the year (DOY) with the maximum streamflow.

    Parameters
    ----------
    streamflow : np.array
        Array of daily streamflow measurements.
    quality : np.array
        Array containing the quality code for the daily streamflow measurements. 
        Data with good quality is "0", data with bad quality is "1"
    hydro_year : np.array
        Array expressing the hydrological year of the measurements.
    threshould_days : int
        This part considers only years with at least this threshould of daily measurements. 

    Returns
    -------
    int or np.nan
        Day of the year with the maximum streamflow for each year. 
    """
    
    # Define the function to calculate the day of minimum streamflow
    def calculate_max_streamflow_day_function(x):
        x = x['Q'].values
        if len(x) < threshould_days:
            return np.nan
        else:
            return x.argmax() + 1  # +1 to get the day of the year
    
    # Construct a pandas DataFrame to filter
    data = pd.DataFrame(data=np.array([streamflow, quality]).transpose(),
                        index=hydro_year,
                        columns=['Q', 'QC'])

    data = data[data['QC'] == 0]
    
    # Check if data is empty
    if data.empty:
        max_streamflow_day = np.nan
    
    else:
        # Apply calculate_min_streamflow_day_function
        max_streamflow_day = data.groupby(data.index).apply(calculate_max_streamflow_day_function)
    
    return max_streamflow_day


def calculate_gini_coefficient(streamflow, quality, hydro_year, threshold_days=360):
    """
    This function calculates the Gini coefficient for the annual streamflow.

    Parameters
    ----------
    streamflow : np.array
        Array of daily streamflow measurements.
    quality : np.array
        Array containing the quality code for the daily streamflow measurements. 
        Data with good quality is "0", data with bad quality is "1".
    hydro_year : np.array
        Array expressing the hydrological year of the measurements.
    threshold_days : int
        Minimum number of days required for a valid year.

    Returns
    -------
    float or np.nan
        Gini coefficient for each year. 
    """

    def calculate_gini_coefficient_function(x):
        x = x['Q'].values
        if len(x) < threshold_days:
            return np.nan
        else:
            # Normalize streamflow values
            x_normalized = x / np.sum(x)
            # Sort the streamflow values
            x_sorted = np.sort(x_normalized)
            # Calculate the Gini coefficient
            n = len(x_sorted)
            gini_coefficient = (2 * np.sum(np.arange(1, n + 1) * x_sorted) - (n + 1)) / n / np.sum(x_sorted)

            return gini_coefficient

    # Construct a pandas DataFrame to filter
    data = pd.DataFrame(data=np.array([streamflow, quality]).transpose(),
                        index=hydro_year,
                        columns=['Q', 'QC'])

    data = data[data['QC'] == 0]

    # Check if data is empty
    if data.empty:
        gini_coefficient = np.nan
    else:
        # Apply calculate_gini_coefficient_function
        gini_coefficient = data.groupby(data.index).apply(calculate_gini_coefficient_function)

    return gini_coefficient


def calculate_iqr(x, threshold):
    """
    Calculate the Interquartile Range (IQR) for a given array, if the number of non-nan values is above a specified threshold.

    Parameters
    ----------
    x : array-like
        Input array for which IQR is calculated.
    threshold : int
        The minimum number of non-nan values required to calculate IQR.

    Returns
    -------
    float or np.nan
        Interquartile Range (IQR) if the number of non-nan values is above the threshold, otherwise np.nan.
    """
    if len(x.dropna()) >= threshold:
        return np.percentile(x.dropna(), 75) - np.percentile(x.dropna(), 25)
    else:
        return np.nan

# It seems that the function within the module (HydroAnalyis) is not working, therefore we need to update this part with the 
# following code:

def calculate_hydro_year(date, first_month=10):
    """
    This function calculates the hydrological year from a date. The
    hydrological year starts on the month defined by the parameter first_month.

    Parameters
    ----------
    date : pandas.core.indexes.datetimes.DatetimeIndex
        Date series
    first_month : int
        Number of the first month of the hydrological year

    Returns
    -------
    numpy.ndarray
        Hydrological year time series
    """

    hydrological_year = date.year.values.copy()
    hydrological_year[date.month >= first_month] += 1

    return hydrological_year
