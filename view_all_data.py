import sqlite3
import json
from datetime import datetime

def view_database():
    """View all tables and their contents"""
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print("="*50)
    print("DATABASE CONTENTS")
    print("="*50)

    for table in tables:
        name = table['name']
        print(f"\nTABLE: {name}")
        print("-"*30)

        cursor.execute(f"SELECT * FROM {name}")
        rows = cursor.fetchall()

        if rows:
            for row in rows[:10]:  # Show first 10 rows
                print(dict(row))
            if len(rows) > 10:
                print(f"... and {len(rows) - 10} more rows")
        else:
            print("No data")

    conn.close()

def view_all_users():
    """View all users with their profile information"""
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("="*80)
    print("ALL USERS - COMPLETE LIST")
    print("="*80)
    
    cursor.execute('''
        SELECT u.id, u.username, u.email, u.full_name, u.created_at, u.last_login, u.is_active,
               up.phone, up.college, up.course, up.year, up.skills, up.bio
        FROM users u
        LEFT JOIN user_profiles up ON u.id = up.user_id
        ORDER BY u.id
    ''')
    
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"\n📌 User ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Full Name: {user['full_name']}")
            print(f"   Created: {user['created_at']}")
            print(f"   Last Login: {user['last_login']}")
            print(f"   Active: {'Yes' if user['is_active'] else 'No'}")
            if user['college']:
                print(f"   College: {user['college']}")
                print(f"   Course: {user['course']}, Year: {user['year']}")
            print("-"*50)
    else:
        print("No users found")
    
    conn.close()

def view_all_aptitude_results():
    """View all aptitude test results"""
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("ALL APTITUDE TEST RESULTS")
    print("="*80)
    
    cursor.execute('''
        SELECT ar.*, u.username, u.full_name
        FROM aptitude_results ar
        JOIN users u ON ar.user_id = u.id
        ORDER BY ar.created_at DESC
    ''')
    
    results = cursor.fetchall()
    
    if results:
        for result in results:
            print(f"\n📊 Result ID: {result['id']}")
            print(f"   User: {result['username']} ({result['full_name']})")
            print(f"   Test Type: {result['test_type']}")
            print(f"   Score: {result['score']}/{result['total_questions']}")
            print(f"   Correct: {result['correct_answers']}")
            print(f"   Time: {result['time_taken']} seconds")
            print(f"   Date: {result['created_at']}")
            print("-"*50)
    else:
        print("No aptitude results found")
    
    conn.close()

def view_all_coding_submissions():
    """View all coding challenge submissions"""
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("ALL CODING SUBMISSIONS")
    print("="*80)
    
    cursor.execute('''
        SELECT cs.*, u.username, u.full_name
        FROM coding_submissions cs
        JOIN users u ON cs.user_id = u.id
        ORDER BY cs.created_at DESC
    ''')
    
    submissions = cursor.fetchall()
    
    if submissions:
        for sub in submissions:
            print(f"\n💻 Submission ID: {sub['id']}")
            print(f"   User: {sub['username']} ({sub['full_name']})")
            print(f"   Challenge: {sub['challenge_title']}")
            print(f"   Language: {sub['language']}")
            print(f"   Status: {sub['status']}")
            print(f"   Score: {sub['score']}")
            print(f"   Date: {sub['created_at']}")
            print("-"*50)
    else:
        print("No coding submissions found")
    
    conn.close()

def view_detailed_user_stats():
    """View detailed statistics for all users"""
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("USER STATISTICS SUMMARY")
    print("="*80)
    
    cursor.execute('''
        SELECT 
            u.id,
            u.username,
            u.full_name,
            COUNT(DISTINCT ar.id) as aptitude_tests,
            AVG(ar.score) as avg_aptitude_score,
            COUNT(DISTINCT cs.id) as coding_submissions,
            AVG(cs.score) as avg_coding_score,
            COUNT(DISTINCT ir.id) as interview_practices,
            COUNT(DISTINCT ra.id) as resume_analyses
        FROM users u
        LEFT JOIN aptitude_results ar ON u.id = ar.user_id
        LEFT JOIN coding_submissions cs ON u.id = cs.user_id
        LEFT JOIN interview_responses ir ON u.id = ir.user_id
        LEFT JOIN resume_analyses ra ON u.id = ra.user_id
        GROUP BY u.id
        ORDER BY u.id
    ''')
    
    stats = cursor.fetchall()
    
    if stats:
        for stat in stats:
            print(f"\n📈 User: {stat['username']} ({stat['full_name']})")
            print(f"   Aptitude Tests: {stat['aptitude_tests'] or 0}")
            if stat['avg_aptitude_score']:
                print(f"   Avg Aptitude Score: {stat['avg_aptitude_score']:.2f}")
            print(f"   Coding Submissions: {stat['coding_submissions'] or 0}")
            if stat['avg_coding_score']:
                print(f"   Avg Coding Score: {stat['avg_coding_score']:.2f}")
            print(f"   Interview Practices: {stat['interview_practices'] or 0}")
            print(f"   Resume Analyses: {stat['resume_analyses'] or 0}")
            print("-"*50)
    else:
        print("No users found")
    
    conn.close()

def export_all_data_to_json():
    """Export all data to JSON files"""
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    export_data = {}
    
    for table in tables:
        table_name = table['name']
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        export_data[table_name] = [dict(row) for row in rows]
    
    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"database_export_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"\n✅ Data exported to {filename}")
    conn.close()

def view_database_menu():
    """Interactive menu for viewing database"""
    while True:
        print("\n" + "="*50)
        print("DATABASE VIEWER MENU")
        print("="*50)
        print("1. View all tables (complete database)")
        print("2. View all users with details")
        print("3. View all aptitude results")
        print("4. View all coding submissions")
        print("5. View user statistics summary")
        print("6. Export all data to JSON")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            view_database()
        elif choice == '2':
            view_all_users()
        elif choice == '3':
            view_all_aptitude_results()
        elif choice == '4':
            view_all_coding_submissions()
        elif choice == '5':
            view_detailed_user_stats()
        elif choice == '6':
            export_all_data_to_json()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Run the interactive menu
    view_database_menu()