# app.py
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('resume')
    results = []

    for uploaded_file in uploaded_files:
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            # 💡 FAKE analysis data
            score = random.randint(60, 95)
            sentiment = random.choice(['Positive', 'Neutral', 'Negative'])
            keywords = random.sample([
                'Python', 'Machine Learning', 'Flask', 'CI/CD',
                'Docker', 'AWS', 'Teamwork', 'Leadership'
            ], k=3)

            results.append({
                'filename': filename,
                'score': score,
                'sentiment': sentiment,
                'keywords': keywords
            })

    if not results:
        return "No resumes parsed successfully."

    # Save the results to use in /result route
    with open("parsed_results.json", "w") as f:
        json.dump(results, f)

    return render_template('analyzing.html')

@app.route('/result')
def result():
    if not os.path.exists("parsed_results.json"):
        return "No analysis data found. Please upload resumes first."

    with open("parsed_results.json", "r") as f:
        results = json.load(f)

    # Sort resumes by score (high to low) 🔥
    ranked = sorted(results, key=lambda x: x['score'], reverse=True)

    return render_template('result.html', results=ranked)

if __name__ == '__main__':
    app.run(debug=True)
