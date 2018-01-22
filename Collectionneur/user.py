from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

''' User class '''

class User():
    def registeruser(username, hash1):
        # register user
        hash1 = pwd_context.hash(request.form.get("password"))
        rows=db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)", username=username, password=hash1)
        return True

    def changepassword(hash1, id):
        # update password
        db.execute("UPDATE users SET hash = :hash1 WHERE id= :id ",hash1 = hash1, id = id)
        # show index page
        return True

    def deleteaccount(id):
        # delete user
        db.execute("DELETE FROM users WHERE id= :id ", id = id)
        # show index/log in page
        return True

    def userexist(username):
        # return true if user exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        return rows

    def requestpassword(id):
        rows = db.execute("SELECT hash FROM users WHERE id = :id", id=id)
        return rows

    '''
    def mylists():
        username = db.execute("SELECT username FROM user WHERE id=:id", id = session["user_id"])
        lists = db.execute("SELECT list_name FROM lists WHERE owner=:username", username = username)
        return lists
    '''