import crypt
from json import JSONEncoder
from db import db
import string
from hmac import compare_digest as compare_hash


class Author(db.Model):
    id = db.Column('userId', db.Integer, primary_key = True)
    user = db.Column(db.String(150),unique=True, nullable=False)
    password_hash = db.Column(db.String(150),nullable=False)
    rol = db.Column(db.Boolean, default=False,nullable=False)
    name = db.Column(db.String(150),nullable=False)
    city = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(250),nullable=False)
    
    def __init__(self, user: string, password: string,name: string, email: string, city: string , rol=False):
        self.user = user
        self.password_hash= crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
        self.rol = rol
        self.name = name
        self.city=city
        self.email = email
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def __iter__(self):
        yield 'id', self.id
        yield 'user', self.user
        yield 'rol', self.rol
        yield 'name', self.name
        yield 'city', self.city
        yield 'email', self.email
            
def validUser(userName, userPassword):
    authorAux = Author.query.filter_by(user=userName).first()
    if authorAux is None:
        return {"ans":"User not found"}
    return validPassword(password=userPassword,password_hash= authorAux.password_hash)
def getUser(idUser):
    authorAux = Author.query.filter_by(id=idUser).first()
    if authorAux is None:
        return False
    return authorAux
def validPassword(password: string, password_hash: string):
    if compare_hash(password_hash, crypt.crypt(password, password_hash)):
        return {"ans": True}
    return {"ans": "Bad Password"}

def deleteUser(id):
    try:        
        user = Author.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {"ans":True}
    except Exception as e:
        return {"error": e.args}
        
def changePassword(id,oldPass,newPass):
    try:
        user:Author
        user = Author.query.get(id)
        if validPassword(password=oldPass,password_hash=user.password_hash)["ans"] == True:
            user.password_hash=crypt.crypt(newPass, crypt.mksalt(crypt.METHOD_SHA512))
        db.session.commit()
        return dict(user)
    except Exception as e:
        return {"error": e.args}



def updateUser(user, id: int):
    try:
        userU:Author
        userU=Author.query.get(id)
        userU.name = user['user']
        userU.name = user['rol']
        userU.name = user['name']
        userU.name = user['city']
        userU.name = user['email']
        db.session.commit()
        return dict(userU)
    except Exception as e:
        return {"error": e.args}