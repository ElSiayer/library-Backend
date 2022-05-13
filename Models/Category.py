#from Models.Book import Book
import json
from unicodedata import category
from db import db
import string

class Category(db.Model, json.JSONDecoder):
    id = db.Column('categoryId', db.Integer, primary_key = True)
    name = db.Column(db.String(150),unique=True)
    books = db.relationship('Book', backref='category', lazy=True)

    def __init__(self, name: string):
        self.name = name
    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        #yield 'books', self.books

def getCategories():
    ans = []
    for item in Category.query.all():
        ans.append(dict(item))        
    return ans

def deleteCategory(id):
    try:        
        category = Category.query.get(id)
        db.session.delete(category)
        db.session.commit()
        return {"ans":True}
    except Exception as e:
        return {"error": e.args}
        
def updateCategory(name, id: int):
    try:
        category:Category
        category=Category.query.get(id)
        category.name = name
        db.session.commit()
        return dict(category)
    except Exception as e:
        return {"error": e.args}
