from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN


def inc_dec(open: int, close: int) -> str:
    if close > open:
        return "Increase"
    elif close < open:
        return "Decrease"
    else:
        return "Equal"


def draw_chart(company, start_date, end_date):
    data_frame = data.DataReader(name=company, data_source='yahoo', start=start_date, end=end_date)

    plot = figure(title=company,
                  x_axis_type='datetime',
                  width=1000,
                  height=300,
                  sizing_mode="scale_width")

    plot.grid.grid_line_alpha = 0.9
    plot.xaxis.ticker.desired_num_ticks = 31

    hours_12 = 12 * 60 * 60 * 1000

    data_frame["Status"] = [inc_dec(o, c) for o, c in zip(data_frame["Open"], data_frame["Close"])]
    data_frame["Middle"] = (data_frame.Open + data_frame.Close) / 2
    data_frame["Height"] = abs(data_frame.Open - data_frame.Close)

    plot.segment(data_frame.index, data_frame.High, data_frame.index, data_frame.Low)

    plot.rect(data_frame.index[data_frame.Status == "Increase"],
              data_frame.Middle[data_frame.Status == "Increase"],
              hours_12,
              data_frame.Height[data_frame.Status == "Increase"],
              fill_color="#228B22",
              line_color="black")

    plot.rect(data_frame.index[data_frame.Status == "Decrease"],
              data_frame.Middle[data_frame.Status == "Decrease"],
              hours_12,
              data_frame.Height[data_frame.Status == "Decrease"],
              fill_color="#B22222", line_color="black")

    plot.line(data_frame.index, data_frame.Middle, line_width=2)

    plot_js_script, plot_html = components(plot)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
    return {'plot_js_script': plot_js_script, 'plot_html': plot_html, 'cdn_js': cdn_js, 'cdn_css': cdn_css}


if __name__ == '__main__':
    start_date = datetime.datetime(2020, 9, 1)
    end_date = datetime.datetime(2020, 10, 16)
    company = "AAPL"
    draw_chart(company, start_date, end_date)
