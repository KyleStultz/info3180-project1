from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    pass

class PropertyForm(FlaskForm):
    propertytitle = StringField("Property Title",validators=[DataRequired()])
    
    numberofbedrooms = IntegerField("Number of Bedrooms",validators=[DataRequired()])
    
    numberofbathrooms= IntegerField("Number of Bathrooms",validators=[DataRequired()])
    
    propertylocation = StringField("Location",validators=[DataRequired()])
    
    price = StringField("Price",validators=[DataRequired()])
    
    propertytype = SelectField("Property Type", validators=[DataRequired()], choices=[('apartment','Apartment'),('house','House')])
    
    propertydescription = StringField('Description', validators=[DataRequired()], widget=TextArea())
    
    photo = FileField("Photo", validators=[FileRequired(),FileAllowed(["jpg","jpeg","png","Images Only"])])