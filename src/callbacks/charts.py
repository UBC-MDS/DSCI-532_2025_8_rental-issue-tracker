from dash.dependencies import Input, Output
from altair import Chart
from dash import dash
from ..components.charts import create_pie_chart, create_bar_chart, create_scatter_plot

def register_chart_callbacks(app, issues, issues_values_joined, property_values):
    # Callback for pie chart
    @app.callback(
        Output('pie-chart', 'spec'),
        Input('region-dropdown', 'value')
    )
    def update_pie_chart(selected_region):
        """Updates and returns HTML of the pie chart based on the selected region."""
        
        aggregated_property_values = issues.groupby('geo_local_area')['total_outstanding'].sum().reset_index()
        return create_pie_chart(aggregated_property_values, selected_region)

    # Updated callback for bar chart
    @app.callback(
        Output('bar-chart', 'spec'),  # Output to the spec property of VegaLite
        Input('region-dropdown', 'value'),
        Input('zoning-dropdown', 'value')  # Add zoning-dropdown as an input
    )
    def update_bar_chart(selected_region, selected_zone):
        """Update bar chart spec displaying total outstanding issues by zoning classification."""
        if selected_region:
            filtered_property_values = issues_values_joined[issues_values_joined['geo_local_area'] == selected_region]
        else:
            filtered_property_values = issues_values_joined

        # If zoning dropdown is cleared (None), show all bars
        if selected_zone is None or selected_zone == "":
            aggregated_property_values = filtered_property_values.groupby('zoning_classification')['total_outstanding'].sum().reset_index()
        else:
            aggregated_property_values = filtered_property_values[
                filtered_property_values['zoning_classification'] == selected_zone
            ].groupby('zoning_classification')['total_outstanding'].sum().reset_index()

        spec = create_bar_chart(
            data=aggregated_property_values,
            x_col='total_outstanding',
            y_col='zoning_classification',
            title='Total Outstanding Issues by Zoning Classification',
            x_title='Total Outstanding Issues',
            y_title='Zoning Classification'
        )
        return spec

    # New callback to update zoning dropdown
    @app.callback(
        Output('zoning-dropdown', 'value'),
        Output('region-dropdown', 'value'),
        Input('pie-chart', 'signalData'),
        Input('bar-chart', 'signalData'),
        prevent_initial_call=True
    )
    def update_dropdown(pie_signal_data, bar_signal_data):
        print(f"[DEBUG] Pie chart signal data: {pie_signal_data}")
        print(f"[DEBUG] Bar chart signal data: {bar_signal_data}")
        
        # Initialize with no_update for both outputs
        zoning_value = dash.no_update
        region_value = dash.no_update
        
        # Check bar chart signals for zoning selection
        if bar_signal_data and 'zoning_select' in bar_signal_data:
            selected = bar_signal_data['zoning_select'].get('zoning_classification')
            
            if isinstance(selected, list):
                zoning_value = selected[0] if selected else None
            elif isinstance(selected, str):
                zoning_value = selected
        
        # Check pie chart signals for region selection
        if pie_signal_data and 'region_select' in pie_signal_data:
            selected = pie_signal_data['region_select'].get('geo_local_area')
            
            if isinstance(selected, list):
                region_value = selected[0] if selected else None
            elif isinstance(selected, str):
                region_value = selected
        
        
        # Return a tuple with values for both outputs
        return zoning_value, region_value
    
    
    # Callback for scatter plot
    @app.callback(
        Output('scatter-plot', 'srcDoc'),
        Input('region-dropdown', 'value'),
        Input('scale-radio','value')
    )
    def update_scatter_plot(selected_region,selected_scale):
        """Update the scatter plot based on the selected region."""

        if selected_region:
            filtered_property_values = property_values[property_values['geo_local_area'] == selected_region]
        else:
            filtered_property_values = property_values

        chart = create_scatter_plot(
            data=filtered_property_values,
            x_col='current_land_value',
            y_col='total_outstanding',
            title='Property Prices vs Outstanding Issues',
            scale_type=selected_scale,
            x_title='Property Prices',
            y_title='Outstanding Issues',  
        )
        return chart.to_html()
    
    # callback for toggle button
    @app.callback(
        Output('na-button',"color"),
        Input("na-button", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_button(n_clicks):
        if n_clicks % 2 == 1:
            return "success"
        else:
            return "secondary"