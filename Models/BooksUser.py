from db import db
import string

class BooksUser(db.Model):
    userId = db.Column('userId',db.Integer, db.ForeignKey('author.userId'),primary_key = True)
    bookId = db.Column('bookId',db.Integer, db.ForeignKey('book.bookId'),primary_key = True)
    
    def __init__(self, userId, bookId):
        self.title = userId
        self.bookId=bookId