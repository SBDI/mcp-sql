import sqlite3
from pathlib import Path

def init_database():
    # Delete existing database if it exists
    db_path = Path("database.db")
    if db_path.exists():
        db_path.unlink()
    
    # Create new database and connect to it
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )
    """)
    
    # Sample user data
    sample_users = [
        ("John Doe", "john@example.com", 28),
        ("Jane Smith", "jane@example.com", 34),
        ("Bob Wilson", "bob@example.com", 45),
        ("Sarah Johnson", "sarah@example.com", 31),
        ("Mike Brown", "mike@example.com", 29),
        ("Emily Davis", "emily@example.com", 38),
        ("David Lee", "david@example.com", 42),
        ("Lisa Anderson", "lisa@example.com", 33),
        ("Tom Harris", "tom@example.com", 27),
        ("Amy Wilson", "amy@example.com", 36)
    ]
    
    # Insert sample data
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        sample_users
    )
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database initialized with sample data!")
    
    # Display sample query
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print("\nSample data:")
    print("ID | Name | Email | Age")
    print("-" * 50)
    for row in cursor.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    conn.close()

if __name__ == "__main__":
    init_database()