from flask import Flask, render_template, redirect, url_for, request, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = b'dbJKSwh873y9WPh&*'

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    conn = mysql.connector.connect(
        host="localhost",user="sarim",password="12345678",database='db_database'
    )
    cur = conn.cursor(dictionary=True)
    user = cur.execute('SELECT * FROM author WHERE name = %s', (request.form['email'],))
    user = cur.fetchone()
    conn.close()

    if user == None:
        flash('An account with that email does not exist')
        return render_template('login.html')
    
    session['user'] = user
    return redirect(url_for('profile', id=user['id']))

@app.route('/user/<int:id>', methods=['GET'])
def profile(id: int):
    cur_id = session.get('id')
    if cur_id == None or cur_id != id:
        return 'Hmmmmmmmmmm'
    
    return render_template(
        'index.html', 
        characters=['Nameless Girl', 'Alex'], stories=['In the world without time'],
        author=session.get('name'),
    )