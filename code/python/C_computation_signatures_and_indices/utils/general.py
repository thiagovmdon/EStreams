# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""


import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm
import geopandas as gpd
import tqdm as tqdm

warnings.simplefilter(action='ignore', category=Warning)


# Function to generate a dataframe with the number of measurements at the daily, monthly and annual time-steps:
# This function assumes that you give as input a time-series at the daily time-step.
# For the daily, the function computes the total number of measurements. For the monthly and yearly it gives both the number of 
# years and month with any, and completed (no gaps within the month or year). Both information might be usefull. 

def count_num_measurements(timeseries: pd.pandas.core.frame.DataFrame):
    """
    Inputs
    ------------------
    timeseries: dataset[Index = Datetime; columns = [Measurements]]: 
        dataframe with datetime as the index, and with each column representing one measurement. 
        It assumes that the gaps in the measurements are stored as np.nan
    Returns
    --------------------
    pandas.DataFrame [n x 6] with columns:
        'Code': Code of the station.
        
        'num_daily': Number of daily measurements.
        
        'num_monthly': Number of of months with any measurement.
        
        'num_yearly': Number of of months with any measurement.
        
        'num_monthly_complete': Number of months with complete measurements.
        
        'num_yearly_complete': Number years with complete measurements.
    """
    # First we create a dataframe for our measurements:
    num_measurements_df = pd.DataFrame(index = timeseries.columns)
    num_measurements_df.index.name = "Code"
    
    # Here we proceed at the daily time-step:
    num_measurements_df["num_daily_obs"] = timeseries.count()
    
    # Now we do the computation for the monthly step:
    timeseries_monthly = timeseries.resample('M').count() # First we count the number of days with non NaN values
    timeseries_monthly.replace(0, np.nan, inplace = True)
    
    num_measurements_df["num_monthly"] = (timeseries_monthly > 0).sum()
    num_measurements_df["num_monthly_complete"] = (timeseries_monthly >= 28).sum()
    
    # Now we do the computation for the yearly step:
    timeseries_yearly = timeseries.resample('Y').count() # First we count the number of days with non NaN values
    timeseries_yearly.replace(0, np.nan, inplace = True)
    
    num_measurements_df["num_yearly"] = (timeseries_yearly > 0).sum()
    num_measurements_df["num_yearly_complete"] = (timeseries_yearly >= 365).sum()
    
    return num_measurements_df


# Function to compute the longest gap periods for each column (measurement) in the input DataFrame.
def longest_gap_measurements(timeseries: pd.DataFrame):
    """
    Inputs
    ------------------
    timeseries: dataset[Index = Datetime; columns = [Measurements]]: 
        dataframe with datetime as the index, and with each column representing one measurement. 
        It assumes that the gaps in the measurements are stored as np.nan
    Returns
    --------------------
    pandas.Series with index as column names and values as the longest gap period.
    """


    # Calculate the longest continuous range with no gaps for each gauge
    longest_gap_periods = pd.DataFrame(index=timeseries.columns, columns=['longest_gap_period'])

    for col in tqdm(timeseries.columns):
        max_gap = 0
        current_gap = 0
        for value in timeseries[col]:
            if pd.notna(value):
                current_gap += 1
                max_gap = max(max_gap, current_gap)
            else:
                current_gap = 0
        longest_gap_periods.at[col, 'longest_gap_period'] = max_gap
    
    return longest_gap_periods

# Function to find the first date without gaps
def find_first_non_nan_dates(data):
    """
    Find the first date with a non-NaN value for each column in the DataFrame.

    Parameters:
    - data (pd.DataFrame): Input DataFrame with datetime index.

    Returns:
    - pd.Series: A Series containing the first date with a non-NaN value for each column.

    """
    first_non_nan_dates = data.apply(lambda col: col.first_valid_index())
    return first_non_nan_dates

# Function to find the last date without gaps
def find_last_non_nan_dates(data):
    """
    Find the last date with a non-NaN value for each column in the DataFrame.

    Parameters:
    - data (pd.DataFrame): Input DataFrame with datetime index.

    Returns:
    - pd.Series: A Series containing the last date with a non-NaN value for each column.
    """
    last_non_nan_dates = data.apply(lambda col: col.last_valid_index())
    return last_non_nan_dates

def calculate_areas_when_0(network, catchment_boundaries):
    """
    This function calculates the areas for catchments that present a area_calc
    equals to 0 to ensure no 0 is present.  

    Parameters
    ----------
    network (pd.DataFrame): Input DataFrame with estreams information, "basin_id" as index, 
    and at least one column as "area_calc".

    catchment_boundaries (geodataframe): Shapefile with the catchment boundaries and with the
    index set to "basin_id". 

    Returns
    -------
    network (pd.DataFrame): Same as initial, but with the "area_calc" updated. 
        
    """
    # This part is to reinforce that there are no areas with 0 km2:
    # Define the target CRS to ETRS89 LAEA (3035)
    target_crs = 'EPSG:3035'  

    # Reproject the GeoDataFrame to the target CRS
    catchment_boundaries_reprojected = catchment_boundaries.to_crs(target_crs)

    # We compute the areas again for the catchments with area equal to 0 km2:
    new_areas = catchment_boundaries_reprojected.loc[network[network.area_calc<=0].index.tolist(), :].area/1000000
    network.loc[new_areas.index, "area_calc"] = new_areas

    return network

