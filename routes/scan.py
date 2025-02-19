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
    
def serializeDocument(doc, similarity=None):
    if not doc:
        return None
    result = {
        'id': doc.id,
        'title': doc.title,
        'content': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content,
        'created_at': doc.created_at.isoformat() if doc.created_at else None,
        'user_id': doc.user_id
    }
    if similarity is not None:
        result['similarity'] = round(similarity * 100, 2) 
    return result


@scanBP.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    documents = Document.query.filter_by(user_id=current_user.id).all()
    credit_requests = CreditRequest.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'user': {
            'username': current_user.username,
            'credits': current_user.credits
        },
        'documents': [{
            'id': doc.id,
            'title': doc.title,
            'created_at': doc.created_at.isoformat()
        } for doc in documents],
        'credit_requests': [{
            'id': req.id,
            'amount': req.amount,
            'status': req.status,
            'created_at': req.created_at.isoformat()
        } for req in credit_requests]
    }), 200
