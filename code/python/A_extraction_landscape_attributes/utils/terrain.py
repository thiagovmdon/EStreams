#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""

import geopandas as gpd
import math
import pandas as pd

def calculate_dimensions(geometry_series):
    """
    Calculate the dimensions of the minimum rotated bounding box (MRBB) for each geometry in a GeoSeries.
    This function is usefull for determining the length of a catchment and therefore later the enlongation ratio

    Parameters:
    - geometry_series (GeoSeries): A GeoSeries containing Polygon geometries.

    Returns:
    - x_dims (GeoSeries): A GeoSeries containing the dimension along the x-axis (length) of each MRBB.
    - y_dims (GeoSeries): A GeoSeries containing the dimension along the y-axis (width) of each MRBB.
    - length (GeoSeries): a GeoSeries containing the length of each geometry after rotation. 
    """
    # Apply the convex hull operation
    convex_hull = geometry_series.convex_hull

    # Compute the minimum rotated bounding box (MRBB) for each geometry
    mbr = convex_hull.apply(lambda x: x.minimum_rotated_rectangle)

    # Compute the dimension along the x-axis (length) of each MRBB
    x_dims = mbr.apply(lambda x: max(x.minimum_rotated_rectangle.exterior.xy[0]) - min(x.minimum_rotated_rectangle.exterior.xy[0]))
    x_dims = abs(x_dims)

    # Compute the dimension along the y-axis (width) of each MRBB
    y_dims = mbr.apply(lambda x: max(x.minimum_rotated_rectangle.exterior.xy[1]) - min(x.minimum_rotated_rectangle.exterior.xy[1]))
    y_dims = abs(y_dims)

    # Calculate the maximum between x and y dimensions for each MRBB
    length = pd.concat([x_dims, y_dims], axis=1).max(axis=1)
    
    return x_dims, y_dims, length


def calculate_elongation_ratio(basin):
    """
    Calculate the Elongation Ratio (Schumm, 1956) for a single basin in a DataFrame.

    Parameters:
    - row (pd.Series): A row of a DataFrame containing 'area' and 'length' columns.

    Returns:
    - elongation_ratio (float): Calculated Elongation Ratio.
    """
    pi_value = math.pi
    area = basin['area']/1000000
    length = basin['length']/1000
    elongation_ratio = 2 * math.sqrt(area / pi_value) / length
    
    return elongation_ratio