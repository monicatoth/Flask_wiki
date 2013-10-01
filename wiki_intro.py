from flask import Flask, render_template, request, redirect
app_wiki = Flask(__name__)

app_wiki.vars = {}
app_wiki.pages = {}

@app_wiki.route('/', methods = ['GET', 'POST'])
def hello():
	if request.method == 'GET':
		return render_template('hello_wiki.html')
	else:
		return "You haven't coded the POST option yet!"

if __name__ == "__main__":
	app_wiki.run(debug = True)