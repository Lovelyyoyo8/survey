from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

app = Flask(__name__)

survey_data = pd.DataFrame(columns=['Question', 'Response'])


@app.route('/')
def index():
    return render_template('Survey.html')


@app.route('/submit', methods=['POST'])
def submit():
    global survey_data

    for field in request.form:
        question = field
        response = request.form[field]

        survey_data = survey_data.append({'Question': question, 'Response': response}, ignore_index=True)

    formatted_csv = StringIO()
    survey_data.to_csv(formatted_csv, index=False)
    formatted_csv.seek(0)

    formatted_content = formatted_csv.getvalue().replace('\n', '\n,<span style="font-family:Arial; font-size:14px; text-align:center;">')

    with open('formatted_survey_data.csv', 'w') as f:
        f.write(formatted_content)

    return 'Response recorded successfully!'


@app.route('/chart')
def chart():
    global survey_data

    survey_data = pd.read_csv('formatted_survey_data.csv')

    plt.figure(figsize=(10, 6))
    plt.bar(survey_data['Question'], survey_data['Response'])
    plt.xlabel('Question')
    plt.ylabel('Response')
    plt.title('Survey Responses')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('static/survey_chart.png')

    return render_template('chart.html')


@app.route('/summary')
def summary():
    global survey_data

    summary_stats = survey_data.groupby('Question')['Response'].value_counts().unstack().fillna(0)

    summary_html = summary_stats.to_html(classes='table table-bordered', justify='center')

    return render_template('summary.html', summary_table=summary_html)


@app.route('/analysis')
def analysis():
    global survey_data

    analysis_results = survey_data.groupby('Question')['Response'].mean()

    return render_template('analysis.html', analysis_results=analysis_results)


@app.route('/visualization')
def visualization():
    global survey_data

    response_counts = survey_data['Response'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(response_counts, labels=response_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Survey Response Distribution')
    plt.tight_layout()

    plt.savefig('static/pie_chart.png')

    return render_template('visualization.html')


if __name__ == '__main__':
    app.run(debug=True)
