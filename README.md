# EStreams
This repository is part of the EStreams project and encompass all the code used to derive the aggregated data.

## Description 
We present an extensive database and catalogue of hydro-climatic and landscape descriptors for 15,046 catchments in Europe: EStreams. The data covers more than 100 years of open-source catchment aggregated landscape attributes (terrain, soils, lithology, vegetation and land cover), climatic forcing time-series, streamflow gauges indices and a catalogue of streamflow time-series for Europe (European streamflow and where to find them). EStreams offers both an extensive and extensible data collection together with codes for performing the whole data retrieval and processing. Our vision is to provide a further step towards the integration of hydro-climatic and landscape datasets for Europe and to speed up the data collection process by providing to users a ready-to-use database for large-scale hydrological analysis or model simulations. 

## About this repository 
This repository is divided into four folders:

| folder      | description                                                       |
| ------------| ----------------------------------------------------------------- |
| code        | where all the code used to derive the dataset is stored.          |
| data        | where the original source data should be stored to run the codes. |
| environments| where a environment.yml and a requirements.txt are provided.      |
| results     | where all the results are stored.                                 |

* Note that due to redistribution and storage reasons the data folder is empty, however complete guidance about the files, version, where to download and where to upload them are provided in their respective readme.txt files. 

## Using this repository 
if users want to use this repository to repeat or adapt the extraction process to their data, we recomend:
- Clone this repository locally.
- Place all files with their adequate names (see the readme.txt files at each data subfolders).
- Do not change anything in the folders structures or file names. 

If the repository was cloned locally and all the original data necessary to extract and aggregate the attributes are stored adequately the users should not experinece any problem running the scripts. 

## Reference
The EStreams dataset (https://doi.org/10.5281/zenodo.10733142) and its corresponding manuscript are currently under revision. If users want to use the data, we recomend them to cite the pre-print and Zenodo repositories in their research. 

## Contact information
If you have any questions/feedback, please contact Thiago Nascimento (thiago.nascimento@eawag.ch)

> Date: 01.03.2024