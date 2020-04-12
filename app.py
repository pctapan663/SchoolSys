import psycopg2

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import config

app = Flask(__name__)

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


# SIGNIN - Signin Form
@app.route('/signin')
def signin():
    return render_template('signin.html')

# AUTHENTICATE - let the user sign in to application
@app.route('/authorize', methods=['POST'])
def login():
    user = request.form['u']
    psswd = request.form['p']

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("select * from \"SchoolSys\".users where email='" + user + "' and password='" + psswd + "'")
        if len(cur.fetchall()) == 1:
            print("AUTHENTICATE: One record found")
            app.logger.info('%s logged in successfully', user)
            return render_template(index.html)
        else:
            print("AUTHENTICATE: No record found")
            app.logger.info('%s failed to log in', user)
            messages = ["Either your Username or Password is incorrect, please try again"]
            return render_template('signin.html', messages = messages)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    app.run()