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


if __name__ == '__main__':
    app.run(debug=True)
