from flask import request,jsonify
from datetime import datetime

from models import User, Admin, Petition, Solution, Expenses, Introduction, Comment
from app import app, db


@app.route('/petition', methods=['POST', 'GET'])
def Add_petition():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        desc = data.get('desc')
        solution_category = data.get('solution_category')
        solution_character = data.get('solution_character')
        rewards = data.get('rewards')
        expenses_name = data.get('expenses_name')
        expenses_sum = data.get('expenses_sum')
        introductions_stage = data.get('introduction_stage')
        introductions_days = data.get('introduction_days')
        petition = Petition(title, desc, rewards, solution_category,solution_character, 0)

        for i in range(0, len(expenses_name)):
            name = expenses_name[i]
            sum = expenses_sum[i]
            expense = Expenses(name=name, sum=sum)
            petition.expenses.append(expense)

        for i in range(0,len(introductions_stage)):
            stage = introductions_stage[i]
            days = introductions_days[i]
            introduction = Introduction(stage=stage, days=days)
            petition.introduction.append(introduction)

        try:
            db.session.add(petition)
            db.session.commit()
            return 'Success!', 200
        except:
            return 'DB adding error', 200

    elif request.method == 'GET':
        petitions = Petition.query.order_by(Petition.likes.desc())
        return jsonify(petitions=[i.serialize for i in petitions])

@app.route('/users', methods=['POST'])
def Users():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        father_name = data.get('father_name')
        date_of_birth = data.get('date_of_birth')
        date_of_birth = datetime.strptime(str(date_of_birth) + "T00:00", '%Y-%m-%dT%H:%M')
        position = data.get('position')
        education = data.get('education')
        experience = data.get('experience')
        phone = data.get('phone')

        user = User(first_name=first_name,
                    last_name=last_name,
                    father_name=father_name,
                    date_of_birth=date_of_birth,
                    position=position,
                    education=education,
                    experience=experience,
                    phone=phone)

        try:
            db.session.add(user)
            db.session.commit()
            return 'Success', 200
        except:
            return 'Error', 400

@app.route('/comments/<int:id>', methods=['POST', 'GET'])
def Comments(id):
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message')
        date_time = data.get('date_time')
        date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        user_id = data.get('user_id')

        user = User.query.filter_by(id_user=user_id).first()
        petition = Petition.query.filter_by(id_petition=id).first()

        comment = Comment(message=message, date_time=date_time, petition_id=petition.id_petition, user_id=user.id_user)

        try:
            db.session.add(comment)
            db.session.commit()
            return 'Success', 200
        except:
            return 'Comment adding error',400


    elif request.method == 'GET':
        comments = Comment.query.filter_by(petition_id=id)
        return jsonify(comments=[i.serialize for i in comments])

@app.route('/likes/<int:id>', methods=['PUT'])
def Like(id):
    if request.method == 'PUT':
        petition = Petition.query.filter_by(id_petition=id).first()
        likes_count = petition.likes
        petition.likes = likes_count + 1
        try:
            db.session.commit()
            return {
                'likes_count': likes_count+1
            }
        except:
            return "Like count Error", 400

