from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from form_builder import form_builder

app = Flask(__name__)
app.secret_key = b'dbJKSwh873y9WPh&*'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sarim'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)
fb = form_builder(mysql, app.config['MYSQL_DB'])

def query(q : str, t : tuple, l = True, d=True):
    if d:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    else:
        cur = mysql.connection.cursor()
    cur.execute(q, t)
    if l:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    cur.close()
    return res
def get_col_names(table_name):
    col = query("select column_name \
        from information_schema.columns \
        where table_schema=%s and table_name=%s order by ordinal_position", 
        (app.config['MYSQL_DB'], table_name),
    )
    return col

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('profile', id=session['user']['id']))
        return render_template('login.jinja')

    user = query(
        "SELECT id, concat(first_name, ' ', last_name) as name, email, pen_name \
            FROM author WHERE email = %s", (request.form['email'],), False
    )
    print(user)

    if not user:
        flash('An account with that email does not exist')
        return render_template('login.jinja')
    
    session['user'] = user
    return redirect(url_for('profile', id=user['id']))

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login'))

@app.route('/user/<int:id>', methods=['GET'])
def profile(id: int):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session.get('user')

    _characters = query("select * from characters where author_id=%s", (id,))
    _stories = query("select * from story where author_id=%s", (id,))
    _worlds = query("select * from world where author_id=%s", (id,))
    _locations = query("select * from location where author_id=%s", (id,))
    _items = query("select * from item where author_id=%s", (id,))
    _races = query("select * from race where author_id=%s", (id,))
    _organizations = query("select * from organization where author_id=%s", (id,))

    return render_template('index.jinja', 
        author=user, characters_list=_characters, stories=_stories, 
        worlds=_worlds,locations=_locations, items=_items, races=_races, organizations=_organizations
    )

@app.route('/characters/<int:id>', methods=['GET', 'POST'])
def characters(id: int):
    if 'user' not in session:
        return redirect(url_for('login'))
    _character = query("select * from characters where id=%s and author_id=%s", (id, session['user']['id']), False)
    if not _character:
        return 'Not Found',404
    
    if request.method == 'POST':
        existing = {"character_id":id}
        return fb.get_form('traits', url_for('form', table_name='traits'), existing)

    _traits = query("select * from traits where character_id=%s", (id,))
    _character_appearances = query(
        "select a.name, ap.role, ap.description as role_description, a.story_id, ap.arc_id \
        from characters c inner join (appearance ap inner join arc a on ap.arc_id=a.id) on c.id=ap.character_id \
        where c.id=%s", (id,)
    )
    _race = query("select id, name from race where id=%s", (_character['race_id'],), False)

    return render_template('elements/character.jinja', 
        author= session['user'], element=_character,
        traits=_traits, appearances=_character_appearances, race=_race, table_name='characters'
    )

