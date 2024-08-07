# Changelog

## [1.0.0] - 2024-08-07
### Added

### Changed
- updated readme.md file
- updated the codes for time-series demonstration from FR, HR and IE at [utils](https://github.com/thiagovmdon/EStreams/tree/main/code/python/D_demonstration_streamflow_data/utils)
- The current version used for [selenium](https://github.com/thiagovmdon/EStreams/tree/main/environments) was updated in the environments lists. 

### Fixed
- The code for the retrieve of the list of nested catchments per basin was fixed, and now makes sure to include their respective basin outlet, when it was missing [#fixednestedlist](https://github.com/thiagovmdon/EStreams/tree/main/code/python/E_complementary_extra_codes/estreams_extras_nested_catchments)

## [0.1.2] - 2024-06-15
### Added
- addition of the folder [D_demonstration_streamflow_data](https://github.com/thiagovmdon/EStreams/tree/main/code/python/D_demonstration_streamflow_data) with two codes for the demonstration of the catalogue and data organization.
- addition of a code for [#filterduplicates](https://github.com/thiagovmdon/EStreams/blob/main/code/python/E_complementary_extra_codes/estreams_extras_filter_duplicates.ipynb) in the EStreams dataset.
- folder where the raw streamflow data should be place [#rawdata](https://github.com/thiagovmdon/EStreams/tree/main/data/streamflow/raw_data).

### Changed
- updated readme.md file
- updated the gee code for landcover attributes aggregation to deal easily with downloading chuncks of data [#landcovergee](https://github.com/thiagovmdon/EStreams/blob/main/code/gee/EStreams_landscape_attributes_landcover_gee.txt).
- update the name of the additional codes to [E_complementary_extra_codes](https://github.com/thiagovmdon/EStreams/tree/main/code/python/E_complementary_extra_codes).

### Fixed
- meteorological time series variable name changed from "sp_min" to "sp_mean" [#updatenames](https://github.com/thiagovmdon/EStreams/blob/main/code/python/B_extraction_meteorological_records/estreams_meteorology_timeseries_c.ipynb).
- adjust in both [#environments](https://github.com/thiagovmdon/EStreams/tree/main/environments) files. 

## [0.1.0] - 2024-03-02
- Initial release