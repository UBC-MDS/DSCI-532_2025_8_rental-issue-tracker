# Milestone 2 Reflection

## Features Implemented From Proposal

The following features from our proposal and app sketch have been implemented:

- A **bar chart** showing how the number of rental issues vary with property zoning type. 
When a district is selected in the dropdown, the bar chart only shows the distribution of rental issues for that particular district.

- A **scatterplot** showing how property value is associated to the number of rental issues,
 which can be narrowed down to show trends in specific districts in Vancouver using the dropdown.

- A **pie chart** showing how the number of rental issues varies with each district. 
Proportions for specific districts can be highlighted using the dropdown.

- An **interactive map** which displays properties across Vancouver with rental issues. 
Icons are coloured by their zoning type, and the tooltip shows useful info such as the property manager, address, zoning type, 
number of units and most importantly the number of issues. The map can zoom in to different districts in Vancouver using the dropdown. 
Some properties have missing property value and zoning types, and are coloured as grey on the map.

## New Features Not From Proposal

**Icon filtering by zoning type:** Using one of the dropdowns, the user can choose to show properties of specific zoning types. 
This was done to add extra interactivity and prevent the map from becoming too crowded with all icons at once.

## Features Not Implemented From Proposal

- **Global gridding of rental issues/property value:** Unfortunately setting up the interactive map took extensive time to debug, 
so we did not have time to implement the gridding of rental issues and property values. 
We would like to implement this in the future, if time permits.

- **More detailed scatterplot:** We will incorporate more information in the scatter plot 
-such as color coding by district and encoding size by number of units- in a future milestone. 
We have not yet implemented this due to time constraints and uncertainty about how to effectively 
visualize this without making the plot too busy with many colors, point sizes, and trendlines.

## Final Reflection and Additional Improvements

The dashboard has interactivity that is simple for the user to grasp, and is consistent between all plots and the map which helps with 
narrowing down the displayed information to depict useful trends in rental issues across Vancouver.
The dashboard is heavily lacking in layout and aesthetics due to the time it took to implement the interactive elements.
Therefore some future improvements (that were not already previously mentioned) may be:

- Organize the layout more effectively so all plots/maps are appropriately sized and fit on the screen
- Make color coding of the bar plot consistent with map icon colors and organize the bars by length for easier viewing/juxtaposition
- Fill additional whitespace with a title, summary statistics and information about the displayed data and how to interact with the app.
