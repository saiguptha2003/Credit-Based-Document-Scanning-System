from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Document, CreditRequest,User
from utils import db
import difflib
from werkzeug.utils import secure_filename
import os
import pypdf
import io
from datetime import datetime, timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

scanBP = Blueprint('scanBP', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'txt'}
SIMILARITY_THRESHOLD = 0.3

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def readPDFContent(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



def calculateSimilarity(text1, text2):
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {str(e)}")
        return 0.0