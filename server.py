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

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/tables')
def tables():
    with open("seats.txt","r") as f:
        k = f.read()
    k = k.split(" ")
    tot = ["A1", "A2", "A3", "A4", "B1", "B2", "C1", "C2", "C3", "C4", "C5","C6", "D1", "D2", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8","F1", "F2", "F3", "F4"]
    na_seats = list(set(tot)-set(k))
    av_seats = list(set(tot)-set(na_seats))
    na_seats = ", ".join(na_seats)
    av_seats = ", ".join(av_seats)
    return render_template('tables.html', data=[na_seats,av_seats])

@app.route('/check_tables', methods=['POST'])
def check_tables():
    with open("seats.txt","r") as f:
        k = f.read()
    k = k.split(" ")
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    ids = request.form['guest_ids']
    ids = ids.split(" ")
    k = k[:len(ids)]
    flag=False
    j=k[0][0]
    for i in k:
        if (i[0]!=j):
            flag=True
    k = ", ".join(k)
    ids = ", ".join(ids)
    info = [name,email,phone,date,time,ids,k,flag]
    return render_template("tables_info.html", data=info)


if __name__ == '__main__':
    app.run(debug=True)