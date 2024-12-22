import pyodbc

from models.models import Board, Thread


class SQLAccess:

    def __init__(self, connection: pyodbc.Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def _get_threads(self, board: Board, thread_amount: int):
        rows = self.cursor.execute('EXEC uspGetTopThreads ?, ?', (board.board_name, thread_amount))
        return rows.fetchall()

    def _get_replies_from_thread(self, board: Board, thread_number: int, reply_amount: int, min_words_per_reply: int):
        rows = self.cursor.execute("EXEC uspGetRepliesForThread ?, ?, ?, ?",
                            (board.board_name, thread_number, reply_amount, min_words_per_reply))
        return rows.fetchall()

    def get_board_with_threads(self, board_name: str, thread_amount: int,
                               reply_amount: int, min_words_per_reply: int):

        board = Board(board_name, [])
        threads = self._get_threads(board, thread_amount)

        for thread in threads:
            thread_number = int(thread[0])
            thread_posts = self._get_replies_from_thread(board, thread_number, reply_amount, min_words_per_reply)
            thread_posts = [post[0] for post in thread_posts]
            board.threads.append(Thread(thread_number, thread_posts))

        return board