# Project Overview

This repository contains the data and code for an interactive visualization project that explores the correlation between environmental emissions and human health, particularly respiratory and liver diseases.

## Contents

- `Results/`: Images generated from producer.py script.
- `sdg_13_10_esmsip2.sdmx/` `tps00001.tsv`: Data file dir for Sustainable Development Goals related to climate action.
- `2013_liver`, `2013_Respiratory`, `2018_Respiratory`, `2021_liver`, `2021_Respiratory`: HTML documents visualizing health data per year.
- `countries_emissions.geojson`: GeoJSON data mapping country emissions.
- `Graphics.ipynb`: [Testing phase] Jupyter notebook used for creating graphics.
- `HFA_73_EN`, `HFA_212_RESPIRATORY_EN`: Excel files containing health-focused data.
- `producer.py`: Script to build the datasets and the png.
- `producer_folium.py`: Script to build the datasets and the interactive map in html
- `README.md`: Documentation of the project structure and instructions.
- `session-6-Valeria-ImpactOfClimateChange...`: PDF document outlining project goals and findings.
- `Folium_implementation.ipynb`: [Testing phase] Jupyter notebook with the Folium implementation code.
- `tools.py`: Auxiliary file for functions for producer files.

## Interactive Visualization

The key component of this project is the interactive map created using the Folium library, which visually represents the link between emissions and reported cases of certain disease over time. The map allows users to see the density of health issues against the backdrop of emissions intensity.

## Getting Started

To view the interactive maps:
1. Navigate to the `Results/` directory.
2. Open any of the HTML documents in a web browser.

To explore the data analysis process:
1. Review Jupyter notebooks within the `Graphics/` directory.

For a full understanding of the project's context:
1. Read the `session-6-Valeria-ImpactOfClimateChange...` PDF.
2. Examine the data in Excel files.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

---

Embrace the exploration of data-driven environmental health insights and contribute to a project that seeks not only to inform but to inspire action.