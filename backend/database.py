import sqlite3
import os
from datetime import datetime
import hashlib
import json
import threading

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '../data/smartplace.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.local = threading.local()
        self.init_database()
    
    def get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.connection.row_factory = sqlite3.Row
        return self.local.connection
    
    def get_cursor(self):
        """Get cursor from thread-local connection"""
        return self.get_connection().cursor()
    
    def close(self):
        """Close thread-local connection if exists"""
        if hasattr(self.local, 'connection'):
            self.local.connection.close()
            del self.local.connection
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                phone TEXT,
                college TEXT,
                course TEXT,
                year INTEGER,
                skills TEXT,
                bio TEXT,
                avatar TEXT DEFAULT 'fa-user-graduate',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Aptitude test results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aptitude_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                test_type TEXT,
                score INTEGER,
                total_questions INTEGER,
                correct_answers INTEGER,
                answers TEXT,
                time_taken INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Coding submissions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coding_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                challenge_id INTEGER,
                challenge_title TEXT,
                language TEXT,
                code TEXT,
                status TEXT,
                score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Interview responses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                response TEXT,
                feedback TEXT,
                score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Resume analyses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                resume_text TEXT,
                ats_score INTEGER,
                keywords TEXT,
                suggestions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Activity logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity_type TEXT,
                activity_details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Coding challenges
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coding_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                difficulty TEXT,
                category TEXT,
                test_cases TEXT,
                starter_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Insert sample coding challenges"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if challenges already exist
        cursor.execute("SELECT COUNT(*) FROM coding_challenges")
        count = cursor.fetchone()[0]
        
        if count == 0:
            challenges = [
                ('Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.', 'Easy', 'Array', '[{"input": "[2,7,11,15], 9", "output": "[0,1]"}]', 'def two_sum(nums, target):\n    # Write your code here\n    pass'),
                ('Reverse String', 'Write a function that reverses a string.', 'Easy', 'String', '[{"input": "hello", "output": "olleh"}]', 'def reverse_string(s):\n    # Write your code here\n    pass'),
                ('Fibonacci Series', 'Generate the first n numbers in the Fibonacci sequence.', 'Medium', 'Recursion', '[{"input": "5", "output": "[0,1,1,2,3]"}]', 'def fibonacci(n):\n    # Write your code here\n    pass'),
                ('Valid Parentheses', 'Given a string containing parentheses, determine if it is valid.', 'Medium', 'Stack', '[{"input": "()[]{}", "output": "true"}]', 'def is_valid(s):\n    # Write your code here\n    pass'),
                ('Merge Sort', 'Implement merge sort algorithm.', 'Hard', 'Sorting', '[{"input": "[3,1,4,1,5]", "output": "[1,1,3,4,5]"}]', 'def merge_sort(arr):\n    # Write your code here\n    pass'),
            ]
            
            for challenge in challenges:
                cursor.execute('''
                    INSERT INTO coding_challenges (title, description, difficulty, category, test_cases, starter_code)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', challenge)
            
            conn.commit()
    
    def create_user(self, username, email, password, full_name):
        """Create a new user"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, hashed_password, full_name))
            user_id = cursor.lastrowid
            
            # Create default profile
            cursor.execute('''
                INSERT INTO user_profiles (user_id)
                VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def authenticate_user(self, username, password):
        """Authenticate user"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email, full_name FROM users 
            WHERE username = ? AND password = ? AND is_active = 1
        ''', (username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user['id'],))
            conn.commit()
            return dict(user)
        
        return None
    
    def get_user_profile(self, user_id):
        """Get user profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.username, u.email, u.full_name, u.created_at, u.last_login,
                   up.phone, up.college, up.course, up.year, up.skills, up.bio, up.avatar
            FROM users u
            LEFT JOIN user_profiles up ON u.id = up.user_id
            WHERE u.id = ?
        ''', (user_id,))
        profile = cursor.fetchone()
        return dict(profile) if profile else None
    
    def update_user_profile(self, user_id, data):
        """Update user profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET full_name = ?, email = ?
            WHERE id = ?
        ''', (data.get('full_name'), data.get('email'), user_id))
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_profiles (user_id, phone, college, course, year, skills, bio, avatar)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data.get('phone'), data.get('college'), data.get('course'), 
              data.get('year'), data.get('skills'), data.get('bio'), data.get('avatar')))
        
        conn.commit()
        return True
    
    def save_aptitude_result(self, user_id, test_type, score, total, correct, answers, time_taken):
        """Save aptitude test result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO aptitude_results (user_id, test_type, score, total_questions, correct_answers, answers, time_taken)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, test_type, score, total, correct, json.dumps(answers), time_taken))
        conn.commit()
        return True
    
    def save_coding_submission(self, user_id, challenge_id, title, language, code, status, score):
        """Save coding submission"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO coding_submissions (user_id, challenge_id, challenge_title, language, code, status, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, challenge_id, title, language, code, status, score))
        conn.commit()
        return True
    
    def save_interview_response(self, user_id, question, response, feedback, score):
        """Save interview response"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO interview_responses (user_id, question, response, feedback, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, question, response, feedback, score))
        conn.commit()
        return True
    
    def save_resume_analysis(self, user_id, resume_text, ats_score, keywords, suggestions):
        """Save resume analysis"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resume_analyses (user_id, resume_text, ats_score, keywords, suggestions)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, resume_text, ats_score, json.dumps(keywords), json.dumps(suggestions)))
        conn.commit()
        return True
    
    def log_activity(self, user_id, activity_type, details):
        """Log user activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activity_logs (user_id, activity_type, activity_details)
            VALUES (?, ?, ?)
        ''', (user_id, activity_type, details))
        conn.commit()
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Aptitude stats
        cursor.execute('''
            SELECT COUNT(*) as total, AVG(score) as avg, MAX(score) as max 
            FROM aptitude_results WHERE user_id = ?
        ''', (user_id,))
        aptitude = cursor.fetchone()
        
        # Coding stats
        cursor.execute('''
            SELECT COUNT(*) as total, AVG(score) as avg 
            FROM coding_submissions WHERE user_id = ?
        ''', (user_id,))
        coding = cursor.fetchone()
        
        # Recent activity
        cursor.execute('''
            SELECT activity_type, activity_details, created_at 
            FROM activity_logs WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 10
        ''', (user_id,))
        activities = cursor.fetchall()
        
        return {
            'total_tests': aptitude['total'] or 0,
            'avg_aptitude_score': round(aptitude['avg'] or 0, 2),
            'best_score': round(aptitude['max'] or 0, 2),
            'total_coding': coding['total'] or 0,
            'avg_coding_score': round(coding['avg'] or 0, 2),
            'recent_activities': [dict(act) for act in activities]
        }
    
    def get_coding_challenges(self, difficulty=None):
        """Get coding challenges"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if difficulty:
            cursor.execute('SELECT * FROM coding_challenges WHERE difficulty = ?', (difficulty,))
        else:
            cursor.execute('SELECT * FROM coding_challenges')
        challenges = cursor.fetchall()
        return [dict(ch) for ch in challenges]
    
    def get_aptitude_history(self, user_id):
        """Get user aptitude history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT test_type, score, correct_answers, total_questions, created_at 
            FROM aptitude_results WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 20
        ''', (user_id,))
        history = cursor.fetchall()
        return [dict(h) for h in history]