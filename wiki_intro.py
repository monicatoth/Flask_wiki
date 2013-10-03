from flask import Flask, render_template, request, redirect
import time, datetime

app_wiki = Flask(__name__)

app_wiki.pages = {}

@app_wiki.route('/', methods = ['GET', 'POST'])
def hello():
	if request.method == 'GET':
		return render_template('hello_wiki.html', num=0)
	else:
		# grabs the timestamp at the moment we receive the POST message
		epoch_ts = time.time()
		legible_ts = datetime.datetime.fromtimestamp(epoch_ts).strftime('%m-%d %H:%M')
		# now feeds this into app_wiki.pages
		app_wiki.pages[epoch_ts] = [request.form['title'], request.form['content']]
		wiki_title = request.form['title']
		wiki_content = request.form['content']
		# wiki metadata
		num = len(app_wiki.pages)
		return render_template('hello_wiki.html', num=num, pages=app_wiki.pages)

		# return 'On: %s <br> You asked for title: %s <br> And you asked for content: %s'%(legible_ts, wiki_title, wiki_content)


if __name__ == "__main__":
	app_wiki.run(debug = True)