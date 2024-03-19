from . import db
from werkzeug.security import generate_password_hash

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) #python2
        except NameError:
            return str(self.id) #python3
        
    def __repr__(self):
        return '<User %r>' % (self.username)

class PropertyInfo(db.Model):
    __tablename__ = 'Property_Info'

    propertyid = db.Column(db.Integer, primary_key=True)
    propertytitle = db.Column(db.String(255))
    propertydescription = db.Column(db.String(1024))
    propertytype = db.Column(db.String(80))
    photo = db.Column(db.String(255))
    numberofbedrooms = db.Column(db.Integer())
    numberofbathrooms = db.Column(db.Integer())
    price = db.Column(db.Integer())
    propertylocation = db.Column(db.String(80))
    

    def __init__(self,propertytitle,propertydescription,numberofbedrooms,numberofbathrooms,propertylocation,price,propertytype,photo,):
        self.propertytitle = propertytitle
        self.propertydescription = propertydescription
        self.numberofbedrooms = numberofbedrooms
        self.numberofbathrooms = numberofbathrooms
        self.propertylocation = propertylocation
        self.price = price
        self.propertytype = propertytype
        self.photo = photo

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
    def __repr__(self):
        return '<Property %r>' % (self.propertytitle)

#ppty = PropertyInfo(propertytitle = "House 1", propertydescription = "Large House", numberofbedrooms = "3", numberofbathrooms = "4", propertylocation = "1 Ring Road", price = "50000000", propertytype = "House", photo = "house.jpeg")