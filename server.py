from flask import Flask, render_template, request
from stick_chart import draw_chart
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/chart/')
def chart():
    return render_template('chart.html',
                           plot_js_script='',
                           plot_html='',
                           cdn_js='',
                           cdn_css='',
                           company=''
                           )


@app.route('/chart/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        form_data = request.form.to_dict()

        start_date = form_data['start_date']
        end_date = form_data['end_date']
        company = form_data['company']

        resourses = draw_chart(company, start_date, end_date)
        return render_template('chart.html',
                               plot_js_script=resourses['plot_js_script'],
                               plot_html=resourses['plot_html'],
                               cdn_js=resourses['cdn_js'],
                               cdn_css=resourses['cdn_css'],
                               company=company)
    else:
        return 'Something wrong'


if __name__ == '__main__':
    app.run(port=8000, debug=True)
