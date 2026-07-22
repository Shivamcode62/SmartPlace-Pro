import sqlite3

def show_all_users():
    conn = sqlite3.connect('data/smartplace.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    print("\n" + "="*60)
    print(f"TOTAL USERS: {len(users)}")
    print("="*60)
    
    for user in users:
        print(f"\nID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"Full Name: {user['full_name']}")
        print(f"Created: {user['created_at']}")
        print(f"Last Login: {user['last_login']}")
        print(f"Active: {user['is_active']}")
        print("-"*40)
    
    conn.close()

if __name__ == "__main__":
    show_all_users()