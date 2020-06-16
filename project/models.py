import enum

from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


metadata = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64))

    course_users = db.relationship(
        'CourseUser', lazy='select',
        backref=db.backref('user', lazy='joined'))

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)

    course_users = db.relationship(
        'CourseUser', lazy='select',
        backref=db.backref('course', lazy='joined'))

    def __repr__(self):
        return '<Course {}>'.format(self.username)


class UserType(enum.Enum):
    STUDENT = 'Student'
    INSTRUCTOR = 'Instructor'


class CourseUser(db.Model):
    __tablename__ = 'course_user'

    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.ForeignKey('course.id'), primary_key=True)
    user_type = db.Column(db.Enum(UserType), nullable=False, default=UserType.STUDENT)
    lecture = db.Column(db.String(32))
    section = db.Column(db.String(32))
    dropped = db.Column(db.Boolean(), nullable=False, default=False)

    def is_instructor(self):
        '''Returns whether this course user is an instructor.'''
        return self.user_type == CourseUser.INSTRUCTOR

    def __repr__(self):
        return '<CourseUser {} [{}]>'.format(self.user.username, self.course.code)
