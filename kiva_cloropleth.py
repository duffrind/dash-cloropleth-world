'''
Author: Richard Decal

Code adapted from Plotly documentation:
https://plot.ly/python/choropleth-maps/#full-county-choropleths
...and Ashok Lathwal

https://www.kaggle.com/codename007/a-very-extensive-kiva-exploratory-analysis

Dataset:
https://www.kaggle.com/kiva/data-science-for-good-kiva-crowdfunding
'''

import plotly.plotly as py
import plotly
import pandas as pd
from kiva_data_loaders import *

loans_data, mpi_location_data, loan_theme_ids_data, loan_themes_by_region_data = load_all()

# view loans data with:
# loans_data.head()

# code adapted from https://www.kaggle.com/codename007/a-very-extensive-kiva-exploratory-analysis
countries_funded_amount = loans_data.groupby('country').mean()['funded_amount'].sort_values(ascending = False)

data = [dict(
        type='choropleth',
        locations= countries_funded_amount.index,
        locationmode='country names',
        z=countries_funded_amount.values,
        text=countries_funded_amount.index,
        colorscale='Red',
        marker=dict(line=dict(width=0.7)),
        colorbar=dict(autotick=False, tickprefix='', title='Top Countries with funded_amount(Mean value)'),
)]
layout = dict(title = 'Top Countries with funded_amount(Dollar value of loan funded on Kiva.org)',)
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, validate=False, filename='d3-world-map.html')


# data = [ dict(
#         type = 'choropleth',
#         locations = df['CODE'],
#         z = df['GDP (BILLIONS)'],
#         text = df['COUNTRY'],
#         colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
#             [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
#         autocolorscale = False,
#         reversescale = True,
#         marker = dict(
#             line = dict (
#                 color = 'rgb(180,180,180)',
#                 width = 0.5
#             ) ),
#         colorbar = dict(
#             autotick = False,
#             tickprefix = '$',
#             title = 'GDP<br>Billions US$'),
#       ) ]
#
# layout = dict(
#     title = '2014 Global GDP<br>Source:\
#             <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
#             CIA World Factbook</a>',
#     geo = dict(
#         showframe = False,
#         showcoastlines = False,
#         projection = dict(
#             type = 'Mercator'
#         )
#     )
# )
#
# fig = dict(data=data, layout=layout)
#
# # switch to offline plots
# # ref https://plot.ly/python/getting-started/#initialization-for-offline-plotting
# plotly.offline.plot(fig, validate=False, filename='d3-world-map.html')