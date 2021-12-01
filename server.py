import sqlite3
from flask import Flask, request, render_template, redirect, url_for
import hashlib
from datetime import datetime

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
    pswd = request.form['pass_']
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
    pswd = request.form['pass_']
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
    k = k[:int(ids)]
    flag=False
    j=k[0][0]
    for i in k:
        if (i[0]!=j):
            flag=True
    k = ", ".join(k)
    # ids = ", ".join(ids)
    date_booking = datetime.strptime(date, "%Y-%m-%d")
    weekend=False
    if (date_booking.strftime("%A")=="Saturday" or date_booking.strftime("%A")=="Sunday"):
        weekend=True
    info = [name,email,phone,date,time,ids,k,flag,weekend]
    return render_template("tables_info.html", data=info)

@app.route('/confirmation', methods=['POST'])
def confirmation():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    guest_ids = request.form['guest_ids']
    seat_ids = request.form['seat_ids']
    conn = sqlite3.connect("resturant.db")
    q1 =  "insert into orders (name, email, phone, date, time, guest_ids, seat_ids) values('{nm}','{em}','{ph}','{dt}','{tm}','{gi}','{si}')".format(nm=name, em=email, ph=phone, dt=date, tm=time, gi=guest_ids, si=seat_ids)
    conn.execute(q1)
    conn.commit()
    conn.close()
    seat_ids = seat_ids.split(", ")
    cost = len(seat_ids)*10
    conn = sqlite3.connect("resturant.db")
    q1 =  "update users set points = points+{pt} where email='{em}'".format(pt=cost, em=email)
    conn.execute(q1)
    conn.commit()
    conn.close()
    with open("seats.txt","r") as f:
        tot = f.read()
    tot = tot.split(" ")
    for i in seat_ids:
        if i in tot:
            tot.remove(i)
    tot = " ".join(tot)
    with open("seats.txt","w") as f:
        f.write(tot)
    return render_template("thankyou.html")

@app.route('/validate_signup', methods=['POST'])
def validate_signup():
    signup_email = request.form['signup_email']
    signup_pass = request.form['signup_pass']
    signup_pass = encrypt(signup_pass)
    conn = sqlite3.connect("resturant.db")
    q1 = "select email,password from users where email = '{em}' and password = '{ps}'".format(
        em=signup_email, ps=signup_pass)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    if (len(rows) != 1):
        q2 = "insert into users (email, password) values('{em}','{ps}')".format(
        em=signup_email, ps=signup_pass)
        conn.execute(q2)
        conn.commit()
        conn.close()
    name = request.form['name_signup']
    email = request.form['email_signup']
    phone = request.form['phone_signup']
    date = request.form['date_signup']
    time = request.form['time_signup']
    guest_ids = request.form['guest_ids_signup']
    seat_ids = request.form['seat_ids_signup']
    conn = sqlite3.connect("resturant.db")
    q1 =  "insert into orders (name, email, phone, date, time, guest_ids, seat_ids) values('{nm}','{em}','{ph}','{dt}','{tm}','{gi}','{si}')".format(nm=name, em=email, ph=phone, dt=date, tm=time, gi=guest_ids, si=seat_ids)
    conn.execute(q1)
    conn.commit()
    conn.close()
    seat_ids = seat_ids.split(", ")
    cost = len(seat_ids)*10
    conn = sqlite3.connect("resturant.db")
    q1 =  "update users set points = points+{pt} where email='{em}'".format(pt=cost, em=signup_email)
    conn.execute(q1)
    conn.commit()
    conn.close()
    with open("seats.txt","r") as f:
        tot = f.read()
    tot = tot.split(" ")
    for i in seat_ids:
        if i in tot:
            tot.remove(i)
    tot = " ".join(tot)
    with open("seats.txt","w") as f:
        f.write(tot)
    return render_template("thankyou.html")

@app.route('/profile/<string:uname>')
def profile(uname):
    conn = sqlite3.connect("resturant.db")
    q1 = "select name,mailing_address,billing_address,pay_method,c_id,points from users where email = '{em}'".format(em=uname)
    row = conn.execute(q1)
    row = row.fetchone()
    row = list(row)
    for idx,i in enumerate(row):
        if i is None:
            row[idx] = ""
    conn.close()
    row.append(uname)
    return render_template("profile.html",info=row)

@app.route('/update_details', methods=['POST'])
def update_details():
    conn = sqlite3.connect("resturant.db")
    email= request.form['email']
    name = request.form['name']
    mailing_address = request.form['mailing_address']
    billing_address = request.form['billing_address']
    pay = request.form['pay']
    q4 = "update users set name='{nm}', mailing_address='{ma}', billing_address='{ba}', pay_method='{pm}' where email='{em}'".format(nm=name,ma=mailing_address,ba=billing_address,pm=pay,em=email)
    conn.execute(q4)
    conn.commit()
    conn.close()
    return redirect("/profile/{}".format(email))

if __name__ == '__main__':
    app.run(debug=True)