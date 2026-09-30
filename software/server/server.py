"""
    Author: Ahmad Taka
    Description this page handles server requests
"""
import sqlite3
import datetime

COLORS_DATABASE = "/var/jail/home/ahmadtak/server/colors_database.db"


def handle_database_post(red, green, blue):
    conn = sqlite3.connect(COLORS_DATABASE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS colors_table (red int, green int, blue int, timing timestamp);""")
    c.execute("""INSERT into colors_table VALUES (?, ? , ?, ?);""", (red, green, blue, datetime.datetime.now()))
    conn.commit()
    conn.close()
    return  

def handle_database_get():
    conn = sqlite3.connect(COLORS_DATABASE)
    c = conn.cursor()
    colors_and_time = c.execute("""SELECT * FROM colors_table ORDER BY timing DESC;""").fetchall()
    conn.commit()
    conn.close()
    if not colors_and_time:
        return (0, 0, 0, None)
    else:
        return colors_and_time[0]


def request_handler(request):
    if request["method"] == "GET":
        red, green, blue, _ = handle_database_get()
        return "{},{},{}".format(red, green, blue)
    else: 
        return "ERROR NOT GET FROM ESP32"