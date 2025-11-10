"""
give each letter in each word a numerical value equal to its position in the alphabet.
so "a" is 1 and "z" is 26. Punctuatiion and whitespace is 0. find words where the sum of
the value of the letters is 100. print the list fo words ordered from shortest to longest.

the first line of the input will be an integer representing the number of inputs

sample input:


10
acalephe
decolor
estheses
heroize
paviors
speer
stower
tsoris
unmiter
sample


output:
stower
tsoris
paviors
unmiter
estheses
"""

import sys
import sqlite3


def setup_database():
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            word_value INTEGER NOT NULL,
            word_length INTEGER NOT NULL
        )
    """
    )
    conn.commit()
    return conn, cursor


def calculate_word_value(word):
    total = 0
    for char in word:
        if char.isalpha():
            total += ord(char) - ord("a") + 1
    return total


def store_words_in_db(cursor, conn):
    max_words = int(sys.stdin.readline())
    for count in range(max_words):
        word = sys.stdin.readline().strip().lower()
        word_value = calculate_word_value(word)
        word_length = len(word)

        cursor.execute(
            """
            INSERT INTO words (word, word_value, word_length)
            VALUES (?, ?, ?)
        """,
            (word, word_value, word_length),
        )
    conn.commit()


def get_words_with_value_100(cursor):
    cursor.execute(
        """
        SELECT word FROM words
        WHERE word_value = 100
        ORDER BY word_length ASC, word ASC
    """
    )
    return [row[0] for row in cursor.fetchall()]


if __name__ == "__main__":
    conn, cursor = setup_database()
    store_words_in_db(cursor, conn)
    results = get_words_with_value_100(cursor)
    for row in results:
        print(row)
    conn.close()
