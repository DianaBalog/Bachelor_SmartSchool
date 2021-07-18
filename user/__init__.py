from flask import Flask, Blueprint, request, session
from flask_pymongo import PyMongo
import bcrypt
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from datetime import datetime, timedelta
from flask import current_app
import config

jwt = config.jwt
mongo = config.mongo

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/register', methods=['POST'])
def register():
    """
        user register function
        params: username, password, firstName, lastName
    """
    ok = 1
    username = request.json.get('username')
    password = request.json.get('password')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')

    users = mongo.db.users
    # if that username exists, it returns an error, else the new user is added in the database
    existing_user = users.find_one({'username': username})
    if existing_user is None:

        image = "data:image/svg+xml;base64,PHN2ZyBpZD0iZTU5ZWRiODYtYTNiYy00Njk0LThhYWMtMzFlNTY1Y2E1Y2ZjIiBkYXRhLW5hbWU9IkxheWVyIDEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjY3NiIgaGVpZ2h0PSI2NzYiIHZpZXdCb3g9IjAgMCA2NzYgNjc2Ij48dGl0bGU+bWFsZV9hdmF0YXI8L3RpdGxlPjxwYXRoIGQ9Ik05MzgsNDUwYTMzNi44NTIsMzM2Ljg1MiwwLDAsMS0yNy4yMiwxMzMuMUw5MDkuNjYsNTg1LjY4QTMzOC41NTksMzM4LjU1OSwwLDAsMSw1NDEuMzUsNzgyLjkzcS0zLjA0NS0uNTQtNi4wOC0xLjEyYTMzNC45ODExMSwzMzQuOTgxMTEsMCwwLDEtNjEuMTQtMTguMDNxLTQuODE1LTEuOTM1LTkuNTYtNC4wMWMtMi4xNi0uOTQtNC4zMi0xLjkxLTYuNDYtMi45MUEzMzguNDE0MjQsMzM4LjQxNDI0LDAsMCwxLDI2Miw0NTBjMC0xODYuNjcsMTUxLjMzLTMzOCwzMzgtMzM4UzkzOCwyNjMuMzMsOTM4LDQ1MFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yNjIgLTExMikiIGZpbGw9IiM0ZDk2YjgiLz48cGF0aCBkPSJNNTQxLjM1LDc4Mi45M3EtMy4wNDUtLjU0LTYuMDgtMS4xMmMtMS4zMi0zOC4zMS01Ljg1LTExNi45NC0yMS4zMDAwNS0xOTkuMjlDNTA1LjUyLDUzNy40NSw0OTMuNzksNDkxLjI1LDQ3Ny41Miw0NDkuOTVhNDEyLjYwMzg3LDQxMi42MDM4NywwLDAsMC0xOS4wNy00MS44NGMtMTYuNDQtMzEuMDUtMzYuMzgtNTcuMTktNjAuNTYtNzQuOWwzLjU2LTQuODZxMzAuMTY1LDIyLjExLDU0LjIyLDYyLjA4LDcuMjE1LDExLjk3LDEzLjg2MDA1LDI1LjU0LDcuMTI1LDE0LjUyLDEzLjU5LDMwLjgzLDQuMTI1LDEwLjM4LDcuOTcsMjEuNDgsMTYuNzQsNDguMTk1LDI4LjQ2LDEwOS45OCwyLjU5NTA2LDEzLjY1LDQuOTQsMjcuOTdDNTM2LjYsNjgwLjIsNTQwLjI1LDc0OC41OSw1NDEuMzUsNzgyLjkzWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTI2MiAtMTEyKSIgb3BhY2l0eT0iMC4yIi8+PHBhdGggZD0iTTQ2NC41Nyw3NTkuNzdjLTIuMTYtLjk0LTQuMzItMS45MS02LjQ2LTIuOTEtMi4wOS0yMi43LTUuOTMtNTAuODYtMTIuOTUtNzcuNTlBMjU0LjU1NjY2LDI1NC41NTY2NiwwLDAsMCw0MzMuMzUsNjQ0LjA3Yy04LjAxLTE4Ljc1LTE4LjM4LTM0LjY5LTMxLjc5LTQ0LjUybDMuNTYtNC44NWMxNC4wNCwxMC4yOCwyNC44NywyNi41MywzMy4yNCw0NS41NCw5LjQzLDIxLjQyLDE1LjcyLDQ2LjM1LDE5LjkxLDcwLjE3QzQ2MS4zOCw3MjguMSw0NjMuMzQsNzQ1LjE5LDQ2NC41Nyw3NTkuNzdaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjYyIC0xMTIpIiBvcGFjaXR5PSIwLjIiLz48Y2lyY2xlIGN4PSIxMDIuMjYxNzQiIGN5PSIxOTAuOTgxNjciIHI9IjMwLjA4ODU3IiBvcGFjaXR5PSIwLjIiLz48Y2lyY2xlIGN4PSIxMTEuOTUxNCIgY3k9IjQ0OS45OTA4MyIgcj0iMzAuMDg4NTciIG9wYWNpdHk9IjAuMiIvPjxwYXRoIGQ9Ik00ODMuNzE0NDksMzUzLjUyMTM5Yy02LjM4MDQ2LDM1Ljk5NzMyLDcuNzA0NTYsNjguNTkyMjUsNy43MDQ1Niw2OC41OTIyNXMyNC40Mjk3OS0yNS43NjgyNSwzMC44MTAyNS02MS43NjU1Ny03LjcwNDU3LTY4LjU5MjI1LTcuNzA0NTctNjguNTkyMjVTNDkwLjA5NDk0LDMxNy41MjQwNyw0ODMuNzE0NDksMzUzLjUyMTM5WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTI2MiAtMTEyKSIgb3BhY2l0eT0iMC4yIi8+PHBhdGggZD0iTTM4My43MTc2Niw0MzguOTcxMjJjMzQuMzM0OTQsMTIuNTU1LDY4LjgzNjc2LDQuNDk4LDY4LjgzNjc2LDQuNDk4cy0yMS4xNjYxMi0yOC40MTI3OS01NS41MDEwNi00MC45Njc4NC02OC44MzY3NS00LjQ5OC02OC44MzY3NS00LjQ5OFMzNDkuMzgyNzIsNDI2LjQxNjE3LDM4My43MTc2Niw0MzguOTcxMjJaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjYyIC0xMTIpIiBvcGFjaXR5PSIwLjIiLz48cGF0aCBkPSJNMzc3Ljg5NTM0LDY2OC4zMzNjMjQuMDY2LDguODAwMDgsNDguMjgzMTQsMy4wNTk0LDQ4LjI4MzE0LDMuMDU5NFM0MTEuMzc2ODcsNjUxLjM4NCwzODcuMzEwODYsNjQyLjU4MzlzLTQ4LjI4MzE0LTMuMDU5NC00OC4yODMxNC0zLjA1OTRTMzUzLjgyOTMzLDY1OS41MzI5MiwzNzcuODk1MzQsNjY4LjMzM1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yNjIgLTExMikiIG9wYWNpdHk9IjAuMiIvPjxjaXJjbGUgY3g9IjMzNy4zMDYwOCIgY3k9IjI4MS4wNzg4IiByPSIxMzEuNzcwMTQiIGZpbGw9IiNkMGNkZTEiLz48cGF0aCBkPSJNNTQ3LjgzMzM3LDQ5My45NjUzMXMxNi40NzEyNyw3OC4yMzg1MiwxNi40NzEyNyw4Ni40NzQxNSw3OC4yMzg1Miw0NS4yOTYsNzguMjM4NTIsNDUuMjk2TDcxMi41NDYsNjEzLjM4Miw3MzcuMjUzLDUzOS4yNjEyOXMtNDEuMTc4MTctNjEuNzY3MjUtNDEuMTc4MTctODYuNDc0MTVaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjYyIC0xMTIpIiBmaWxsPSIjZDBjZGUxIi8+PHBhdGggZD0iTTkxMC43OCw1ODMuMSw5MDkuNjYsNTg1LjY4QTMzOC41NTksMzM4LjU1OSwwLDAsMSw1NDEuMzUsNzgyLjkzcS0zLjA0NS0uNTQtNi4wOC0xLjEyYTMzNC45ODExMSwzMzQuOTgxMTEsMCwwLDEtNjEuMTQtMTguMDNxLTQuODE1LTEuOTM1LTkuNTYtNC4wMWMtMi4xNi0uOTQtNC4zMi0xLjkxLTYuNDYtMi45MWEzMzcuNTkyNzMsMzM3LjU5MjczLDAsMCwxLTU1LjI1LTMyLjI4bC0xNS42Mi00NS4zMSw4Ljc4LTYuNjk5OTUsMTguMDYtMTMuNzksMTkuMjctMTQuNzEsNS4wMS0zLjgzLDc1LjYxLTU3LjcyLDUuNTgtNC4yNiwzOS4zLTMwLC4wMS0uMDFzNDIuNSw2OS4yNSwxMDQuMjcsNDguNjYsNjAuNDItNzkuNjMsNjAuNDItNzkuNjNaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMjYyIC0xMTIpIiBmaWxsPSIjMmYyZTQxIi8+PHBhdGggZD0iTTQ4NS4wMzUzOCwyODYuOTE2czQxLjgzNjUzLTkwLjY0NTgxLDEyMi4wMjMyMS02OS43Mjc1NSwxMjUuNTA5NTgsNTIuMjk1NjYsMTI4Ljk5Niw4My42NzMwNi0xLjc0MzE5LDc4LjQ0MzQ4LTEuNzQzMTksNzguNDQzNDgtOC43MTYtNjQuNDk4LTY0LjQ5OC01MC41NTI0Ny0xNDIuOTQxNDcsMy40ODYzOC0xNDIuOTQxNDcsMy40ODYzOEw1MTIuOTI2NCw0NTcuNzQ4NDlzLTE1LjY4ODctMjIuNjYxNDUtMzMuMTIwNTgtOC43MTU5NFM0MjkuMjUzMzUsMzE0LjgwNyw0ODUuMDM1MzgsMjg2LjkxNloiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yNjIgLTExMikiIGZpbGw9IiMyZjJlNDEiLz48cGF0aCBkPSJNNDc0LjEzLDc2My43OHEtNC44MTUtMS45MzUtOS41Ni00LjAxYy0yLjE2LS45NC00LjMyLTEuOTEtNi40Ni0yLjkxYTMzOC44MzUsMzM4LjgzNSwwLDAsMS04Ny41OS01OC43YzkuMTktMTIuNTIsMTYuNzItMTguODksMTYuNzItMTguODloNjEuNzdsOS4yNiwzMS4xNFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yNjIgLTExMikiIGZpbGw9IiMyZjJlNDEiLz48cGF0aCBkPSJNODU2LjY3LDU3Ni4zMmw1Mi45OSw5LjM2QTMzNy45NDQzNCwzMzcuOTQ0MzQsMCwwLDEsODUyLjksNjc0LjI1WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTI2MiAtMTEyKSIgZmlsbD0iIzJmMmU0MSIvPjwvc3ZnPg=="

        hashpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert({'username': username, 'password': hashpassword, 'firstname': firstName, 'lastname': lastName, 'institution' : [], 'photo' : image})
        ok = 0
    else:
        ok = 1
    return {
        'register': ok
    }


