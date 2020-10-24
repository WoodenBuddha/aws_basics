from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SubscriptionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Subscribe')


class UnsubscriptionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Unsubscribe')