def calculate_specific_discharge(network, timeseries_discharge):
    """
    This function calculates masks negative values and computes the specific discharge 
    of a time series. 

    Parameters
    ----------
    timeseries_discharge (pd.DataFrame): Input timeseries. Columns are the same as "basin_id"

    network (pd.DataFrame): Input DataFrame with estreams information, "basin_id" as index, 
    and at least one column as "area_calc".

    Returns
    -------
    timeseries_runoff (pd.DataFrame): Output timeseries. 

    """
    # Replace any negative value by np.nan:
    timeseries_discharge = timeseries_discharge.applymap(lambda x: np.nan if x < 0 else x)

    # Convert from cms to mm/day:
    timeseries_runoff = (timeseries_discharge * 86400 * 1000) / (network.area_calc * 1000000)

    # Sort the columns (make sure they are sorted):
    timeseries_runoff = timeseries_runoff.sort_index(axis=1)


    return timeseries_runoff

def check_for_potential_outliers(df, log_mean_df, log_std_df, threshould_std = 10):
    """
    Checks each specified original column in the DataFrame (df) to see if values are greater than the thresholds
    based on the mean and standard deviation values grouped by day of the year.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the time series data. Assumes DateTimeIndex.
    log_mean_df (pd.DataFrame): The DataFrame containing mean values grouped by the day of the year.
    log_std_df (pd.DataFrame): The DataFrame containing standard deviation values grouped by the day of the year.
    threshold_std (int): The number of standard deviations from the mean to use as a threshold.

    Returns:
    tuple: A tuple containing:
        - dict: A dictionary where keys are column names and values are DataFrames (from df) with rows where the conditions are met.
        - pd.DataFrame: A DataFrame with the same shape as df, containing a full mask indicating where the conditions are met.
    """
    # Initialize an empty dictionary to store results and a full mask with the same shape as df
    results = {}
    full_mask = pd.DataFrame(False, index=df.index, columns=df.columns)
    
    mean_df_above = log_mean_df + threshould_std*(log_std_df)
    mean_df_below = log_mean_df - threshould_std*(log_std_df)
    
    # Iterate through each column in df
    for column in tqdm.tqdm(df.columns):
        # Check if the column also exists in mean_df
        if column not in mean_df_above.columns:
            continue
        
        df_col = pd.DataFrame(df[column])
        mean_df_above_col = pd.DataFrame(mean_df_above[column])
        mean_df_below_col = pd.DataFrame(mean_df_below[column])
        
        # Convert mean_df index to 'day_of_year' to match the time series DataFrame
        mean_df_above_col['day_of_year'] = mean_df_above_col.index
        mean_df_below_col['day_of_year'] = mean_df_below_col.index
        
        # Calculate the day of the year for each index in df
        df_col['day_of_year'] = df.index.dayofyear
        df_col["date"] = df.index
        
        # Merge df with mean_df on the 'day_of_year' column
        merged_df = df_col.merge(mean_df_above_col, on='day_of_year', suffixes=('', '_mean'))
        merged_below_df = df_col.merge(mean_df_below_col, on='day_of_year', suffixes=('', '_mean'))

        # Use the sort_values() method to sort the merged DataFrame
        merged_df = merged_df.sort_values(by="date")
        merged_below_df = merged_below_df.sort_values(by="date")
        
        # Drop the "date" column
        merged_df.drop("date", axis=1, inplace=True)
        merged_below_df.drop("date", axis=1, inplace=True)
        
        # Reset the index
        merged_df.reset_index(drop=True, inplace=True)
        merged_below_df.reset_index(drop=True, inplace=True)
        
        # Apply the condition: value in df > 5 times the mean from mean_df
        mask1 = merged_df[column] > 1 * merged_df[f"{column}_mean"]
        mask2 = merged_below_df[column] < 1 * merged_below_df[f"{column}_mean"]
        
        # Combine the two masks using a logical AND (&) operator
        combined_mask = mask1 | mask2
    
        # Filter the DataFrame based on the mask
        filtered_df = merged_df[combined_mask][[column]]
        
        # Store the filtered DataFrame in the results dictionary
        results[column] = filtered_df
        
        # Update the full mask with the combined mask for the current column
        full_mask[column] = combined_mask.values

    # Return the results dictionary and the full mask
    return results, full_mask






