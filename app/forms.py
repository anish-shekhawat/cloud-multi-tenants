from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class LoginForm(Form):
    """Login form to access writing and settings pages"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ProjectForm(Form):
    """Form to create projects"""
    projectname = StringField('ProjectName', validators=[DataRequired()])
    projectdescription = TextAreaField('ProjectDescription', validators=[DataRequired()])

class InviteForm(Form):
    inviteusers = SelectField('InviteUsers')
