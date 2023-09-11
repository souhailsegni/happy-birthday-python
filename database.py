import sqlite3

class Database:
    def __init__(self, db_name="mydatabase.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        # Create a user table if it doesn't exist
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            date_of_birth DATE
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def update_user_info(self, username, date_of_birth):
        # Insert or update user information
        query = '''
        INSERT OR REPLACE INTO users (username, date_of_birth)
        VALUES (?, ?);
        '''
        self.conn.execute(query, (username, date_of_birth))
        self.conn.commit()

    def get_user_info(self, username):
        # Retrieve user information by username
        query = '''
        SELECT date_of_birth FROM users
        WHERE username = ?;
        '''
        cursor = self.conn.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def close(self):
        self.conn.close()
