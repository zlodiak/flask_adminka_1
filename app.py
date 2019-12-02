from flask import Flask, render_template
from flask import request, Response, make_response, redirect
import psycopg2
import hashlib

app = Flask(__name__)

@app.route('/')
def auth():
    return render_template('auth.html')

@app.route('/admin')
def admin():
    if 'flask_adminka_authorized_user_id' not in request.cookies:
        return redirect('/', code=404)

    return render_template('admin.html')

@app.route('/auth_request', methods=['POST'])
def auth_request():
    db_conn = psycopg2.connect(
        database='flask_adminka', 
        user='flask_admin', 
        password='flask_admin',
        host='localhost'
    )
    db_cursor = db_conn.cursor()
    pasword = request.values.get('password')
    password_hash = hashlib.sha1(pasword.encode('ASCII')).hexdigest()
    email = request.values.get('email')
    req = "select * from users where password_hash='" + password_hash + "' and email='" + email + "' and active=TRUE"

    try:
        db_cursor.execute(req)
        user = db_cursor.fetchone() 
        print("Id = ", user[0])
        print("pass = ", user[1])
        print("email  = ", user[2])
        print("active  = ", user[3])
        resp = Response('authorized')
        resp.headers['Set-Cookie'] = 'flask_adminka_authorized_user_id=' + str(user[0])
        return resp
    except:
        resp = Response('not authorized')
        return resp

@app.route('/profile_request', methods=['POST'])
def profile_request():
    db_conn = psycopg2.connect(
        database='flask_adminka', 
        user='flask_admin', 
        password='flask_admin',
        host='localhost'
    )
    db_cursor = db_conn.cursor()
    db_conn.autocommit = True 

    firstname = request.values.get('firstname')
    lastname = request.values.get('lastname')
    id_auth_user = request.cookies.get('flask_adminka_authorized_user_id')

    req = "select * from options where user_id=" + id_auth_user
    db_cursor.execute(req)
    record = db_cursor.fetchone() 

    if record:
        req = "UPDATE options SET firstname='" + firstname + "', lastname='" + lastname + "' WHERE user_id=" + str(id_auth_user)
        db_cursor.execute(req);
        db_conn.commit()

    return 'profile_request' + lastname + firstname

if __name__ == '__main__':
    app.run()