@user.route('/login', methods=['POST'])
def login():
    """
        user login function
        params: username, password
    """
    
    username = request.json.get('username')
    password = request.json.get('password')

    users = mongo.db.users
    # check if an user with that username exists
    # if the user is valid, create a token and cookies
    login_user = users.find_one({'username': username})
    if login_user:
        if bcrypt.hashpw(password.encode('utf-8'), login_user['password']) == login_user['password']:
            # correct
            access_token = create_access_token(identity=username)
            response = jsonify({'login': '0',
                            'firstName': login_user['firstname'],
                            'lastName': login_user['lastname'],
                            'photo': login_user['photo']
                            })
            set_access_cookies(response, access_token)
            ok = 0
        else:
            # invalid password
            ok = 1
    else:
        # invalid user
        ok = 1
    
    if (ok == 0):
        return response
    else:
        return {
            'login': ok
        }


@user.route('/info', methods=['GET'])
@jwt_required(optional=True)
def userInfo():
    """
        return user info if is logged in
    """

    current_user = get_jwt_identity()
    if current_user == None:
         return {
            'ok' : '1'
        }
    users = mongo.db.users
    user = users.find_one({'username': current_user})
    if user:
        return {
            'ok' : '0',
            'firstName' : user['firstname'],
            'lastName' : user['lastname'],
            'photo' : user['photo']
        }
    else:
        return {
            'ok' : '1'
        }


