from dash.dependencies import Input, Output
from altair import Chart
from dash import dash
from ..components.charts import create_pie_chart, create_bar_chart, create_scatter_plot

def register_chart_callbacks(app, issues, issues_values_joined, property_values):
    # Callback for pie chart
    @app.callback(
        Output('pie-chart', 'srcDoc'),
        Input('region-dropdown', 'value')
    )
    def update_pie_chart(selected_region):
        """Updates and returns HTML of the pie chart based on the selected region."""
        
        aggregated_property_values = issues.groupby('geo_local_area')['total_outstanding'].sum().reset_index()
        return create_pie_chart(aggregated_property_values, selected_region).to_html()

# Updated callback for bar chart
    @app.callback(
        Output('bar-chart', 'spec'),  # Output to the spec property of VegaLite
        Input('region-dropdown', 'value')
    )
    def update_bar_chart(selected_region):
        """Update bar chart spec displaying total outstanding issues by zoning classification."""
        if selected_region:
            filtered_property_values = issues_values_joined[issues_values_joined['geo_local_area'] == selected_region]
            aggregated_property_values = filtered_property_values.groupby('zoning_classification')['total_outstanding'].sum().reset_index()
        else:
            aggregated_property_values = issues_values_joined.groupby('zoning_classification')['total_outstanding'].sum().reset_index()

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
        Input('bar-chart', 'signalData')
    )
    def update_zoning_dropdown(signal_data):
        print(f"[DEBUG] Raw signal data: {signal_data}")  
        
        if signal_data and 'zoning_select' in signal_data:

            selected = signal_data['zoning_select'].get('zoning_classification')
            
            if isinstance(selected, list):
                return selected[0] if selected else None
            elif isinstance(selected, str):
                return selected
        
        return dash.no_update

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
