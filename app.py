#at first importing all needed modules
from flask import Flask , render_template , request , redirect , url_for , session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'my new project'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sql4321'
app.config['MYSQL_DB'] = 'weblogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/login',methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        passkey = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM datalist WHERE username = %s AND passkey = %s',(username , passkey,))
        useraccount = cursor.fetchone()
        if useraccount:
            session['loggedin'] = True
            session['id'] = useraccount['id']
            session['username'] =  useraccount['username']
            msg = 'Logged in successfully'
            return render_template('index.html',msg = msg)
        else:
            msg = 'INCORRECT password or username . try again!!'
    
    return render_template('login.html',msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/register',methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'passkey' in request.form and 'email' in request.form:
        username = request.form['username']
        passkey = request.form['passkey']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM datalist WHERE username = %s',(username ,))
        useraccount = cursor.fetchone()
        if useraccount:
            msg = 'acoount already exists !'
            return redirect(url_for('login'))
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        
        else:
            cursor.execute('INSERT INTO datalist VALUES (NULL, %s , %s , %s)', (username , passkey , email,))
            mysql.connection.commit()
            msg = 'You have registered successfully !!'
    elif request.method == 'POST':
        msg = 'please fill the form'
    return render_template('register.html', msg = msg)