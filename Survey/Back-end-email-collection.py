from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Create an empty DataFrame to store survey data
survey_data = pd.DataFrame(columns=['Question', 'Response'])


@app.route('/')
def index():
    return render_template('Survey.html')


@app.route('/submit', methods=['POST'])
def submit():
    global survey_data

    # Get user inputs from the form
    for field in request.form:
        question = field
        response = request.form[field]

        # Append data to DataFrame
        survey_data = survey_data.append({'Question': question, 'Response': response}, ignore_index=True)

    # Save data to CSV
    survey_data.to_csv('survey_data.csv', index=False)

    return 'Response recorded successfully!'


@app.route('/chart')
def chart():
    global survey_data

    # Read data from CSV
    survey_data = pd.read_csv('survey_data.csv')

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(survey_data['Question'], survey_data['Response'])
    plt.xlabel('Question')
    plt.ylabel('Response')
    plt.title('Survey Responses')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart as an image file
    plt.savefig('static/survey_chart.png')

    return render_template('chart.html')


if __name__ == '__main__':
    app.run(debug=True)
