from datetime import datetime
import json

class User:
    def __init__(self, id=None, username=None, email=None, full_name=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AptitudeResult:
    def __init__(self, user_id=None, test_type=None, score=None, total_questions=None, 
                 correct_answers=None, answers=None, time_taken=None):
        self.user_id = user_id
        self.test_type = test_type
        self.score = score
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.answers = answers or []
        self.time_taken = time_taken
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'test_type': self.test_type,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'answers': self.answers,
            'time_taken': self.time_taken,
            'created_at': self.created_at.isoformat()
        }

class CodingSubmission:
    def __init__(self, user_id=None, challenge_id=None, challenge_title=None, 
                 language=None, code=None, status=None, score=None):
        self.user_id = user_id
        self.challenge_id = challenge_id
        self.challenge_title = challenge_title
        self.language = language
        self.code = code
        self.status = status
        self.score = score
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'challenge_title': self.challenge_title,
            'language': self.language,
            'code': self.code,
            'status': self.status,
            'score': self.score,
            'created_at': self.created_at.isoformat()
        }

class InterviewResponse:
    def __init__(self, user_id=None, question=None, response=None, feedback=None, score=None):
        self.user_id = user_id
        self.question = question
        self.response = response
        self.feedback = feedback
        self.score = score
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'question': self.question,
            'response': self.response,
            'feedback': self.feedback,
            'score': self.score,
            'created_at': self.created_at.isoformat()
        }

class ResumeAnalysis:
    def __init__(self, user_id=None, resume_text=None, ats_score=None, keywords=None, suggestions=None):
        self.user_id = user_id
        self.resume_text = resume_text
        self.ats_score = ats_score
        self.keywords = keywords or []
        self.suggestions = suggestions or []
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'resume_text': self.resume_text[:500],  # Truncate for display
            'ats_score': self.ats_score,
            'keywords': self.keywords,
            'suggestions': self.suggestions,
            'created_at': self.created_at.isoformat()
        }