import psycopg2

from flask import Flask, render_template, url_for, request, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import config

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


# SIGNIN - Signin Form
@app.route('/signin')
def signin():
    return render_template('signin.html')

# SIGNUP - Signup Form
@app.route('/signup')
def signup():
    return render_template('signup.html')

# CREATE USER - Create a new user
@app.route('/createuser', methods=['POST'])
def createuser():
    user = request.form['u']
    psswd = request.form['p']    

    print("From screen received : user = " + user + " :: password = " + psswd )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        # Check if email exists. If not, create a new user
        cur.execute("select * from \"SchoolSys\".users where email='" + user + "'")
        if len(cur.fetchall()) == 1:
            print("app.py : createuser :: user already exists in DB.")
            messages = ["Email already exists, try resetting your password!"]
            return render_template('signup.html', messages = messages)
        else:
            # Create a new user
            print("app.py : createuser :  no user record found, create new user")

            pw_hash = bcrypt.generate_password_hash(psswd).decode("utf-8")
            result = bcrypt.check_password_hash(pw_hash, 'hunter2') 
            print("pw_hash = " + pw_hash + " and pw chedk = " + str(result))
            
            cur.execute("insert into \"SchoolSys\".users (email,password,created_date,modified_date) values ('" + user + "', '" + pw_hash + "', now(), now());")
            messages = ["User successfully created."]
            conn.commit()
            return render_template('signin.html', messages = messages)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close() 



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
        
        cur.execute("select * from \"SchoolSys\".users where email='" + user + "'")
        rows_retrieved = cur.fetchall() 
        if len(rows_retrieved) == 1:
            print("AUTHENTICATE: One record found")
            for row in rows_retrieved:
                print("Password retrieved = " + row[1] + " :: " + psswd)
                result = bcrypt.check_password_hash(row[1], psswd)
                print ("Password check result = " + str(result))
                if( not result ):
                    messages = ["Either your Username or Password is incorrect, please try again"]
                    return render_template('signin.html', messages = messages)
                
            return render_template('index.html')
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