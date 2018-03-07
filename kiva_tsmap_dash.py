import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from kiva_data_loaders import *

# Import your dataframe from a csv with pandas


# use data load helper I made in kiva_data_loaders.py
df = load_loan_data()
df['date'] = pd.to_datetime(df['date'])
df['year'] = df.date.dt.to_period("Y")
countries_funded_amount = df.groupby('country').size()

# Create a Dash object instance
app = dash.Dash()

# The layout attribute of the Dash object, app
# is where you include the elements you want to appear in the
# dashboard. Here, dcc.Graph and dcc.Slider are separate
# graph objects. Most of Graph's features are defined
# inside the function update_figure, but we set the id
# here so we can reference it inside update_figure
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    # TODO select col
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),  # The default value of the slider.
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])


# Notice the Input and Outputs in this wrapper correspond to
# the ids of the components in app.layout above.
@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    """Define how the graph is to be updated based on the slider."""

    # Depending on the year selected on the slider, filter the db
    # by that year.
    filtered_df = countries_funded_amount[countries_funded_amount.year == selected_year]

    # The go.Scatter graph object go.Scatter contains information
    # about points to put on a scatter plot. Here, we create one
    # Scatter object for each continent by filtering, and append each
    # Scatter object to a list. The whole list of Scatterplots will
    # appear on one graph--'graph-with-slider'
    traces = []
    # for i in filtered_df.continent.unique():
    #     df_by_continent = filtered_df[filtered_df['continent'] == i]
    #     """The mode controls the appearance of the points of data. Try changing
    #     mode below to 'lines' and see the change. A complete list of modes is
    #     available at https://plot.ly/python/reference/#scatter"""
    #     traces.append(go.Scatter(  # Scatter is just one plotly.graph_obj (.go)
    #         x=df_by_continent['gdpPercap'],   # graph type. Try changing
    #         y=df_by_continent['lifeExp'],     # to go.Scatter3d.
    #         text=df_by_continent['country'],  # (It won't look great, here.)
    #         mode='markers',
    #         opacity=0.7,
    #         marker={
    #             'size': 15,
    #             'line': {'width': 0.5, 'color': 'white'}
    #         },
    #         name=i
    #     ))
    data = [dict(
        type='choropleth',
        locations=filtered_df.index,  # list of country names
        # other option is USA-states
        locationmode='country names',
        # sets the color values
        z=filtered_df.values,  # ...and their associated value means
        # sets the text element associated w each position
        # text=countries_funded_amount.index,
        # other colorscales are available here:
        # https://plot.ly/ipython-notebooks/color-scales/
        colorscale='Greens',
        # by default, low numbers are dark and high numbers are white
        reversescale=True,
        # set upper bound of color domain (see also zmin)
        zmax=30000,
        # if you want to use zmin or zmax don't forget to disable zauto
        zauto=False,
        marker={'line': {'width': 0.5}},  # width of country boundaries
        colorbar={'autotick': True,
                  'tickprefix': '',  # could be useful if plotting $ values
                  'title': 'Mean funded amount<br>in USD'},  # colorbar title
    )]
    layout = dict(
        title='Mean Kiva Microloan Size<br>Source:\
                <a href="https://www.kaggle.com/kiva/data-science-for-good-kiva-crowdfunding"">\
                Kaggle</a>',
        geo={'showframe': False}  # hide frame around map
    )
    fig = {'data': data, 'layout': layout}
    return fig

    # return {
    #     'data': traces,
    #     'layout': go.Layout(
    #         xaxis={'type': 'log', 'title': 'GDP Per Capita'},
    #         yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
    #         margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #         legend={'x': 0, 'y': 1},
    #         hovermode='closest'  # Try commenting out this line and seeing what
    #     )                        # changes.
    # }


if __name__ == '__main__':
    app.run_server()