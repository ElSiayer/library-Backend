import datetime
from flask import Flask, jsonify, request
from Models.Author import *
from Models.Book import *
from Models.Category import *
from db import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import jsonify


app = Flask(__name__)
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testUser:TestUser1234@localhost/dbTest'
##
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
##
app.config["JWT_SECRET_KEY"] = "JWT-FirstProyect"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=30)
jwt = JWTManager(app)


db.init_app(app)
        

@app.route("/")
def hello_world():
    return "<h1>Back End Up! :v</h1>"

###User Apis ###

@app.route("/signin", methods=(['POST']))
def login():
    auxAns = validUser(userName=request.json.get('username'),userPassword=request.json.get('password'))
    if auxAns['ans'] == True:
        access_token = create_access_token(identity=request.json.get('username'))
        return jsonify(access_token=access_token)
    return jsonify(auxAns)

@app.route("/signup", methods=(['POST']))
def register():
    newUser= Author(user=request.json.get('username'),password=request.json.get('password'),name=request.json.get('name'),email=request.json.get('email'),city=request.json.get('city'))
    newUser.save()
    return dict(newUser)

@app.route("/changePassword", methods=['POST'])
@jwt_required()
def changePass():
    try:
        res = changePassword(oldPass=request.json.get('oldPass'),newPass=request.json.get('newPass'), id= request.json.get('id'))
        if "error" in res.keys():
            return res
        return res
    except Exception as e:
        return {"msg": e.args}

@app.route("/updateUser", methods=['POST'])
@jwt_required()
def editUser():
    try:
        user = {"user":request.json.get('user'), "rol": request.json.get('rol'),
        "name":request.json.get('name'),"city":request.json.get('city'),"email": request.json.get('email')}
        res = updateUser(user=user, id= request.json.get('id'))
        if "error" in res.keys():
            return res        
        return res
    except Exception as e:
        return {"msg": e.args}

@app.route("/removeUser", methods=['GET'])
@jwt_required()
def removeUser():
    try:
        res = deleteUser(request.args.get('id'))
        if "error" in res.keys():
            return res        
        return res
    except Exception as e:
        return {"msg": e.args}
        

###Book Apis ###


@app.route("/updateBook", methods=['POST'])
@jwt_required()
def editBook():
    try:
        book = {"title":request.json.get('title'), "description": request.json.get('description')
        ,"categoryId":request.json.get('categoryId'),
        "img":request.json.get('img'),"doc":request.json.get('doc'),"authors":[],"rating": request.json.get('rating')}
        for idAuthor in request.json.get('authors'):
            book["authors"].append(getUser(idAuthor))
            res = updateBook(book, id=request.json.get('id'))
        if "error" in res.keys():
            return res        
        return res
    except Exception as e:
        return {"msg": e.args}

@app.route("/removeBook", methods=['GET'])
@jwt_required()
def removeBook():
    try:
        res = deleteBook(request.args.get('id'))
        if "error" in res.keys():
            return res        
        return res
    except Exception as e:
        return {"msg": e.args}

@app.route("/getBooksForUser", methods=['GET'])
@jwt_required()
def allBooksForUser():
    try:
        aux = []
        for item in getAllBooksForUsers(id=int(request.args.get('id'))):
            aux.append(dict(item))
        return {"books":aux}
    except Exception as e:
        return {"msg": e.args}

@app.route("/getBooksUser", methods=['GET'])
@jwt_required()
def getBooksUser():
    try:
        aux = []
        for item in getAllBooksOfUser(id=int(request.args.get('id'))):
            aux.append(dict(item))
        return {"books":aux}
    except Exception as e:
        return {"msg": e.args}

@app.route("/getAllBooks", methods=['GET'])
@jwt_required()
def allBooks():
    try:
        aux = []
        for item in getAllBooks():
            aux.append(dict(item))
        return {"books":aux}
    except Exception as e:
        return {"msg": e.args}
    

@app.route("/newBook", methods=['POST'])
@jwt_required()
def addBook():        
    newBook = Book(title=request.json.get('title'), description=request.json.get('description')
    ,categoryId=int(request.json.get('categoryId')),
    img=request.json.get('img'),doc=request.json.get('doc'))
    for idAuthor in request.json.get('authors'):
        newBook.authors.append(getUser(idAuthor))
    newBook.save()
    return dict(newBook)


###Category Apis ###


@app.route("/newCategory", methods=['POST'])
@jwt_required()
def addCategory():
    newCategory = Category(name=request.json.get('name'))
    newCategory.save()
    return  dict(newCategory)

@app.route("/Categories", methods=['GET'])
@jwt_required()
def getAllCategories():
    return {"ans": getCategories()}

@app.route("/updateCategory", methods=['POST'])
@jwt_required()
def editCategory():
    try:
        res = updateCategory(name=request.json.get('name'), id= request.json.get('id'))
        if "error" in res.keys():
            return res        
        return res
    except Exception as e:
        return {"msg": e.args}

@app.route("/removeCategory", methods=['GET'])
@jwt_required()
def removeCategory():
    try:
        res = deleteCategory(request.args.get('id'))
        if "error" in res.keys():
            return res        
        return res
    except Exception as e:
        return {"msg": e.args}

with app.app_context():
    db.create_all()
    #db.drop_all()