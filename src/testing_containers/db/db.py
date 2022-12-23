import logging
import os
from typing import List

import psycopg2
from psycopg2.extras import execute_values

from testing_containers.model.users import User


class Repo:
    # psycopg2 wrapper
    def __init__(self) -> None:
        self.conn = None
        try:
            self.connect()
            logging.info("db: database ready")
        except Exception as err:
            logging.error("db: failed to connect to database: %s", str(err))
            self.close()
            raise err

    def connect(self):
        """Stores a connection object `conn` of a postgres database"""
        logging.info("db: connecting to database")
        conn_str = os.environ.get("DB_DSN")
        self.conn = psycopg2.connect(conn_str)

    def close(self):
        """Closes the connection object `conn`"""
        if self.conn is not None:
            logging.info("db: closing database")
            self.conn.close()

    def execute_select_query(self, query: str, args: tuple = ()) -> List[tuple]:
        """Executes a read query and returns the result

        Args:
            query (str): the query to execute.
            args (tuple, optional): arguments to the select statement. Defaults to ().

        Returns:
            List[tuple]: result of the select statement. One element per record
        """
        with self.conn.cursor() as cur:
            cur.execute(query, args)
            return list(cur)

    def execute_multiple_insert_query(self, query: str, data: List[tuple], page_size: int = 100) -> None:
        """Execute a statement using :query:`VALUES` with a sequence of parameters.

        Args:
            query (str): the query to execute. It must contain a single ``%s``
                        placeholder, which will be replaced by a `VALUES list`__.
                        Example: ``"INSERT INTO table (id, f1, f2) VALUES %s"``.
            data (List[tuple]): sequence of sequences or dictionaries with the arguments to send to the query.
            page_size (int, optional): maximum number of *data* items to include in every statement.
                        If there are more items the function will execute more than one statement. Defaults to 100.
        """
        with self.conn.cursor() as cur:
            execute_values(cur, query, data, page_size=page_size)

    # repository functions
    def get_user(self, name: str) -> (User | None):
        query = "SELECT name, email FROM users WHERE name = %s"
        res = self.execute_select_query(query, (name,))
        if len(res) == 0:
            return None
        record = res[0]
        return User(name=record[0], email=record[1])

    def insert_users(self, users: List[User]) -> None:
        query = "INSERT INTO users (name, email) VALUES %s"
        data: List[tuple] = [(u.name, u.email) for u in users]
        self.execute_multiple_insert_query(query, data)
