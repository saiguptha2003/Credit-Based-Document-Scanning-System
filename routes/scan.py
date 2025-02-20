from flask import Blueprint, jsonify, request
from models import Document, CreditRequest,User
from utils import token_required
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
    pdf_reader = pypdf.PdfReader(file)
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
@token_required
def dashboard(current_user):
    try:
        documents = Document.query.filter_by(user_id=current_user.id).all()
        credit_requests = CreditRequest.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'user': {
                'username': current_user.username,
                'email': current_user.email,
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
    except Exception as e:
        return jsonify({'error': f'Error retrieving dashboard data: {str(e)}'}), 500

@scanBP.route('/scan-document', methods=['POST'])
@token_required
def scanDocument(current_user):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowedFile(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload PDF or TXT files only'}), 400
        
        try:
            if file.filename.endswith('.pdf'):
                content = readPDFContent(file)
            else:  
                content = file.read().decode('utf-8')
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
        
        if not content:
            return jsonify({'error': 'File is empty or could not be read'}), 400
        
        try:
            new_doc = Document(
                title=secure_filename(file.filename),
                content=content,
                user_id=current_user.id,
                created_at=datetime.now(timezone.utc)
            )

            user = User.query.get(current_user.id)
            if user is None:
                return jsonify({'error': 'User not found'}), 404
            
            if user.credits <= 0:
                return jsonify({'error': 'Insufficient credits. Please request more credits.'}), 403           
            
            db.session.add(new_doc)
            db.session.commit()
            db.session.refresh(new_doc)
            similar_docs = findSimilarDocuments(content,current_user)
            return jsonify({
                'message': 'Document scanned successfully',
                'document': serializeDocument(new_doc),
                'similar_documents': similar_docs
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@scanBP.route('/request-credits', methods=['POST'])
@token_required
def requestCredits(current_user):
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        if not amount or amount <= 0:
            return jsonify({'error': 'Invalid credit amount'}), 400
            
        creditRequest = CreditRequest(
            user_id=current_user.id,
            amount=amount,
            created_at=datetime.now(timezone.utc)
        )
        
        db.session.add(creditRequest)
        db.session.commit()
        
        return jsonify({
            'message': 'Credit request submitted',
            'request': {
                'id': creditRequest.id,
                'amount': creditRequest.amount,
                'status': creditRequest.status,
                'created_at': creditRequest.created_at.isoformat()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error processing credit request: {str(e)}'}), 500


def findSimilarDocuments(content, current_user, threshold=SIMILARITY_THRESHOLD):
    try:
        similarDocs = []
        allDocs = Document.query.filter_by(user_id=current_user.id).all()
        for doc in allDocs:
            similarity = calculateSimilarity(content, doc.content)
            if similarity > threshold:
                similarDocs.append((doc, similarity))
        similarDocs.sort(key=lambda x: x[1], reverse=True)
        user = User.query.get(current_user.id)
        if user.credits <= 0:
            return jsonify({'error': 'Insufficient credits. Please request more credits.'}), 403
        user.credits -= 1
        db.session.add(user)
        db.session.commit()        
        return [
            serializeDocument(doc, similarity)
            for doc, similarity in similarDocs
            if doc.id != Document.query.order_by(Document.id.desc()).first().id  # Exclude the current document
        ]
    except Exception as e:
        print(f"Error in findSimilarDocuments: {str(e)}")
        return []





