# key packages:

# standard packages
import numpy as np
import pandas as pd
import datetime
from dateutil import parser

# dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# plotly packages for visualizations
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# janitor for data cleaning
from janitor import clean_names, remove_empty

# yahoo finance for stock info
import yfinance as yf

plotly_figure = dict()

# instantiating the default asset to be displayed upon start-up
present_asset_name = 'VTI'

# sourcing some css to style the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Markdown('''
        ## Asset Time Machine

        Welcome to the Asset Time Machine App! 

        Check out the [documentation here](https://github.com/pmaji/asset-time-machine-app), then select your inputs and click "SUBMIT" to get started.
        '''
        ), 
    # this Div will hold the label and asset-input component:
    html.Div(
        children=[
            html.P("Pick the asset you'd like to explore:"),
            dcc.Input(id='asset-input', type='text', value=present_asset_name)
        ], 
        style=dict(justifyContent='left')
    ),
    # this Div will hold the label and start date picker component:
    html.Div(
        children=[
            html.P("Pick how far back you'd like to explore:"),
            html.P(" "),
            dcc.DatePickerSingle(
                id='ts-start-date-picker-range',
                # this is the date from which we will start our calculations
                date='2000-01-01'
                )
        ], 
        style=dict(justifyContent='left')
    ),
    html.Br(),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div([dcc.Graph(id="asset-graph", figure=plotly_figure)],
            # shouldn't be setting opacity to 0, div should be gone, but plotly messes up horizontal sizing with that
             id="graph-div", style={"opacity": "0"}),
    dcc.Markdown('''
        #### Notes:
        If you have any questions or comments, don't hesitate to [reach out via Twitter](https://twitter.com/ByPaulJ).
        '''
        )
])

@app.callback(Output('graph-div', 'style'), [Input('submit-button', 'n_clicks')])
def display_div(n_clicks):
    if n_clicks > 0:
        return {"opacity": "1"}
    return {"opacity": "0"}

@app.callback(Output('asset-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('asset-input', 'value'),
               State('ts-start-date-picker-range', 'date')])
def update_output(n_clicks, asset, date):
    present_asset_name = asset
    date_today = datetime.datetime.today()
    # formatting today's date appropriately for yf.download() call
    formatted_date_today = date_today.strftime('%Y-%m-%d')
    # setting start date of period for which to pull data
    # need to think about how far back we want to go; code is fast but plotly is a bit slow
    start_date = date
    try:
        initial_data_pull_df = (
            yf.download(
                tickers=asset,
                start=start_date,
                end=formatted_date_today,
                progress=False
            )
            # using janitor to clean the column names
            .pipe(clean_names)
        )
    except:
        asset = present_asset_name
        initial_data_pull_df = (
            yf.download(
                tickers=present_asset_name,
                start=start_date,
                end=formatted_date_today,
                progress=False
            )
            # using janitor to clean the column names
            .pipe(clean_names)
        )

    # renaming the index as well to make it lowercase (sadly janitor doesn't yet catch the index name)
    initial_data_pull_df.index.rename('date', inplace=True)
    initial_data_pull_df.reset_index(level=0, inplace=True)
    cleaned_close_df = initial_data_pull_df.loc[:, ('date', 'adj_close')]
    cleaned_close_df['recent_ath_val'] = cleaned_close_df['adj_close'].cummax()
    recent_ath_date_df = (cleaned_close_df
                          .groupby("recent_ath_val")['date']
                          .first()
                          .reset_index()
                          .rename(columns={"date": "recent_ath_date"})
                          )
    close_and_ath_df = cleaned_close_df.merge(
        recent_ath_date_df, on="recent_ath_val")
    close_and_ath_df['perc_down_from_ath'] = (
        100 * (1 - (close_and_ath_df['adj_close'] /
                    close_and_ath_df['recent_ath_val']))
    )
    close_and_ath_df["days_since_ath"] = close_and_ath_df['date'] - \
        close_and_ath_df['recent_ath_date']

    closing_price_trace = (
        go.Scatter(
            x=close_and_ath_df['date'],
            y=close_and_ath_df['adj_close'],
            line=dict(
                color='rgb(100, 143, 255)',
                width=1.5
            ),
            hoverlabel=dict(namelength=-1),
            opacity=0.75,
            yaxis='y',
            name="Adj. Close Price"
        )
    )

    # building the trace for percent down from ATH values
    pct_down_frm_ath_trace = (
        go.Scatter(
            x=close_and_ath_df['date'],
            y=close_and_ath_df['perc_down_from_ath'],
            line=dict(
                color='rgb(255, 176, 0)',
                width=3
            ),
            hoverlabel=dict(namelength=-1),
            opacity=1,
            yaxis='y2',
            name="% Down from ATH"
        )
    )

    # building the figure itself
    result = {
        'data': [closing_price_trace, pct_down_frm_ath_trace],
        'layout': go.Layout(
            title=dict(
                text=f"Asset Selected: {present_asset_name} <br> Time Series Start: {start_date} <br> Most Recent Date: {close_and_ath_df['date'].iloc[-1].date()}"
            ),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='top',
                xanchor='right',
                y=1.15,
                x=1
            ),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(count=2,
                             label='2y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                type='date',
                title="Date",
                rangeslider=dict(
                    visible=True
                ),
            ),
            yaxis=dict(
                title="Closing Price ($)",
                anchor='x',
                mirror=True,
                side='right',
                showline=True
            ),
            yaxis2=dict(
                title="% Down from ATH",
                anchor='x',
                mirror=True,
                side='left',
                showline=True,
                overlaying='y'
            )
        )
    }

    # in order to get the range slider to not show the full chart...
    # we need to update the range value of the x-axis...
    # here I'm setting it to default to a 1-year lookback from whatever the most recent in the data is
    initial_range = [
        close_and_ath_df['date'].iloc[-1] - pd.DateOffset(years=1), 
        close_and_ath_df['date'].iloc[-1]
    ]
    # updating the xaxis to just cover the initial range we want (defined above)
    result['layout']['xaxis'].update(range=initial_range)

    return result


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
