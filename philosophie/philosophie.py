#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, url_for
from getpage import getPage

app = Flask(__name__)

app.secret_key = "why would I tell you my secret key?"
#app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def index():
	
    return render_template('index.html', message="Start your journey!")

@app.route('/newgame', methods=['POST'])
def newgame():
    if request.method == 'POST':
    	
        session['article'] = request.form['start']
        session['steps'] = 0 
        session['history'] = [] 
        session['history'].append(session['article'])
       	return redirect(url_for('game'))
    error = None
    return redirect(url_for('game'))  

@app.route('/game', methods=['GET','POST'])
def game():
	#5.1
	if session['article'] in session['links'] or session['steps']==0:
		session['title'], session['links'] = getPage(session['article'])
	else:
		flash(u"This page leads nowhere. Please kindly chose another page",'info')
		return redirect(url_for('index'))

	#5.3
	if session['steps'] == 0:
		if session['title']== "Philosophie" or session['title'] == None:
			flash(u"Please chose another page to start.",'warning')
			return redirect(url_for('index',message="Not Found"))
   #5.2
	if session['title'] == None :
		flash(u"Sorry, this page goes nowhere.",'warning')
		return redirect(url_for('index',message="You lost!"))

	session['history'].append(session['title'])
	session['steps']=session['steps']+1

	if session['title'] == 'Philosophie' :
		flash(u"You win with " + str(session['steps'])+ " steps!",'success')
		flash(u"Scores: "+ str(session['steps']), 'success')
		flash(u"Here is your itinerary: "+ str(session['history']),'success')
		return redirect(url_for('index',message="You win!"))

	return render_template('game.html', title=session['title'], links=session['links'])


@app.route('/move', methods=['POST'])
def move():
	session['article']=request.form['destination']
	return redirect(url_for('game')) 


if __name__ == '__main__':
    app.run(debug=True)