@user.route('/logout', methods=['GET'])
def logout():
    """
        logout function
        remove cookies
    """ 
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response


@user.route('/editUserInfo', methods=['POST'])
@jwt_required()
def editUserInfo():
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    mycol = mongo.db["users"]

    if user is not None:
        edited_user = { "$set": { "firstname": firstName, "lastname": lastName } }
        mycol.update_one(user, edited_user)
        return {
            'ok': '0'
        }
    else:
        return {
            'ok': '1'
        }


@user.route('/changeUserPassword', methods=['POST'])
@jwt_required()
def changeUserPassword():
    currentPassword = request.json.get('currentPassword')
    password = request.json.get('password')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    mycol = mongo.db["users"]

    if user is not None:
        if bcrypt.hashpw(currentPassword.encode('utf-8'), user['password']) == user['password']:   
            if bcrypt.hashpw(password.encode('utf-8'), user['password']) != user['password']:
                hashpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                edited_user = { "$set": { "password": hashpassword } }
                mycol.update_one(user, edited_user)
                return {
                    'ok': '0'
                }
            else:
                return{
                    'ok': 'You can not change your password with your current password!'
                }
        else:
            return {
                'ok': 'Current password is incorrent!'
            }
    else:
        return {
            'ok': 'An unexpected error occurred!'
        }


@user.route('/editUserImage', methods=['POST'])
@jwt_required()
def editUserImage():
    image = request.json.get('image')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    mycol = mongo.db["users"]

    if user is not None:
        edited_user = { "$set": { "photo": image } }
        mycol.update_one(user, edited_user)
        return {
            'ok': '0'
        }
    else:
        return {
            'ok': '1'
        }


@user.route('/getUserImage', methods=['GET'])
@jwt_required()
def getUserImage():    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    if user is not None:
        return {
            'ok': '0',
            'image': user['photo']
        }
    else:
        return {
            'ok': '1'
        }
