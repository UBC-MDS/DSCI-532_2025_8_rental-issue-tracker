# DSCI-532_2025_8_rental-issue-tracker

The Rental Issue Tracker is a dashboard designed to help property managers and tenants track, manage, and analyze rental issues efficiently. This project is part of DSCI 532 (Data Visualization II) and aims to provide an interactive and intuitive interface for exploring reported rental issues.

## Motivation

### The problem

- It’s challenging for newcomers, like international students or new investors—to make informed decisions about rental housing options and neighborhood safety in Vancouver.
- Tenants, prospective renters, and investors lack easy access to data-driven insights that can help them identify trends, pinpoint high-risk properties, explore the connection between property violations and tax assessments, and estimate rental costs.

### The solution

The rental issue tracker app will:

- Combine rental property by-law issues with property tax data from the Vancouver Open Data portal to help users identify trends, pinpoint high-risk properties, explore the connection between property violations and tax assessments, and estimate rental costs.
- Feature an interactive map of Vancouver, allowing users to view brief information about rental properties.
- Provide additional insights through statistical charts on the right, offering detailed analysis of rental issues by property type and local area, as well as the correlation between property values and the number of outstanding violations.

## Data Description

The dashboard utilizes two primary datasets from the Vancouver Open Data portal:

### Property Tax Report
This dataset contains property assessment values and zoning information for Vancouver properties:
- Property identifiers and address details
- Current land and improvement values
- Property tax information
- Construction and renovation years
- Zoning classification

### Rental Standards - Current Issues
This dataset tracks unresolved rental issues in multi-unit buildings (5+ units):
- Property management information (business operator)
- Property location (address, neighborhood)
- Number of unresolved issues
- Total rental units per property
- Geolocation data

## Running app locally

1. Ensure you have the `conda` installed and inside the root directory of the repository, execute the following command:

```bash
conda env create -f environment.yml
```

2. From the root directory of this repository, start the app via `python -m src.app`. This will serve a web page locally, which you can view by navigating to the address `http://127.0.0.1:8050/` in your browser.

## Usage

- Open the Rental Issue Tracker app on your device or web browser to access the interactive dashboard for Vancouver’s rental market via this link https://dsci-532-2025-8-rental-issue-tracker.onrender.com/.
- Use the interactive map to view neighborhoods across Vancouver. Hover over areas to see brief details about rental properties, including property values and unresolved by-law violations. Red shading indicates high numbers of violations (Issues tab) or high property values (Value tab).
- Use the dropdown menu or filters in the bottom corner to explore specific neighborhoods, and building types.
- Check the statistical charts on the right side of the dashboard for detailed insights. View trends in rental issues, property values, and correlations between violations and tax assessments to make informed decisions.
- Use the app to pinpoint high-risk properties, estimate rental costs, and identify safe, well-maintained neighborhoods—perfect for tenants, prospective renters, or investors.

## Demo

![Demo](./img/demo.gif)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms. [`CONTRIBUTING.md`](https://github.com/UBC-MDS/DSCI-532_2025_8_rental-issue-tracker/blob/main/CONTRIBUTING.md)

## Contact us

If you want to report a problem or suggest an improvement, feel free to open an [`issue`](https://github.com/UBC-MDS/DSCI-532_2025_8_rental-issue-tracker/issues) at this github repository.
