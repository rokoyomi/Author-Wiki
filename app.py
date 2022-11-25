from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from form_builder import form_builder
from dummydb import query, join

app = Flask(__name__)
app.secret_key = b'dbJKSwh873y9WPh&*'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sarim'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'db_database'
mysql = MySQL(app)
fb = form_builder(mysql)

#def query(q : str, t : tuple, l = True):
#    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#    cur.execute(q, t)
#    if l:
#        res = cur.fetchall()
#    else:
#        res = cur.fetchone()
#    cur.close()
#    return res

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('profile', id=session['user']['id']))
        return render_template('login.jinja')

    #user = query(
    #    "SELECT id, concat(first_name, ' ', last_name) as name, email, pen_name \
    #        FROM author WHERE email = %s",
    #    (request.form['email'],), False
    #)

    user = query('author', ['email'], [request.form['email']], False)

    if user == None:
        flash('An account with that email does not exist')
        return render_template('login.jinja')
    
    session['user'] = user
    return redirect(url_for('profile', id=user['id']))

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))

@app.route('/user/<int:id>', methods=['GET'])
def profile(id: int):
    user = session.get('user')
    
    #characters = query(
    #    "SELECT * FROM characters WHERE author_id = %s",
    #    (cur_id,)
    #)
    characters = query('characters', ['author_id'], [user['id']])
    stories = query('story', ['author_id'], [user['id']])
    worlds = query('world', ['author_id'], [user['id']])
    locations = query('location', ['author_id'], [user['id']])
    items = query('item', ['author_id'], [user['id']])
    races = query('race', ['author_id'], [user['id']])

    return render_template('index.jinja', 
        author=user, characters_list=characters, stories=stories, 
        worlds=worlds,locations=locations, items=items, races=races
    )

@app.route('/characters/<int:character_id>')
def character(character_id: int):
    #chara = query(
    #    "SELECT * FROM characters WHERE id = %s and author_id = %s",
    #    (character_id, session['user']['id']), False
    #)

    _character = query('characters', ['id','author_id'], [character_id, session['user']['id']], False)
    if _character == None:
        return 'Not Found',404

    traits= query('traits', ['character_id'], [character_id])
    appearances = query('appearance', ['character_id'], [character_id])
    s_appearances = [query('story', ['id'], [appearance['story_id']], False) for appearance in appearances]

    return render_template('elements/character.jinja', 
        author= session['user'], element=_character,
        traits=traits, appearances=join(s_appearances, appearances)
    )

@app.route('/stories/<int:story_id>')
def story(story_id):
    s = query('story', ['id'], [story_id], False)

    if s == None:
        return 'Not Found',404

    arcs = query('arc', ['story_id'], [story_id])
    s_appearances = query('appearance', ['story_id'], [story_id])
    c_appearances = [query('characters', ['id'], [appearance['character_id']], False) for appearance in s_appearances]

    return render_template('elements/story.jinja', 
        author=session['user'], element=s, arcs=arcs, appearances=join(s_appearances, c_appearances)
    )

@app.route('/stories/<int:story_id>/arcs/<arc_name>')
def arc(story_id, arc_name):
    a = query('arc', ['story_id', 'name'], [story_id, arc_name], False)
    if a == None:
        return 'Not Found',404
    
    return render_template('elements/element_base.jinja', 
        author=session['user'], element=a
    )

@app.route('/worlds/<int:world_id>')
def world(world_id):
    _world = query('world', ['id'], [world_id], False)
    if _world == None:
        return 'Not Found',404

    _locations = query('location', ['world_id'], [world_id])

    return render_template('elements/world.jinja', 
        author=session['user'], element=_world, locations=_locations
    )

@app.route('/locations/<int:location_id>')
def location(location_id):
    _location = query('location', ['id'], [location_id], False)
    if _location == None:
        return 'Not Found', 404
    
    return render_template('elements/element_base.jinja',
        author=session['user'], element=_location
    )

@app.route('/races/<int:race_id>')
def race(race_id):
    _race = query('race', ['id'], [race_id], False)
    if _race == None:
        return 'Not Found', 404
    
    return render_template('elements/element_base.jinja',
        author=session['user'], element=_race
    )

@app.route('/items/<int:item_id>')
def item(item_id):
    _item = query('item', ['id'], [item_id], False)
    if _item == None:
        return 'Not Found', 404
    
    return render_template('elements/element_base.jinja',
        author=session['user'], element=_item
    )

@app.route('/forms/<table_name>')
def form(table_name):
    if 'user' not in session:
        return redirect(url_for('login'))
    return fb.get_form(table_name)
