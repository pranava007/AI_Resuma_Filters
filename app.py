from flask import Flask, render_template, request
import os
import nltk
from nltk.corpus import stopwords



app = Flask(__name__)

def compare_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        content1 = set(f1.read().split())
        content2 = set(f2.read().split())
        matching_keywords = content1.intersection(content2)
        return matching_keywords

nltk.download('stopwords')
  
def remove_articles(words):
    articles = set(stopwords.words('english'))
    return [word for word in words if word.lower() not in articles]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    file_to_compare = request.files['file_to_compare']
    files = request.files.getlist('files[]')

    # Save uploaded files to server
    file_to_compare_path = os.path.join('uploads', file_to_compare.filename)
    file_to_compare.save(file_to_compare_path)

    result = {}
    for file in files:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        matching_keywords = compare_files(file_to_compare_path, file_path)
        
        matching_keywords  = remove_articles(   matching_keywords )

        result[file.filename] = matching_keywords

    return render_template('result.html', result=result)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
