from flask import render_template, session
from flask_mysqldb import MySQL, MySQLdb

class form_builder:
    def __init__(self, mysql : MySQL, db_name) -> None:
        self.mysql = mysql
        self.db_name = db_name
        self.mapper = {
            'arc':self.arc_form,
            'characters':self.character_form,
            'item':self.item_form,
            'location':self.location_form,
            'race':self.race_form,
            'story':self.story_form,
            'world':self.world_form,
            'organization':self.organization_form,
            'traits':self.trait_form,
        }
    
    def get_form(self, table_name, post_addr, existing=None):
        return self.mapper[table_name](table_name, post_addr, existing)

    def arc_form(self, table_name, post_addr, existing):
        return render_template(
            'forms/form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing
        )
    def character_form(self, table_name, post_addr, existing):
        race_list = self.query('select id, name from race where author_id=%s',(session['user']['id'],))
        return render_template(
            'forms/character_form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing,
            race_list=race_list
        )
    def item_form(self, table_name, post_addr, existing):
        return render_template(
            'forms/form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing
        )
    def location_form(self, table_name, post_addr, existing):
        location_list = self.query('select id, name from location where author_id=%s',(session['user']['id'],))
        return render_template(
            'forms/location_form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing,
            location_list=location_list
        )
    def race_form(self, table_name, post_addr, existing):
        return render_template(
            'forms/form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing
        )
    def story_form(self, table_name, post_addr, existing):
        return render_template(
            'forms/form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing
        )
    def world_form(self, table_name, post_addr, existing):
        return render_template(
            'forms/form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing
        )
    def organization_form(self, table_name, post_addr, existing):
        character_list = self.query('select id, name from characters where author_id=%s',(session['user']['id'],))
        location_list = self.query('select id, name from location where author_id=%s',(session['user']['id'],))
        return render_template(
            'forms/organization_form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing,
            location_list=location_list, character_list=character_list
        )
    def trait_form(self, table_name, post_addr, existing):
        return render_template(
            'forms/form.jinja', author=session['user'], table_name=table_name, 
            columns = self.get_col_names(table_name), post_addr=post_addr, existing=existing
        )
    
    def query(self, q : str, t : tuple, l = True, d=True):
        if d:
            cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        else:
            cur = self.mysql.connection.cursor()
        cur.execute(q, t)
        if l:
            res = cur.fetchall()
        else:
            res = cur.fetchone()
        cur.close()
        return res

    def get_col_names(self, table_name):
        col = self.query("select column_name \
            from information_schema.columns \
            where table_schema=%s and table_name=%s order by ordinal_position", 
            (self.db_name, table_name),
        )
        return col