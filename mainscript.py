from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sqlite3 import dbapi2 as sqlite3
import time, datetime
from wikiclass import *
from string import Template

wiki_app = Flask(__name__)

# ======================
# (Begin) Database Stuff

# Load default config
wiki_app.config.update(dict(
    DATABASE='sqlite/test.db',
    DEBUG=True,
    SECRET_KEY='call me ishmael',
    USERNAME='ishmael',
    PASSWORD='ishmael'
))

def connect_db():
    '''Connects to the specific database.'''
    rv = sqlite3.connect(wiki_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# This carries the danger of wiping my entries table
# def init_db():
#     '''Creates the database tables.'''
#     with wiki_app.app_context():
#         db = get_db()
#         with wiki_app.open_resource('sqlite/schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

def get_db():
    '''Opens a new database connection if there is none yet for the \n
    current application context.'''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@wiki_app.teardown_appcontext
def close_db(error):
    '''Closes the database again at the end of the request.'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# (End) Database Stuff
# ====================

@wiki_app.route('/', methods = ['GET', 'POST'])
def show_entries():
	if request.method == 'GET':
	    db = get_db()
	    cursor = db.execute('SELECT id, created, title, content FROM pages ORDER BY created DESC LIMIT 5')
	    entries = cursor.fetchall()
	    return render_template('show_entries.html', entries=entries)
	else:
		db = get_db()
		db.execute('insert into pages (title, content) values (?, ?)', [request.form['title'], request.form['content']])
		db.commit()
		#flash('New entry was successfully posted')
		return redirect(url_for('show_entries'))

@wiki_app.route('/edit/<id>', methods=['GET','POST'])
def edit_page(id):
	if request.method == 'GET':
	    db = get_db()
	    sub = Template('SELECT id, created, title, content FROM pages WHERE id = $num')
	    relevant_page = sub.substitute(num=id)
	    cursor = db.execute(relevant_page)
	    page = cursor.fetchone()
	    #return str(page)
	    return render_template('edit.html', page=page)
    #db.execute('update pages set title, content) values (?, ?)',
    #             [request.form['title'], request.form['content']])
    #db.commit()
    #flash('New entry was successfully posted')

@wiki_app.route('/success', methods=['POST'])
def success():
	if request.method == 'POST':
		db = get_db()
		sub = Template("UPDATE pages SET content = '$content' WHERE id = $page_id")
		page_id = request.form['id']
		page_content = request.form['content']
		sql = sub.substitute(content=page_content, page_id=page_id)
		db.execute(sql)
		db.commit()
		return render_template('success.html')
		return str(sql)

@wiki_app.route('/welcome')
def intro():
	return render_template('welcome.html', num=0)

@wiki_app.route('/placeholder')
def placeholder():
	return render_template('dumb.html')

if __name__ == "__main__":
	wiki_app.run(debug = True)