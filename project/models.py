import enum

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)

    course_users = db.relationship(
        'CourseUser', lazy='select',
        backref=db.backref('user', lazy='joined'))

    def __repr__(self):
        return '<User %r>' % self.username


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)

    course_users = db.relationship(
        'CourseUser', lazy='select',
        backref=db.backref('course', lazy='joined'))

    def __repr__(self):
        return '<Course %r>' % self.code


class UserType(enum.Enum):
    STUDENT = 's'
    INSTRUCTOR = 'i'


class CourseUser(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True)
    course = db.Column(db.ForeignKey('course.id'), primary_key=True)
    user_type = db.Column(db.Enum(UserType), nullable=False, default=UserType.STUDENT)
    lecture = db.Column(db.String(32), nullable=False)
    section = db.Column(db.String(32), nullable=False)
    dropped = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return '<CourseUser %r [%r]>' % (self.user, self.course)
