from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
base_dir = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{base_dir}/sports.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False


class NFL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    score = db.Column(db.String(100))
    teams = db.Column(db.String(100))

    def __repr__(self):
        return f"({self.date})  {self.teams}"


class NBA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    score = db.Column(db.String(100))
    teams = db.Column(db.String(100))

    def __repr__(self):
        return f"({self.date})  {self.teams}"


class MLB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    score = db.Column(db.String(100))
    teams = db.Column(db.String(100))

    def __repr__(self):
        return f"({self.date})  {self.teams}"


class UFC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    result = db.Column(db.String(100))
    fighters = db.Column(db.String(100))
    winner = db.Column(db.String(100))

    def __repr__(self):
        return f"({self.date})  {self.fighters}"


if __name__ == "__main__":
    db.create_all()
