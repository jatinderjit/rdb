from . import http
from .db import Database


def run():
    db = Database()
    http.run(db)
