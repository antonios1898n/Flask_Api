from . import db
from sqlalchemy.sql import func

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(200),nullable=False)
    password =db.Column(db.String(250),nullable=False)
    created_at= db.Column(db.DateTime(timezone=True),server_default=func.now())
    tasks = db.relationship("Tasks",backref="Users")

    def __repr__(self):
        return f'<User {self.name} {self.id}'

class Tasks(db.Model):
    __tablename__ = "Tasks"
    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer,db.ForeignKey("Users.id"))
    title =  db.Column(db.String(100),nullable=False)
    description =  db.Column(db.String(250),nullable=True)
    completed =  db.Column(db.Boolean,nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)  # Priority of the task
    due_date = db.Column(db.DateTime(timezone=True))  # Due date of the task
    category = db.Column(db.String(50),nullable=True)  # Category of the task
    created_at= db.Column(db.DateTime(timezone=True),server_default=func.now())

    @property
    def serialize(self):
        return{
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "completed":self.completed,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "category": self.category,
            "created_at":self.created_at,
        }
    def __repr__(self):
        return f'<Task {self.title} {self.id}'