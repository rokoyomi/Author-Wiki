from flask import render_template, session
from flask_mysqldb import MySQL

class form_builder:
    def __init__(self, mysql : MySQL) -> None:
        self.mysql = mysql
    
    def get_form(self, table_name):
        return self.character_form()

    def character_form(self):
        return render_template('forms/character_form.jinja', user=session['user'])