import pyodbc

from models.board import Board
from models.thread import Thread


class SQLAccess:

    def __init__(self, connection: pyodbc.Connection):
        self.connection = connection
        self.cursor = connection.cursor() # race condition waiting to happen, should fix it

    def _get_threads(self, board: Board, thread_amount: int):
        rows = self.cursor.execute('EXEC uspGetTopThreads ?, ?', (board.board_name, thread_amount))
        return rows.fetchall()

    def _get_posts_from_thread(self, board: Board, thread_number: int, post_amount: int, min_words_per_post: int):
        rows = self.cursor.execute("EXEC uspGetPostsForThread ?, ?, ?, ?",
                                   (board.board_name, thread_number, post_amount, min_words_per_post))
        return rows.fetchall()

    def get_board_with_threads(self, board_name: str, thread_amount: int,
                               post_amount: int, min_words_per_post: int):

        board = Board(board_name, [])
        threads = self._get_threads(board, thread_amount)

        for thread in threads:
            thread_title = thread[0]
            thread_number = int(thread[1])
            thread_posts = self._get_posts_from_thread(board, thread_number, post_amount, min_words_per_post)
            thread_posts = [post[0] for post in thread_posts]

            # this can happen if no post satisfies the min_words_per_post condition
            if not thread_posts:
                continue

            # actually i should check this earlier because this way it's not meeting the min thread amount required

            board.threads.append(Thread(board_name, thread_number, thread_title, thread_posts))

        return board

    def get_boards(self):
        rows = self.cursor.execute('SELECT board_name FROM Board')
        return rows.fetchall()

    def close_connection(self):
        self.connection.close()