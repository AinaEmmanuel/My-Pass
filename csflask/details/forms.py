from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo,Length, Email, ValidationError

class DetailForm(FlaskForm):
    sitename = StringField('Platform', validators=[DataRequired()])
    siteusername = StringField('Username (optional)')
    siteemail = StringField('Email', validators=[DataRequired(), Email()])
    sitepassword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add account')

class Admin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('ADMIN')