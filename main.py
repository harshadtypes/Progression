from flask import Flask, render_template, redirect, url_for, request
import time
import os
import shutil
import csv

import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.csv'):
        file.save(os.path.join('static/data_prime', 'dataframe.csv'))
        csv_file = 'static/data_prime/dataframe.csv'
        data = []

        # Read the CSV file and store its contents in a list
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

        # Pass the data to the template
        return render_template('post_upload.html', data=data)
    else:
        return "Invalid file format. Please upload a CSV file.", 400


@app.route('/uploadf1', methods=['POST'])
def uploadf_file():
    shutil.copy('static/datasets/Position_Salaries.csv', 'static/data_prime/')
    os.rename('static/data_prime/Position_Salaries.csv',
              'static/data_prime/dataframe.csv')

    csv_file = 'static/data_prime/dataframe.csv'
    data = []

    # Read the CSV file and store its contents in a list
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    # Pass the data to the template
    return render_template('post_uploadf.html', data=data)


@app.route('/uploadf2', methods=['POST'])
def uploadf_file2():
    shutil.copy('static/datasets/50_Startups.csv', 'static/data_prime/')
    os.rename('static/data_prime/50_Startups.csv',
              'static/data_prime/dataframe.csv')

    csv_file = 'static/data_prime/dataframe.csv'
    data = []

    # Read the CSV file and store its contents in a list
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    # Pass the data to the template
    return render_template('post_uploadf.html', data=data)


@app.route('/submit', methods=['POST'])
def submit():
    # Run the external Python file
    subprocess.run(['python', 'regressor.py'])
    time.sleep(1)
    # Redirect to the page that displays the image
    return redirect(url_for('show_image'))


@app.route('/show_image')
def show_image():
    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
