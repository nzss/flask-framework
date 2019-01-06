from flask import Flask, render_template, request, redirect
import requests
import quandl
#import datetime
#import dateutil.relativedelta
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8



app = Flask(__name__)

@app.route('/') # homepage
def index():
  return render_template('index2.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    ticker_symbol = request.form['ticker_symbol']
    closing_price = request.form['closing_price']
    
    data = get_price(ticker_symbol)
    
    #plot = make_chart(data)

    #script, div = components(plot)
    
    html = make_chart(data)
    return encode_utf8(html)
    #return render_template('chart.html', script = script, div=div)
    #return  #closing_price#ticker_symbol

def get_price(symbol):
	# auth_tok = "kwpSd-EtzUzRsN4QVzYP"
	quandl.ApiConfig.api_key = "kwpSd-EtzUzRsN4QVzYP"
	#today_date = datetime.datetime.today().strftime('%Y-%m-%d')
	#one_month_ago_date = datetime.date.today() - dateutil.relativedelta.relativedelta(months=6)
	#one_month_ago_date = one_month_ago_date.strftime('%Y-%m-%d')
	data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['date', 'close'] },\
	 ticker = [symbol], date = { 'gte': '2018-01-01', 'lte': '2018-02-01' })
	return data


def make_chart(data):
	fig = figure(plot_width=600, plot_height=600)
	fig.line(x = data['date'], y = data['close'])

	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	script, div = components(fig)

	html = render_template('chart.html', plot_script=script, plot_div=div, \
		js_resources=js_resources,
        css_resources=css_resources)

	return html #encode_utf8(html)


@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == '__main__':
  app.run(port=33507)


