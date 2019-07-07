import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd
import datetime

# for data cleaning
from janitor import clean_names, remove_empty

import fix_yahoo_finance as yf

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode(connected=False)

plotly_figure = dict()

present_asset_name = 'FNMA'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='security-input', type='text', value='FNMA'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div([dcc.Graph(id="asset-graph",figure=plotly_figure)],id="graph-div",style={"opacity":"0"})
	#shouldn't be setting opacity to 0, div should be gone, but plotly messes up horizontal sizing with that
])

@app.callback(Output('graph-div','style'),[Input('submit-button','n_clicks')])
def display_div(n_clicks):
	if n_clicks > 0:
		return {"opacity":"1"}
	return {"opacity":"0"}

@app.callback(Output('asset-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('security-input', 'value')])
def update_output(n_clicks, security):
	present_asset_name = security
	date_today = datetime.datetime.today()
	# formatting today's date appropriately for yf.download() call
	formatted_date_today = date_today.strftime('%Y-%m-%d')
	# setting start date of period for which to pull data
	# need to think about how far back we want to go; code is fast but plotly is a bit slow
	start_date = '2000-01-01'
	try:
		print("hihi")
		initial_data_pull_df = (
			yf.download(
				tickers=security,
				start=start_date,
				end=formatted_date_today,
				progress=False
			)
		# using janitor to clean the column names
		.pipe(clean_names)
		)
	except:
		print("hi")
		security = "FNMA"
		initial_data_pull_df = (
			yf.download(
				tickers="FNMA",
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
	cleaned_close_df = initial_data_pull_df.loc[:,('date','adj_close')]
	cleaned_close_df['recent_ath_val'] = cleaned_close_df['adj_close'].cummax()
	recent_ath_date_df = (cleaned_close_df
                      .groupby("recent_ath_val")['date']
                      .first()
                      .reset_index()
                      .rename(columns={"date":"recent_ath_date"})
                     )
	close_and_ath_df = cleaned_close_df.merge(recent_ath_date_df,on="recent_ath_val")
	close_and_ath_df['perc_down_from_ath'] = (
		100 * (1 - (close_and_ath_df['adj_close'] / close_and_ath_df['recent_ath_val']))
	)
	close_and_ath_df["days_since_ath"] = close_and_ath_df['date'] - close_and_ath_df['recent_ath_date']
	
	closing_price_trace = (
    go.Scatter(
        x = close_and_ath_df['date'],
        y = close_and_ath_df['adj_close'],
        line = dict(
            color = 'rgb(100, 143, 255)',
            width = 1.5
        ),
        hoverlabel = dict(namelength = -1),
        opacity = 0.75,
        yaxis = 'y',
        name = "Adj. Close Price"
    )
)

	# building the trace for percent down from ATH values
	pct_down_frm_ath_trace = (
		go.Scatter(
			x = close_and_ath_df['date'],
			y = close_and_ath_df['perc_down_from_ath'],
			line = dict(
				color = 'rgb(255, 176, 0)',
				width = 3
			),
			hoverlabel = dict(namelength = -1),
			opacity = 1,
			yaxis = 'y2',
			name = "% Down from ATH"
		)
	)

	# building the figure itself
	result = {
        'data' : [closing_price_trace, pct_down_frm_ath_trace],
        'layout': go.Layout(
            title = dict(
                text = f"Asset Selected: {present_asset_name}  |  Time Series Start: {start_date}"
            ),
            showlegend = True,
            legend = dict(
                orientation = 'h',
                yanchor = 'top',
                xanchor = 'right',
                y=1.15,
                x=1
            ),
            xaxis = dict(
                rangeselector = dict(
                    buttons = list([
                        dict(count = 1,
                            label = '1m',
                            step = 'month',
                            stepmode = 'backward'),
                        dict(count = 6,
                            label = '6m',
                            step = 'month',
                            stepmode = 'backward'),
                        dict(count = 1,
                            label = 'YTD',
                            step = 'year',
                            stepmode = 'todate'),
                        dict(count = 1,
                            label = '1y',
                            step = 'year',
                            stepmode = 'backward'),
                        dict(count = 2,
                            label = '2y',
                            step = 'year',
                            stepmode = 'backward'),
                        dict(step = 'all')
                    ])
                ),
                type = 'date',
                title = "Date",
                rangeslider = dict(
                    visible = True
                ),
            ),
            yaxis = dict(
                title = "Closing Price ($)",
                anchor = 'x',
                mirror = True,
                side = 'right',
                showline = True
            ),
            yaxis2 = dict(
                title = "% Down from ATH",
                anchor = 'x',
                mirror = True,
                side = 'left',
                showline = True,
                overlaying ='y'
            )
        )
    }
	return result


if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')