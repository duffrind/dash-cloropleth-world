'''
Author: Richard Decal

Code adapted from Plotly documentation:
https://plot.ly/python/choropleth-maps/#full-county-choropleths
...and Ashok Lathwal

https://www.kaggle.com/codename007/a-very-extensive-kiva-exploratory-analysis

Dataset:
https://www.kaggle.com/kiva/data-science-for-good-kiva-crowdfunding
'''

import plotly
from kiva_data_loaders import *

# use data load helper I made in kiva_data_loaders.py
loans_data = load_loan_data()

# view loans data with:
# loans_data.head()

# code adapted from https://www.kaggle.com/codename007/a-very-extensive-kiva-exploratory-analysis
countries_funded_amount = loans_data.groupby('country').mean()[
    'funded_amount']\

# If you need to sort that data, you can use the .sort_values(ascending=False)
# method

data = [dict(
    type='choropleth',
    locations=countries_funded_amount.index,  # list of country names
    locationmode='country names',
    # values used to color in countries
    z=countries_funded_amount.values,  # ...and their associated value means
    # text=countries_funded_amount.index,
    # other colorscales are available here:
    # https://plot.ly/ipython-notebooks/color-scales/
    colorscale='Greens',
    marker={'line': {'width': 0.5}},  # width of country boundaries
    colorbar={'autotick': False, 'tickprefix': '$',
              'title': 'Mean funded amount<br>in USD'},  # colorbar title
)]
layout = dict(
    title = 'Mean Kiva Microloan Size<br>Source:\
            <a href="https://www.kaggle.com/kiva/data-science-for-good-kiva-crowdfunding"">\
            Kaggle</a>',
    geo ={'showframe': False}  # hide frame around map
    )
fig = {'data': data, 'layout': layout}

# switch to offline plots to avoid runtime exception
# from not having Plotly account
# ref https://plot.ly/python/getting-started/#initialization-for-offline-plotting
plotly.offline.plot(fig, validate=False, filename='d3-world-map.html')

