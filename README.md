# EStreams

This repository is part of the EStreams project and encompasses all the code used to derive the dataset, some additional demonstrations and examples. 

## Description 

_EStreams_ is an extensive database and catalogue of hydro-climatic and landscape descriptors for +17,000 catchments in Europe. The data covers more than 100 years of open-source catchment aggregated landscape attributes (terrain, soils, lithology, hydrology, vegetation and land cover), climatic forcing time-series, streamflow gauges indices and signatures and a catalogue with detailed information European streamflow time-series and where to find them. EStreams offers both an extensive and extensible data collection together with codes for performing the whole data retrieval and processing. Our vision is to provide a further step towards the integration of hydro-climatic and landscape datasets for Europe and to speed up the data collection process by providing to users a ready-to-use database for large-scale hydrological analysis or model simulations. 

The EStreams dataset can be found [here](https://doi.org/10.5281/zenodo.10733142), and is currently described by the [preprint](https://doi.org/10.31223/X5M39F) (accepted for publication at Nature Scientific Data).

## About this repository 

This repository is divided into four folders:

| folder      | description                                                       |
| ------------| ----------------------------------------------------------------- |
| code        | where all the code used to derive the dataset is stored.          |
| data        | where the original source data should be stored to run the codes. |
| environments| where a environment.yml and a requirements.txt are provided.      |
| results     | where all the results are stored.                                 |

- Note that due to redistribution and storage reasons the _data_ folder is empty, however complete guidance about the files, versions, where to download and where to upload them are provided in their respective readme.txt files. 

## Using this repository 

- Clone this repository locally.
- Place all files with their adequate names (see the readme.txt files at each data subfolders).
- Do not change anything in the folders structures or file names. 

## Setup Instructions

To reproduce the Python environment for this project, you can use either the `environment.yml` file (for conda users) or the `requirements.txt` file (for pip users).

### Using `environment.yml` (Conda)

1. Clone the repository:
   `git clone https://github.com/thiagovmdon/EStreams.git`

2. Create the conda environment:
   `conda env create -f environment.yml`

3. Activate the conda environment:
   `conda activate estreams`

### Using `requirements.txt` (pip)

1. Clone the repository:
   `git clone https://github.com/thiagovmdon/EStreams.git`

2. Create a virtual environment:
   `python -m venv venv`

3. Activate the virtual environment:

   - On Windows:
     `venv\Scripts\activate`

   - On macOS and Linux:
     `source venv/bin/activate`

4. Install the dependencies:
   `pip install -r requirements.txt`
   
## References
The [dataset](https://doi.org/10.5281/zenodo.10733142) and its corresponding [preprint](https://doi.org/10.31223/X5M39F). If users want to use the data, we recomend them to cite the pre-print and Zenodo repositories in their research. 

Additionally, we would highly appreciated if you also cite the corresponding sources datasets used to derive the EStreams dataset. For details on the references, see the information included in the licenses folder of the EStreams dataset and in the preprint. 

## Contact information
If you have any questions/feedback, please contact Thiago Nascimento (thiago.nascimento@eawag.ch)