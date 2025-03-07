from dash.dependencies import Input, Output
from altair import Chart
from components.charts import create_pie_chart, create_bar_chart, create_scatter_plot

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

    # Callback for bar chart (Global view)
    @app.callback(
        Output('bar-chart', 'srcDoc'),
        Input('region-dropdown', 'value')
    )
    def update_bar_chart(selected_region):
        """Update bar chart displaying total outstanding issues by zoning classification for a selected region."""

        if selected_region:
            filtered_property_values = issues_values_joined[issues_values_joined['geo_local_area'] == selected_region]
            aggregated_property_values = filtered_property_values.groupby('zoning_classification')['total_outstanding'].sum().reset_index()
        else:
            aggregated_property_values = issues_values_joined.groupby('zoning_classification')['total_outstanding'].sum().reset_index()

        chart = create_bar_chart(
            data=aggregated_property_values,
            x_col='total_outstanding',
            y_col='zoning_classification',
            title='Total Outstanding Issues by Zoning Classification',
            x_title='Total Outstanding Issues',
            y_title='Zoning Classification'
        )
        return chart.to_html()

    # Callback for scatter plot
    @app.callback(
        Output('scatter-plot', 'srcDoc'),
        Input('region-dropdown', 'value')
    )
    def update_scatter_plot(selected_region):
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
            x_title='Property Prices',
            y_title='Outstanding Issues'
        )
        return chart.to_html()
