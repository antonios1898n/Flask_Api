from functools import wraps
import traceback

from Validations import TaskValidator
from . import app, db
from flask import request,make_response
from .models import Users,Tasks
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import datetime,timedelta

@app.route("/signup",methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    if name and password :
        user =Users.query.filter_by(name=name).first()
        if user:
            return make_response(
                {"message":"User already exists"},404
            )
        user = Users(
            name= name,
            password = generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
                {"message":"User Created"},200
            )
    return make_response(
        {"message":"Unable to create user"},500
    )
@app.route("/signin",methods=["POST"])
def login():
    auth = request.json
    if not auth or not auth.get("password") or not auth.get("name"):
        return make_response(
            {"message":"Proper credentials were not provided"},404
        )
    user = Users.query.filter_by(name=auth.get("name")).first()
    if not user:
        return make_response(
            {"message":"Please create an account"},404
        )
    if check_password_hash(user.password , auth.get('password')):
        token = jwt.encode({
            'id':user.id,
            'exp':datetime.now()+timedelta(minutes=30)
        },
        "secret",
        "HS256"
        )
        return make_response({'token':token},200)
    return make_response({'messgae',"Please check your credentials"},404)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'] 
        if not token:
            return make_response({
                "message":"Token is missing"
            },404)
        try:
            data=jwt.decode(token,"secret",algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(e)
            return make_response({
                "message":"Token is invalid"
            },404)
        return f(current_user,*args,**kwargs)
    return decorated
@app.route("/tasks", methods=["GET", "POST"])
@token_required
def createTasks(current_user):
    if request.method == "GET":
        tasks =Tasks.query.all()
        return make_response({"data":[
            task.serialize for task in tasks
        ]})
    elif request.method == "POST":
        try:
            data = request.json
            title = data.get("title")
            description = data.get("description")
            priority = data.get("priority")
            due_date = data.get("due_date")
            category = data.get("category")
            
            is_valid, errors = TaskValidator.validateTaskData(data)

            if not is_valid:
                # Handle validation errors
                error_messages = {"errors": errors}
                return make_response(error_messages, 400)
            if not title:
                return make_response(
                    {"message": "Title missing"}, 404
                )
            task = Tasks(
                title=title,
                description=description,
                completed=False,
                priority = priority,
                due_date = due_date,
                category = category,
                userId=current_user.id
            )
            if Tasks.query.filter_by(title = title,userId=current_user.id).first():
                return make_response(
                    {"message": "Task already exists"}, 404
                )
            db.session.add(task)
            db.session.commit()
            return make_response(
                {"message": "Task Created", "task": task.serialize}, 200
            )
        except Exception as e:
            traceback.print_exc()
            return make_response({"message": str(e)}, 500)
@app.route("/tasksByUser",methods=["GET"])
@token_required
def gettasksByUser(current_user):
    tasks = Tasks.query.filter_by(userId=current_user.id).all()
    return make_response({"data":[
        task.serialize for task in tasks
    ]})
@app.route("/tasksByUser/<int:id>", methods=["GET"])
@token_required
def getTaskByUserById(current_user, id):
    task = Tasks.query.filter_by(id=id, userId=current_user.id).first()
    if task:
        return make_response({"data": [task.serialize]})
    else:
        return make_response({"message": "Task not found"}, 404)

@app.route("/tasks/<int:id>", methods=["GET"])
def getTaskById(id):
    task = Tasks.query.filter_by(id=id).first()
    if task:
        return make_response({"data": [task.serialize]})
    else:
        return make_response({"message": "Task not found"}, 404)
@app.route("/tasksByCateg/<string:code>", methods=["GET","DELETE"])
def getTaskByCategCode(code):
    if request.method == "GET":
        tasks = Tasks.query.filter_by(category=code).all()
        if tasks:
            return make_response({"data": [task.serialize for task in tasks]})
        else:
            return make_response({"message": "Task not found"}, 404)
    elif request.method == "DELETE":
        tasks= Tasks.query.filter_by(category=code).all()
        if not tasks:
            return make_response({"message": "Task not found"}, 404)

        try:
            for task in tasks:
                db.session.delete(task)
            db.session.commit()
            return make_response({"message": "Task deleted successfully"}, 200)
        except Exception as e:
            return make_response({"message": str(e)}, 500)
@app.route("/tasks/<int:id>", methods=["PUT","DELETE"])
@token_required
def update_task(current_user, id):
    if request.method == "PUT":
        task = Tasks.query.filter_by(id=id, userId=current_user.id).first()
        if not task:
            return make_response({"message": "Task not found"}, 404)

        try:
            data = request.json
            title = data.get("title")
            description = data.get("description")
            completed = data.get("completed")
            priority = data.get("priority")
            due_date = data.get("due_date")
            category = data.get("category")

            if title:
                task.title = title
            if description:
                task.description = description
            if completed is not None:
                task.completed = completed
            if priority:
                task.priority = priority,
            if due_date:
                task.due_date = due_date,
            if category:
                task.category = category,

            db.session.commit()
            return make_response({"message": "Task updated successfully"}, 200)
        except Exception as e:
            return make_response({"message": str(e)}, 500)
    elif request.method == "DELETE":
        task = Tasks.query.filter_by(id=id, userId=current_user.id).first()
        if not task:
            return make_response({"message": "Task not found"}, 404)

        try:
            db.session.delete(task)
            db.session.commit()
            return make_response({"message": "Task deleted successfully"}, 200)
        except Exception as e:
            return make_response({"message": str(e)}, 500)
