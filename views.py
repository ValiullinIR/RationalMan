from app import app
from flask import render_template
from models import User, Admin, Petition, Solution, Expenses, Introduction, Comment


@app.route('/')
def Index():
    return render_template('base.html')