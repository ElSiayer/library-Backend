from Models.Author import Author
from Models.BooksUser import BooksUser
from Models.Category import Category
from db import db
import string
import json


class Book(db.Model):
    id = db.Column('bookId', db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    categoryId = db.Column(db.Integer, db.ForeignKey(Category.id),nullable=False)    
    img = db.Column(db.String(300))
    doc = db.Column(db.String(300))
    rating = db.Column(db.Integer)
    authors = db.relationship('Author',secondary= 'books_user', backref='books')



    def __init__(self, title: string, description: string, categoryId: int ,img: string, doc: string):
        self.title = title
        self.description=description
        self.categoryId = categoryId
        self.img = img
        self.doc = doc
        self.rating = 0


    def __iter__(self):
        auxAuthors = []
        for item in self.authors:
            auxAuthors.append({"id":item.id, "name":item.name})
        yield 'id', self.id
        yield 'title', self.title
        yield 'description', self.description
        yield 'category', dict(self.category)
        yield 'authors', auxAuthors
        yield 'img', self.img
        yield 'doc', self.doc
        yield 'rating', self.rating

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
    
def updateBook(book, id: int):
    try:
        bookUp:Book
        bookUp=Book.query.get(id)
        bookUp.authors= book["authors"]
        bookUp.categoryId= book["categoryId"]
        bookUp.description= book["description"]
        bookUp.doc= book["doc"]
        bookUp.img= book["img"]
        bookUp.title= book["title"]
        bookUp.rating = book["rating"]
        db.session.commit()
        return dict(bookUp)
    except Exception as e:
        return {"error": e.args}

def getAllBooksForUsers(id: int):
    try:
        booksSelf = []
        booksAns = []
        for id in Book.query.with_entities(Book.id).join(BooksUser).filter(BooksUser.userId==id):
            booksSelf.append(id[0])
        for book in (db.session.query(Book).filter(Book.id.not_in(booksSelf))):
            booksAns.append(dict(book))       

    except Exception as e:
        return {"error": e.args}
    return booksAns

def getAllBooksOfUser(id: int):
    try:
        booksSelf = []
        for book in db.session.query(Book).join(BooksUser).filter(BooksUser.userId==id):
            booksSelf.append(dict(book))

    except Exception as e:
        return {"error": e.args}
    return booksSelf

def getAllBooks():
    try:
        booksAns = []
        for book in (Book.query.all()):
            booksAns.append(dict(book))
    except Exception as e:
        return {"error": e.args}
    return booksAns

def deleteBook(id):
    try:        
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        return {"ans":True}
    except Exception as e:
        return {"error": e.args}