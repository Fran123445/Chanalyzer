import pyodbc

class DbRetriever:

    def __init__(self, connection: pyodbc.Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_threads(self, board_name: str, thread_amount: int):
        rows = self.cursor.execute('EXEC uspGetTopThreads ?, ?', (board_name, thread_amount))
        return rows.fetchall()

    def get_replies_from_thread(self, board_name: str, thread_number: int, reply_amount: int, min_words_per_reply: int):
        self.cursor.execute("EXEC uspGetRepliesForThread ?, ?, ?, ?",
                            (board_name, thread_number, reply_amount, min_words_per_reply))
        rows = self.cursor.fetchall()
        return rows