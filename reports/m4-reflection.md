# Milestone 4 Reflection

## Refinement

We have implemented most of the feedback given by instructors and students, including:

- **Map refinements**: Added zoom and boundary limits so users cannot navigate outside of Vancouver, and also added coloured polygons overlaying neighbourhod regions which display upon selection.
- **Interactive click selection**: zoning classes and neighburhoods can be selected directly on the respective bar and pie charts.
- **Minor aesthetic improvements**: the scatterplot has angled x-axis price labels, for easier interpretation of where specific price values lie.
- **Remove N/A Button**: Properties with missing value/zoning classes can be easily filtered using a button next to the dropdowns.
- **Performance Improvements**: Data has been saved into binary formats, and Flask/LRU Caching is implemented on map callbacks and data.

## Deviations from Proposal

As stated before, we did not implement the gridding/interpolation from the original proposal, due to difficulty, time constraints, and prioritization of other visualization methods; for example, the polygon neighbourhood bounds in addition to interpolation heatmaps of rental issues would have made the map cumbersome and overly busy.

## Current Issues

An issue we could not solve was between the dropdown and bar chart updates: selecting a zone on the bar chart correctly updates the dropdown, but selection from the dropdown does not update the colour highlighting of the bar chart. We were unable to find a solution to this problem in time for the due date, but it is a minor issue that slightly effects the aesthetic consistency of the dashboard. The selection of the bar chart can be reset by double-clicking the bar chart, but this unfortunately does not update the dropdown.

## Final Reflection

Now that the dashboard has been improved in performance and interactivity, it is much easier for users to get the exact information they want. This makes it more useful for a variety of renter demographics: business owners, residential renters, etc. An interesting improvement to the dashboard would be to set up a CI/CD pipeline that routinely updates the dashboard with new data on rental issues, since the data repository is constantly being updated as bylaw issues are solved and are found (We are using data obtained from early February).