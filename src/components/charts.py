import altair as alt
from ..data.data import load_data, zone_icon_dict, neighborhood_color_range

issues_values_joined, property_values, issues, area_boundaries, neighborhoods, boundary_index, style_dictionary = load_data()

def create_pie_chart(data, selected_region):
    """Creates a donut chart showing the distribution of rental issues by local area."""

    base = alt.Chart(data, title='Number of Rental Issues', height=250).mark_arc(
        innerRadius=50,
    ).encode(
        theta=alt.Theta('total_outstanding', type='quantitative'),
        tooltip=['geo_local_area', 'total_outstanding'],
        order=alt.Order('total_outstanding:Q', sort='descending')
    )

    if selected_region is not None:
        chart = base.encode(
            color=alt.condition(
                alt.datum.geo_local_area == selected_region,
                alt.Color('geo_local_area:N', title='Local Area', scale=alt.Scale(
                    domain=neighborhoods,
                    range=neighborhood_color_range
                )),
                alt.value('gray'),
            ),
            opacity=alt.condition(
                alt.datum.geo_local_area == selected_region,
                alt.value(1.0),
                alt.value(0.2)
            )
        )
    else:
        # If no selected_location, use full color for all
        chart = base.encode(
            color=alt.Color('geo_local_area:N', title='Local Area', scale=alt.Scale(
                    domain=neighborhoods,
                    range=neighborhood_color_range
                ))
        )
    return chart

# Create horizontal bar chart function
def create_bar_chart(data, x_col, y_col, title, x_title=None, y_title=None):
    # Sort data by x_col for consistent visualization
    data = data.sort_values(by=x_col, ascending=True)
    
    # Set default titles if not provided
    if x_title is None:
        x_title = x_col
    if y_title is None:
        y_title = y_col
    
    # Define a selection for interactivity
    zoning_select = alt.selection_point(
        name='zoning_select',
        fields=['zoning_classification'],
        on='click[!event.shiftKey && !event.ctrlKey]',  
        empty=True,  
        toggle=False  
    )
    
    # Create the bar chart with explicit type specifications
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(x_col, title=x_title, type='quantitative'),
        y=alt.Y(y_col, title=y_title, type='nominal').sort('-x'),  
        color=alt.condition(
            zoning_select,
            alt.Color(y_col, type='nominal').scale(  
                domain=list(zone_icon_dict.keys()),
                range=[tup[0] for tup in zone_icon_dict.values()]
            ).legend(None),
            alt.value('lightgray')
        ),
        tooltip=[alt.Tooltip(x_col, title=x_title)]
    ).add_params(zoning_select).properties(
        title=title,
        width=600
    )
    # Return the chart specification as a dictionary
    return chart.to_dict()

    # Create scatter plot
def create_scatter_plot(data, x_col, y_col, title,scale_type,x_title=None, y_title=None):
    """Create a scatter plot with regression line using Altair library for rental property data."""

    if x_title is None:
        x_title = x_col
    if y_title is None:
        y_title = y_col
    
    points = alt.Chart(data, height=250).mark_point(filled=True, opacity=0.7).encode(
        y=alt.Y(y_col, title=y_title)
                .axis(tickMinStep=1,format='d'),
        x=alt.X(x_col, title=x_title)
                .scale(type=scale_type)
                .axis(format='$~s'),  # Use ~s for abbreviated SI units (K, M)
        color=alt.Color('geo_local_area:N') 
                .scale(
                    domain=neighborhoods,
                    range=neighborhood_color_range)
                .legend(None),
        size=alt.Size('total_units:Q',title='Number of Units'),
        tooltip=[
            alt.Tooltip('geo_local_area:N',title='Neighbourhood'),
            alt.Tooltip('total_units:Q',title='Number of Units'),
            alt.Tooltip(x_col, title=x_title, format='$,.0f')  # Keep full precision in tooltip
            ]
    ).properties(
        width=320,
        height=200
    )

    fit_line = alt.Chart(data).transform_regression(
        x_col, y_col
    ).mark_line(color='black').encode(
        x=x_col,
        y=y_col
    )

    chart = (points + fit_line).properties(
        title=title
    )

    return chart
