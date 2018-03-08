import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
#from kiva_data_loaders import *

# Import your dataframe from a csv with pandas


# use data load helper I made in kiva_data_loaders.py
df = pd.read_csv("data/kiva_loans.csv")

# converting dates from string to DateTime objects gives nice tools
df['date'] = pd.to_datetime(df['date'])

# for example, we can turn the full date into just a year
df['year'] = df.date.dt.to_period("Y")
# then convert it to integers so you can do list comprehensions later
# astype(int) expects a strings, so we need to go Period -> str -> int
# we want ints so we can find the min, max, etc later
df['year'] = df.year.astype(str).astype(int)

# This is our features of interest
# I grouped by year first so that I can then filter by year with just
# df.loc[2014]
countries_funded_amount = df.groupby(['year', 'country']).size()

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
        value=df['year'].min(),  # The default value of the slider
        step=None,
        # the values have to be the same dtype for filtering to work later
        marks={str(year): year for year in df['year'].unique()}
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

    # snag: using .groupby() with more than one feature caused the datatype
    # to be Pandas.Series instead of Pandas.DataFrame. So, we couldn't just do
    # countries_funded_amount[countries_funded_amount['year'] == selected_year]
    one_year_data = countries_funded_amount.loc[selected_year]

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
        locations=one_year_data.index.get_level_values('country'),  # list of country names
        # other option is USA-states
        locationmode='country names',
        # sets the color values
        z=one_year_data.values,  # ...and their associated values
        # sets the text element associated w each position
        # text=countries_funded_amount.index,
        # other colorscales are available here:
        # https://plot.ly/ipython-notebooks/color-scales/
        colorscale='Greens',
        # by default, low numbers are dark and high numbers are white
        reversescale=True,
        # set upper bound of color domain (see also zmin)
        #zmax=30000,
        # if you want to use zmin or zmax don't forget to disable zauto
        #zauto=False,
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