"""
    Author: Ahmad Taka
    Description this page handles home page
"""
from cmath import e
import re
import sqlite3
import datetime

COLORS_DATABASE = "/var/jail/home/ahmadtak/server/colors_database.db"
HOME_PAGE = \
    """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="x-ua-compatible" content="ie=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Smart Lamp UI</title>
        
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
                        
        </head>
        <body>
            <nav class="navbar navbar-dark bg-dark">
            <span class="navbar-brand mb-0 h1">Smart Lamp Control</span>
            </nav>
            <div class="card" style="width: 50%; margin: 0 auto; margin-top: 30px;">
            <div class="card-header bg-primary text-center" style="font-size: x-large;"> <b>Pick Color</b> </div>
            <div class="card-body">
                <form action="/sandbox/sc/ahmadtak/server/home.py" method="POST">
                    <div id="red-group" class="form-group">
                    <label for="red">Red (between 0 and 255):</label>
                    <input name="red" type="range" class="form-control-range custom-range-red" id="red" min="0" max="255" value="{0}">
                    </div>
                    <div id="green-group" class="form-group">
                    <label for="green">Green (between 0 and 255):</label>
                    <input name="green" type="range" class="form-control-range custom-range-green" id="green" min="0" max="255" value="{1}">
                    </div>
                    <div id="blue-group" class="form-group">
                    <label for="blue">Blue (between 0 and 255):</label>
                    <input name="blue" type="range" class="form-control-range custom-range-blue" id="blue" min="0" max="255" value="{2}">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
            <div id="last-updated" class="card-footer text-muted">Last Updated: {3}</div>
            </div>
        </body>
        <style>
            .custom-range-red::-webkit-slider-runnable-track{{
                background: linear-gradient(90deg, white, red);
            }}

            .custom-range-red::-moz-range-track {{
                background: linear-gradient(90deg, white, red);
            }}

            .custom-range-red::-ms-track{{
                background: linear-gradient(90deg, white, red);
            }}

            .custom-range-green::-webkit-slider-runnable-track{{
                background: linear-gradient(90deg, white, green);
            }}

            .custom-range-green::-moz-range-track {{
                background: linear-gradient(90deg, white, green);
            }}

            .custom-range-green::-ms-track{{
                background: linear-gradient(90deg, white, green);
            }}
            .custom-range-blue::-webkit-slider-runnable-track{{
                background: linear-gradient(90deg, white, blue);
            }}

            .custom-range-blue::-moz-range-track {{
                background: linear-gradient(90deg, white, blue);
            }}

            .custom-range-blue::-ms-track{{
                background: linear-gradient(90deg, white, blue);
            }}
        </style>
        </html> 
    """


conn = sqlite3.connect(COLORS_DATABASE)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS colors_table (red int, green int, blue int, timing timestamp);""")

def render_home():
    red, green, blue, time = handle_database_get()
    return HOME_PAGE.format(str(red), str(green), str(blue), str(time)) 

def handle_database_post(red, green, blue):
    conn = sqlite3.connect(COLORS_DATABASE)
    c = conn.cursor()
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
    if request["method"] == "POST":
        red, green, blue = 0, 0, 0
        try: 
            red = int(request["form"]["red"])
            green = int(request["form"]["green"])
            blue = int(request["form"]["blue"])
            handle_database_post(red, green, blue)
            return render_home()
        except Exception as e:
            return render_home()
    else:
        return render_home()

