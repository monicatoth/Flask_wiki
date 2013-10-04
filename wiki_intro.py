from flask import Flask, render_template, request, redirect
import time, datetime

app_wiki = Flask(__name__)

app_wiki.pages = {}
app_wiki.chronology = {}

@app_wiki.route('/', methods = ['GET', 'POST'])
def hello():
	if request.method == 'GET':
		return render_template('hello_wiki.html', num=0)
	else:
		# grabs the timestamp at the moment we receive the POST message
		epoch_ts = time.time()
		# now feeds this into app_wiki.pages
		wiki_title = request.form['title']
		wiki_content = request.form['content']
		wiki_excerpt = wiki_content[:100]
		app_wiki.chronology[wiki_title] = epoch_ts
		app_wiki.pages[wiki_title] = [wiki_excerpt, wiki_content]
		# wiki metadata
		num = len(app_wiki.pages)
		ordered_epochs = sorted(app_wiki.chronology.keys())
		# display new content
		return render_template('hello_wiki.html', num=num, order=ordered_epochs, pages=app_wiki.pages)

@app_wiki.route('/pages/<title>')
def loadpage(title):
	timestamp = app_wiki.chronology[title]
	excerpt, content = app_wiki.pages[title]
	legible_ts = datetime.datetime.fromtimestamp(timestamp).strftime('%m-%d %H:%M')
	return render_template('wiki_page.html', title=title, content=content, dt=legible_ts)

@app_wiki.route('/placeholder')
def placeholder():
	return render_template('dumb.html')

if __name__ == "__main__":
	app_wiki.run(debug = True)