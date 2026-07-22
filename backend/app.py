from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import json
import os
import sqlite3
from database import Database

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SECRET_KEY'] = 'smartplace-pro-secret-key-2024'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-2024'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app, supports_credentials=True)
jwt = JWTManager(app)

db = Database()

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    user_id = db.create_user(
        data.get('username'),
        data.get('email'),
        data.get('password'),
        data.get('full_name')
    )
    
    if user_id:
        access_token = create_access_token(identity=user_id)
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'username': data.get('username'),
                'email': data.get('email'),
                'full_name': data.get('full_name')
            }
        }), 201
    else:
        return jsonify({
            'success': False,
            'message': 'Username or email already exists'
        }), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = db.authenticate_user(data.get('username'), data.get('password'))
    
    if user:
        access_token = create_access_token(identity=user['id'])
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': user
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401

# Profile routes
@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    profile = db.get_user_profile(user_id)
    
    if profile:
        return jsonify(profile), 200
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.json
    success = db.update_user_profile(user_id, data)
    
    if success:
        return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
    return jsonify({'error': 'Update failed'}), 400

# Aptitude routes
@app.route('/api/aptitude/submit', methods=['POST'])
@jwt_required()
def submit_aptitude():
    user_id = get_jwt_identity()
    data = request.json
    
    success = db.save_aptitude_result(
        user_id,
        data.get('test_type'),
        data.get('score'),
        data.get('total_questions'),
        data.get('correct_answers'),
        data.get('answers'),
        data.get('time_taken')
    )
    
    if success:
        db.log_activity(user_id, 'aptitude_test', f'Completed {data.get("test_type")} test with score {data.get("score")}%')
        return jsonify({'success': True, 'message': 'Test submitted successfully'}), 200
    return jsonify({'error': 'Submission failed'}), 400

# Coding routes
@app.route('/api/coding/challenges', methods=['GET'])
def get_challenges():
    difficulty = request.args.get('difficulty')
    challenges = db.get_coding_challenges(difficulty)
    return jsonify({'challenges': challenges}), 200

@app.route('/api/coding/submit', methods=['POST'])
@jwt_required()
def submit_coding():
    user_id = get_jwt_identity()
    data = request.json
    
    success = db.save_coding_submission(
        user_id,
        data.get('challenge_id'),
        data.get('challenge_title'),
        data.get('language'),
        data.get('code'),
        data.get('status'),
        data.get('score')
    )
    
    if success:
        db.log_activity(user_id, 'coding_submission', f'Submitted solution for {data.get("challenge_title")}')
        return jsonify({'success': True, 'message': 'Code submitted successfully'}), 200
    return jsonify({'error': 'Submission failed'}), 400

# Interview routes
@app.route('/api/interview/submit', methods=['POST'])
@jwt_required()
def submit_interview():
    user_id = get_jwt_identity()
    data = request.json
    
    success = db.save_interview_response(
        user_id,
        data.get('question'),
        data.get('response'),
        data.get('feedback'),
        data.get('score')
    )
    
    if success:
        db.log_activity(user_id, 'interview_practice', 'Completed interview question')
        return jsonify({'success': True, 'message': 'Interview response saved'}), 200
    return jsonify({'error': 'Submission failed'}), 400

# Resume routes
@app.route('/api/resume/analyze', methods=['POST'])
@jwt_required()
def analyze_resume():
    user_id = get_jwt_identity()
    data = request.json
    resume_text = data.get('resume_text')
    
    # AI analysis
    keywords = ['python', 'javascript', 'react', 'node', 'sql', 'aws', 'machine learning', 'data structures']
    found_keywords = [kw for kw in keywords if kw.lower() in resume_text.lower()]
    ats_score = min(100, len(found_keywords) * 12 + 40)
    
    suggestions = [
        "Add more specific technical keywords",
        "Quantify your achievements with numbers",
        "Use action verbs to start bullet points",
        "Include relevant certifications"
    ]
    
    success = db.save_resume_analysis(user_id, resume_text, ats_score, found_keywords, suggestions)
    
    if success:
        db.log_activity(user_id, 'resume_analysis', f'Resume analyzed with score {ats_score}%')
        return jsonify({
            'success': True,
            'analysis': {
                'ats_score': ats_score,
                'keywords_found': found_keywords,
                'suggestions': suggestions
            }
        }), 200
    return jsonify({'error': 'Analysis failed'}), 400

# Dashboard routes
@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    stats = db.get_user_stats(user_id)
    return jsonify(stats), 200

@app.route('/api/dashboard/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    history = db.get_aptitude_history(user_id)
    return jsonify({'history': history}), 200


@app.route('/datatable')
def serve_datatable():
    return send_from_directory('../frontend', 'datatable.html')

@app.route('/api/view_data')
def view_data():
    """View all database tables"""
    conn = db.get_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    data = {}
    for table in tables:
        table_name = table['name']
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        data[table_name] = [dict(row) for row in rows]
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)