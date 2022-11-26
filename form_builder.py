from flask import render_template, session
from flask_mysqldb import MySQL
from dummydb import db_get_columns

class form_builder:
    def __init__(self, mysql : MySQL) -> None:
        self.mysql = mysql
    
    def get_form(self, table_name):
        return render_template(
            'forms/form.jinja', author=session['user'], 
            table_name=table_name, columns = db_get_columns(table_name)
        )

    def character_form(self):
        return render_template('forms/character_form.jinja', user=session['user'])