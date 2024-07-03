import psycopg2

class database():
    def __init__(self, conn:psycopg2.extensions.connection):
        self.conn = conn

    def get_all_users(self):
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT * FROM users")

        records = cursor.fetchall()

        return records

    def create_new_user(self, telegram_id, username, isPrime=False):
        cursor = self.conn.cursor()

        try:
            cursor.execute("INSERT INTO users (telegram_id, username, isPrime) VALUES (%s, %s, %s)", (telegram_id, username, isPrime))
            self.conn.commit()
            return 1
        except Exception as e:
            print("Error: Creating user:",e)
            return None

    def get_user_by_telegram_id(self,telegram_id):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))

        record = cursor.fetchone()

        return record
    
    def create_new_word(self, data):
        cursor = self.conn.cursor()

        try:
            cursor.execute("INSERT INTO words (word, translated_word, category_id) VALUES (%s, %s, %s)", (data["word"], data["translated_word"], data["category_id"]),)
            self.conn.commit()
            return 1
        except Exception as e:
            print("Error: Creating new word:",e)
            return None
        
    def get_random_words(self):
        cursor = self.conn.cursor()

        cursor.execute("""
                       SELECT * FROM words
                        ORDER BY RANDOM()
                        LIMIT 4;
                """)

        words = cursor.fetchall()

        return words