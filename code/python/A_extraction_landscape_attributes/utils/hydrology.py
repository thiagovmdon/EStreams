# -*- coding: utf-8 -*-
"""
This file is part of the EStreams dataset. See https://github.com/EStreams for details.

Coded by: Thiago Nascimento
"""
import geopandas as gpd
import pandas as pd

def count_geometries_in_polygons(geometries, polygons, polygon_id="id", new_column="points_count"):
    """
    Inputs
    ------------------
    geometries: geodataframe the polygons we are interested to count  
    polygons: geodataframe with the catchment polygon boundaries   
    polygon_id: string with the unique-identifier for each catchment polygon
    new_column: string with the column's name
    --------------------
    pandas.DataFrame [n x 6] with columns:
        'Code': Code of the catchment.
        'new_column': Number of geometries within each catchment polygon.
        
    """
    
    # Count geometries in polygons
    points_in_polygon = (
        # Spatial join associates points and polygons that intersects each other
        polygons.sjoin(
            geometries,
            how="inner",
        )
        .groupby(polygon_id)  # Group points by polygons
        .size()  # Get number of points
        .rename(new_column)  # Name your column as you want it to appear in polygons
    )

    # Create a dataframe:
    count_df = pd.DataFrame(index = polygons[polygon_id], data = points_in_polygon)
    count_df.fillna(0, inplace=True)
    
    return count_df
