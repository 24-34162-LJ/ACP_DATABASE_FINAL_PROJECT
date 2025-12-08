from flask_wtf import FlaskForm # this for security and the secret key
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateTimeLocalField, BooleanField # for the function each of this have their own action
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional # like role to make sure that data is valid

"""
- Datarequired() = make sure it have data
- length(min, max) = add role like example it must compose of that number of letter

to create a form you need this

class nameof the form(FlaskForm) - always use the FlaskForm is very important
      variable_name / function name    =  wtforms  ( - are like example stringfield which depend 
                                                         on the data we want to get 
        "legend", - this is the like a caption
        Validators=[DataRequired()] - this are is for like to make sure it have data to past                        
      )
      submit = SubmitField("Register") = always part of the form
"""

