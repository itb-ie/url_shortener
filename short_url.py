import sqlite3
import random
DB_NAME = "short_urls.db"
TABLE_NAME = "urls"
LEN = 8
VALUES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"


def shorten_url(url):
    result = check_url_exists(url)
    if result:
        # already in the DB
        return result

    short_url = create_short_url()
    add_url(url, short_url)
    return short_url


def get_long_from_short(short):
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE short_url=?", (short, ))
        lines = cur.fetchall()
        if not lines:
            return False
        return lines[0][1]


def check_url_exists(url):
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE url=?", (url,))
        lines = cur.fetchall()
        if not lines:
            return False
        return lines[0][2]


def check_short_url_exists(url):
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE short_url=?", (url,))
        lines = cur.fetchall()
        if not lines:
            return False
        return lines[0][2]


def add_url(url, short_url):
    """
    Adds an Url to the database
    :param url: the url to add
    :type url: str
    :param short_url: the short url to add
    """
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()
        cur.execute(f"INSERT INTO {TABLE_NAME} VALUES (NULL, ?, ?)", (url, short_url))
        db.commit()


def create_short_url():
    while True:
        url = [VALUES[random.randint(0, len(VALUES))] for _ in range(LEN)]
        url = "".join(url)
        if not check_short_url_exists(url):
            return url


if __name__ == "__main__":
    # need to create the database
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER PRIMARY KEY, url STRING, short_url STRING)")

    print(check_url_exists("google.com"))
    add_url("google.com", "gg.com")
    print(check_url_exists("google.com"))
    print(shorten_url("google.com"))
    print(shorten_url("facebook.com"))
