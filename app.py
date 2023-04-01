from flask import Flask, request, jsonify
import io
import nltk
import spacy
import pandas as pd
import pdfminer.high_level
from coverLetterGenerator import generateCoverLetter

nltk.download('punkt')
#python -m spacy download en_core_web_sm 
nlp = spacy.load('en_core_web_sm')
data = pd.read_csv("skills.csv")

app = Flask(__name__)
@app.route('/')
def index():
    return "API is working"

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume uploaded'})
    
    file = request.files['resume']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format'})
    
    with io.BytesIO(file.read()) as resume_buffer:
        text = pdfminer.high_level.extract_text(resume_buffer)
    
    doc = nlp(text)
    resumeText={}

    if request.form.get('job_title') != '':
        resumeText['job_title'] = request.form.get('job_title')
        resumeText['job_description']= request.form.get('job_description')
    resumeText['creative'] = True if request.form.get('creative') == 'Yes' else False         
    resumeText['witty'] = True if request.form.get('witty') == 'Yes' else False
    resumeText['name']= request.form.get('name')
    resumeText['skills']= extract_skills(doc)
    resumeText['experience']= extract_experience(text)
    resumeText['education']= extract_education(text)
    resumeText['projects']= extract_projects(text)

    return generateCoverLetter(resumeText)


def extract_skills(text):
    tokens = [token.text for token in text if not token.is_stop]
    skills = list(data.columns.values)
    return list(set([i.capitalize() for i in tokens if i.lower() in skills]))

def extract_experience(resume_text):
    sentences = nltk.sent_tokenize(resume_text)
    experience_sentences = []
    for sent in sentences:
        doc = nlp(sent)
        for ent in doc.ents:
            if ent.label_ == "DATE" or ent.text.strip().endswith("-"):
                experience_sentences.append(sent)
                break
    return " ".join(experience_sentences)

def extract_education(resume_text):
    sentences = nltk.sent_tokenize(resume_text)
    education_sentences = []
    for sent in sentences:
        doc = nlp(sent)
        for ent in doc.ents:
            if "education" in str(ent.label_).lower():
                education_sentences.append(sent)
                break
    return " ".join(education_sentences)

def extract_projects(resume_text):
    sentences = nltk.sent_tokenize(resume_text)
    project_sentences = []
    for sent in sentences:
        doc = nlp(sent)
        for chunk in doc.noun_chunks:
            if "project" in chunk.text.lower():
                project_sentences.append(sent)
                break
    return " ".join(project_sentences)

if __name__ == '__main__':
    app.run()