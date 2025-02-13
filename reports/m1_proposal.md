## Description of the Data

We will be using two datasets from the Vancouver Open Data portal to explore the relationship between **rental issues and property values** across different neighborhoods.

### **1. Property Tax Report (2025)**
This dataset contains property assessment values, tax information, and zoning details for properties in Vancouver.
- **Key attributes:**
  - `PID`, `from_civic_number`, `street_name`: Unique property identifiers and address details.
  - `CURRENT_LAND_VALUE`, `CURRENT_IMPROVEMENT_VALUE`: Assessed property value.
  - `TAX_LEVY`: Total property tax levied.
  - `YEAR_BUILT`, `BIG_IMPROVEMENT_YEAR`: Construction and renovation details.
  - `ZONING_DISTRICT`: Classification of property zones.

### **2. Rental Standards - Current Issues**
This dataset records **unresolved rental issues** in multi-unit buildings (5+ units).
- **Key attributes:**
  - `streetnumber`, `street`: Property address for merging datasets.
  - `TOTALOUTSTANDING`: Count of unresolved rental issues.
  - `TotalUnits`: Number of rental units per property.
  - `Geo Local Area`, `geo_point_2d`: Neighborhood and geolocation data.

This analysis will help identify trends and challenges in Vancouver’s rental market.
