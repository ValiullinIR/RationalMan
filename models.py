from datetime import datetime

from app import db

users_petitions = db.Table('users_petitions',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id_user'), primary_key=True),
        db.Column('petition_id', db.Integer, db.ForeignKey('petition.id_petition'), primary_key=True)
        )

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    father_name = db.Column(db.String(32))
    date_of_birth = db.Column(db.DateTime, nullable=False)
    position = db.Column(db.String(32), nullable=False)
    education = db.Column(db.String(32))
    experience = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(16), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)
    petitions = db.relationship('Petition', secondary=users_petitions, backref=db.backref('user'), lazy='subquery')
    petition_id = db.Column(db.Integer, db.ForeignKey('petition.id_petition'), nullable=True)

    @property
    def serialize(self):
        return {
            "id_user": self.id_user,
            "first_name": self.first_name,
            "father_name": self.father_name,
            "date_of_birth": str(self.date_of_birth),
            "position": self.position,
            "education": self.education,
            "experience": self.experience,
            "rating": self.rating,
            "phone": self.phone
        }


class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    position = db.Column(db.String(32), nullable=False)

    @property
    def serialize(self):
        return {}

class Petition(db.Model):
    id_petition = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(256))
    solution_category = db.Column(db.String(32), nullable=False)
    solution_character = db.Column(db.String(256))
    likes = db.Column(db.Integer, default=0)
    rewards = db.Column(db.Integer, default=0)
    expenses = db.relationship('Expenses', backref='petition', lazy=True)
    introduction = db.relationship('Introduction', backref='petition', lazy=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id_solution'), nullable=True)
    solution = db.relationship('Solution', backref='petition', lazy=True)
    authors = db.relationship('User', secondary=users_petitions, backref=db.backref('petition'), lazy='subquery')

    @property
    def serialize(self):
        return {
            "id_petition": self.id_petition,
            "title": self.title,
            "desc": self.desc,
            "solution_category": self.solution_category,
            "solution_character": self.solution_character,
            "likes": self.likes,
            "rewards": self.rewards,
            "expenses_name": [i.serialize for i in self.expenses],
            "introduction": [i.serialize for i in self.introduction]
        }

    def __init__(self, title, desc, rewards, solution_category, solution_character, likes):
        self.title = title
        self.desc = desc
        self.rewards = rewards
        self.solution_category = solution_category
        self.solution_character = solution_character
        self.likes = likes

class Solution(db.Model):
    id_solution = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow())

    @property
    def serialize(self):
        return {
            "id_solution":self.id_solution,
            "status": self.status,
            "date_time": str(self.date_time)
        }


class Expenses(db.Model):
    id_expenses = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    sum = db.Column(db.Integer, default=0)
    solution = db.Column(db.Integer, db.ForeignKey('petition.id_petition'), nullable=False)

    @property
    def serialize(self):
        return {
            "id_expenses": self.id_expenses,
            "name": self.name,
            "sum" : self.sum,
        }


class Introduction(db.Model):
    id_introduction = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(64), nullable=False)
    days = db.Column(db.Integer, default=0)
    solution = db.Column(db.Integer, db.ForeignKey('petition.id_petition'), nullable=False)

    @property
    def serialize(self):
        return {
            "id_introduction": self.id_introduction,
            "stage": self.stage,
            "days": self.days
        }

class Comment(db.Model):
    id_comment = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text(256))
    date_time = db.Column(db.DateTime, default=datetime.utcnow())
    petition_id = db.Column(db.Integer, db.ForeignKey('petition.id_petition'), nullable=False)
    petition = db.relationship('Petition',backref=db.backref('comments', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)

    @property
    def serialize(self):
        return {
            "id_comment": self.id_comment,
            "message": self.message,
            "date_time": str(self.date_time),
            "petition_id": self.petition_id,
            "user_id": self.user_id
        }