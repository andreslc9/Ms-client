from app import db

class Client(db.Model):
    __tablename__ = 'abcall_client'
    
    id = db.Column(db.Integer, primary_key=True)
    nit = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