@app.route('/stories/<int:id>', methods=['GET', 'POST'])
def story(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    s = query("select * from story where id=%s", (id,), False)
    if not s:
        return 'Not Found',404
    
    if request.method == 'POST':
        existing = {"story_id":id}
        return fb.get_form('arc', url_for('form', table_name='arc'), existing)

    arcs = query("select * from arc where story_id=%s", (id,))
    characters = query("select distinct(c.id) as character_id, c.name, c.description as role_description \
        from characters c inner join (appearance app inner join arc a on app.arc_id=a.id) on app.character_id=c.id\
        where a.story_id=%s", (id,)
    )

    return render_template('elements/story.jinja', 
        author=session['user'], element=s, arcs=arcs, table_name='story', appearances=characters
    )

@app.route('/stories/<int:story_id>/arcs/<int:id>', methods=['GET','POST'])
def arc(story_id, id):
    if 'user' not in session:
        return redirect(url_for('login'))
    a = query("select * from arc where id=%s", (id,), False)
    if not a:
        return 'Not Found',404
    
    if request.method == 'POST':
        form = request.form.to_dict()
        existing = {"arc_id":id}
        if form['form_name'] == 'add_character':
            return fb.get_form('appearance', url_for('form', table_name='appearance'), existing)
        elif form['form_name'] == 'add_location':
            return fb.get_form('arc_occurs_in', url_for('form', table_name='arc_occurs_in'), existing)
        elif form['form_name'] == 'add_item':
            return fb.get_form('item_featured_in', url_for('form', table_name='item_featured_in'), existing)

    _character_appearances = query("select c.id as character_id, c.name, app.role, app.description as role_description \
        from characters c inner join (appearance app inner join arc a on app.arc_id=a.id) on app.character_id=c.id\
        where a.id=%s",(id,)
    )
    _featured_locations = query("select * \
        from location l inner join (arc_occurs_in occ inner join arc a on occ.arc_id=a.id) on occ.location_id=l.id\
        where a.id=%s",(id,)
    )
    _featured_items = query("select * \
        from item i inner join (item_featured_in f inner join arc a on f.arc_id=a.id) on f.item_id=i.id\
        where a.id=%s",(id,)
    )

    character_list = query("select id, name \
        from characters\
        where author_id=%s and id not in %s", (session['user']['id'], 
        query("select character_id \
            from appearance \
            where arc_id=%s", (id,), d=False) or ((0),) # hack
        )
    )

    return render_template('elements/arc.jinja', 
        author=session['user'], element=a, appearances=_character_appearances,
        locations=_featured_locations, items=_featured_items, table_name='arc', character_list=character_list
    )

@app.route('/worlds/<int:id>')
def world(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    _world = query("select * from world where id=%s", (id,), False)
    if not _world:
        return 'Not Found',404
    
    _locations = query("select id, name, description, category \
        from location \
        where world_id=%s", (id,)
    )
    _races = query("select r.id, r.name, r.description, r.category \
        from race r inner join (race_lives_in rl inner join world w on rl.world_id=w.id) on rl.race_id=r.id \
        where w.id=%s", (id,)
    )
    _items = query("select i.id, i.name, i.description, i.category \
        from item i inner join (item_found_in_world ifw inner join world w on ifw.world_id=w.id) on ifw.item_id=i.id \
        where w.id=%s", (id,)
    )

    return render_template('elements/world.jinja', 
        author=session['user'], element=_world, locations=_locations, 
        races=_races, items=_items,
    )

@app.route('/locations/<int:id>')
def location(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    _location = query("select * from location where id=%s", (id,), False)
    if not _location:
        return 'Not Found', 404
    
    _child_loc = query("select * from location where location_id=%s", (id,))
    _arcs = query("select a.id, a.name, a.description, a.story_id \
        from arc a inner join (arc_occurs_in occ inner join location l on occ.location_id=l.id) on occ.arc_id=a.id\
        where l.id=%s", (id,)
    )

    return render_template('elements/location.jinja',
        author=session['user'], element=_location, locations=_child_loc, arcs=_arcs, table_name='location'
    )

@app.route('/races/<int:id>')
def race(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    _race = query("select * from race where id=%s", (id,), False)
    if not _race:
        return 'Not Found', 404
    
    _worlds = query("select * \
        from world w inner join (race_lives_in l inner join race r on l.race_id=r.id) on l.world_id=w.id\
        where r.id=%s", (id,)
    )
    _characters = query("select * from characters where race_id=%s", (id,))

    return render_template('elements/race.jinja',
        author=session['user'], element=_race, worlds=_worlds, characters=_characters, table_name='race'
    )

@app.route('/items/<int:id>')
def item(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    _item = query("select * from item where id=%s", (id,), False)
    if not _item:
        return 'Not Found', 404
    
    _worlds = query("select w.id, w.name, w.description \
        from world w inner join (item_found_in_world ifw inner join item i on ifw.item_id=i.id) on ifw.world_id=w.id\
        where i.id=%s", (id,)
    )
    _arcs = query("select a.id, a.name, a.description, a.story_id \
        from arc a inner join (item_featured_in ifa inner join item i on ifa.item_id=i.id) on ifa.arc_id=a.id\
        where i.id=%s", (id,)
    )

    return render_template('elements/item.jinja',
        author=session['user'], element=_item, worlds = _worlds, arcs=_arcs, table_name='item'
    )

@app.route('/organizations/<int:id>')
def organization(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    _org = query("select * from organization where id=%s", (id,), False)
    if not _org:
        return "Not Found",404

    return render_template(
        'elements/element_base.jinja', 
        author=session['user'], element=_org, table_name='organization'
    )

@app.route('/forms/<table_name>', methods=['GET', 'POST'])
def form(table_name):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    col_names = get_col_names(table_name)
    if request.method == 'GET':
        return fb.get_form(table_name, url_for('form', table_name=table_name))
    
    _form = request.form.to_dict()
    _form['author_id'] = session['user']['id']

    tup = ()
    for col_name in col_names:
        if col_name['COLUMN_NAME'] in _form:
            cn = col_name['COLUMN_NAME']
            if (cn == 'location_id' or cn == 'race_id') and _form[cn] == '0':
                tup += (None,)
                continue
            o = _form[cn]
            if type(o) is str:
                o = o.strip()
                if o == '':
                    o = None
            tup += (o,)
        else:
            tup += (None,)
    
    sql = f"insert into {table_name} values %s"
    try:
        query(sql, [tup])
        mysql.connection.commit()
    except MySQLdb.Error as e:
        flash(e.args[1])
        mysql.connection.rollback()
        return fb.get_form(table_name, url_for('form', table_name=table_name), _form)

    return redirect(url_for('profile', id=session['user']['id']))

@app.route('/<table_name>/<int:record_id>/update', methods=['GET', 'POST'])
def update(table_name, record_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    sql = f"select * from {table_name} where id=%s"
    existing = query(sql, (record_id,), False)

    if request.method == 'GET':
        if not existing:
            return "Not Found",404
        if existing['author_id'] != session['user']['id']:
            return "Forbidden", 403
        return fb.get_form(table_name, 
            url_for('update', table_name=table_name, record_id=record_id), existing)
    
    form = request.form.to_dict()
    temp = ""
    tup = ()
    col_names = get_col_names(table_name)
    for col_name in col_names:
        if col_name['COLUMN_NAME'] in form:
            cn = col_name['COLUMN_NAME']
            temp += f"{cn} = %s, "
            if (cn == 'location_id' or cn == 'race_id') and form[cn] == '0':
                tup += (None,)
                continue
            o = form[cn]
            if type(o) == str:
                o = o.strip()
                if o == '':
                    o = None 
            tup += (o,)
    tup += (record_id,)
    sql = f"update {table_name} set " + temp.strip(", ") + " where id = %s"

    try:
        query(sql, tup)
        mysql.connection.commit()
    except MySQLdb.Error as e:
        flash(e.args[1])
        mysql.connection.rollback()
        return fb.get_form(table_name, 
            url_for('update', table_name=table_name, record_id=record_id), existing)

    return redirect(url_for(table_name, id=record_id))

@app.route('/<table_name>/<int:record_id>/delete', methods=['POST'])
def delete(table_name, record_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    sql = f"select * from {table_name} where id=%s"
    existing = query(sql, (record_id,), False)
    if not existing:
        return "Not Found",404
    if existing['author_id'] != session['user']['id']:
        return "Forbidden",403
    
    sql = f"delete from {table_name} where id=%s"
    
    try:
        query(sql, (record_id,))
        mysql.connection.commit()
    except MySQLdb.Error as e:
        flash(e.args[1])

    return redirect(url_for('profile', id=session['user']['id']))

@app.route('/characters/<int:id>/<trait_name>')
def add_trait(id, trait_name):
    if 'user' not in session:
        return redirect(url_for('login'))

    existing = query("select * from traits where character_id=%s and name=%s", (id, trait_name))
    if existing:
        flash('A trait with that name already exists for this character')
        return redirect(url_for('characters', id=id))
    
