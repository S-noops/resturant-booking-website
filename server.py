import sqlite3
from flask import Flask, request, render_template, redirect, url_for
import hashlib

app = Flask(__name__)

def encrypt(text):
    b = text.encode()
    enc = hashlib.sha1(b).hexdigest()
    return enc

@app.route('/')
def login_signup():
    try:
        data = [request.args.get('v')]
    except:
        data = ["d"]
    return render_template('login_signup.html', data=data)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/sign_in_check', methods=['POST'])
def checkLogin():
    email = request.form['email']
    pswd = request.form['pass']
    pswd = encrypt(pswd)

    conn = sqlite3.connect("resturant.db")
    q1 = "select email, password from users where email = '{em}' and password = '{ps}'".format(
        em=email, ps=pswd) 
    rows = conn.execute(q1)
    rows = rows.fetchall()
    conn.close()
    if (len(rows) == 1):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login_signup', v="a"))


@app.route('/sign_up_check', methods=['POST'])
def signup_check():
    email = request.form['email']
    pswd = request.form['pass']
    pswd = encrypt(pswd)

    conn = sqlite3.connect("resturant.db")
    q1 = "select email,password from users where email = '{em}' and password = '{ps}'".format(
        em=email, ps=pswd)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    if (len(rows) == 1):
        return redirect(url_for('login_signup', v="b"))
    else:
        q2 = "insert into users (email, password) values('{em}','{ps}')".format(
        em=email, ps=pswd)
        conn.execute(q2)
        conn.commit()
        conn.close()
        return redirect(url_for('login_signup', v="c"))


if __name__ == '__main__':
    app.run(debug=True)