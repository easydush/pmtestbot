# Импортируем библиотеку, соответствующую типу нашей базы данных
import sqlite3


class DBConnector:
    def __init__(self):
        self.db_file = 'test.sqlite'
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def get_all_questions(self):
        sql = """
        SELECT * 
        FROM questions
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_answers(self, question_id):
        sql = """
                SELECT * 
                FROM answers
                WHERE question_id = ?
                """
        self.cursor.execute(sql, (question_id,))
        return self.cursor.fetchall()

    def init_game(self, user_id):
        sql = """
           INSERT INTO games(id, persuasion, authority, experience, relationships, performance, money, terms, quality,
                    readiness,gamer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           """
        self.cursor.execute(sql, (None, 5, 5, 0, 5, 10, 0, 0, 0, 0, user_id))
        return self.connection.commit()

    def get_game(self, user_id):
        sql = """
              SELECT * FROM games 
              WHERE gamer = ?
              ORDER BY id DESC
              """
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def change_game(self, game_id, *args, **kwargs):
        sql = """
                     UPDATE games
                     SET persuasion = persuasion + ?,
                     authority = authority + ?,
                     experience = experience + ?,
                     relationships = relationships + ?,
                     performance = performance + ?, 
                     money = money + ?,
                     terms = terms + ?,
                     quality = quality + ?,
                     readiness = readiness + ?
                     WHERE id = (?)
                     """
        self.cursor.execute(sql, (*args, game_id))
        self.connection.commit()

    def close(self):
        self.connection.close()
