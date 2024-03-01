#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""

import numpy as np
import pandas as pd

def get_majority_columns(row):
    """
    Get the majority column for each year based on the maximum value for columns containing "lulc_" in the DataFrame.

    Parameters:
    - row (pd.Series): A row in the DataFrame.

    Returns:
    - pd.Series: A Series containing the majority columns for each year with "lulc_" prefix.
    """
    # Select columns containing "lulc_" in the DataFrame
    lulc_cols = [col for col in row.index if "lulc_" in col]
    
    years = set(col.split('_')[1] for col in lulc_cols)
    majority_columns = {}

    for year in years:
        # Select columns for the current year
        year_cols = [col for col in lulc_cols if f'_{year}_' in col]
        
        # Check if any value in the relevant columns is NaN
        if not row[year_cols].isna().any():
            # Get the majority column for the current year
            majority_columns[f'lulc_dom_{year}'] = int(row[year_cols].idxmax().split('_')[2])
        else:
            # If any value is NaN, set the majority column to pd.NaT
            majority_columns[f'lulc_dom_{year}'] = np.nan

    return pd.Series(majority_columns)