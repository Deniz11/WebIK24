from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from passlib.apps import custom_app_context as pwd_context
# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

''' User class '''

class User():
    def user(username):
        UserInfo = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        return UserInfo

    # register user
    def registeruser(username, hash1):
        hash1 = pwd_context.hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)", username=username, password=hash1)
        return True

    # update password
    def changepassword(hash1, id):
        db.execute("UPDATE users SET hash = :hash1 WHERE id= :id ",hash1 = hash1, id = id)
        # show index page
        return True

    # delete account
    def deleteaccount(username):

        # delete from community
        db.execute("DELETE FROM community_users WHERE username= :username ", username = username)

        # get list id
        list_id =  db.execute("SELECT id FROM lists WHERE owner= :username ", username = username)[0]["id"]

        # delete list items
        db.execute("DELETE FROM list_item WHERE list_id= :list_id", list_id = list_id)

        # delete list
        db.execute("DELETE FROM lists WHERE owner= :username ", username = username)

        #delete comments
        db.execute("DELETE FROM comment_section WHERE username= :username ", username = username)

        # delete user
        db.execute("DELETE FROM users WHERE username= :username ", username = username)

        # show index/log in page
        return True

    # check if user exists
    def userexist(username):
        # return row if username exists in users or community table
        UsernameCheck = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        CommunityNameCheck = db.execute("SELECT * FROM community_page WHERE name = :username", username=username)
        if len(UsernameCheck) == 0 or not len(CommunityNameCheck) == 0:
            return False
        else:
            return True

    # get user password
    def requestpassword(id):
        rows = db.execute("SELECT hash FROM users WHERE id = :id", id=id)
        return rows

    # get list id of user
    def get_list_id(username):
        return db.execute("SELECT * FROM lists WHERE owner = :username", username=username)[0]["id"]


    '''
    def mylists():
        username = db.execute("SELECT username FROM user WHERE id=:id", id = session["user_id"])
        lists = db.execute("SELECT list_name FROM lists WHERE owner=:username", username = username)
        return lists
    '''