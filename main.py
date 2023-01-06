from flask import Flask, request
import pymysql

from models.registerRequestModel import register_request_model_from_dict
from responseBuilder import ResponseBuilder
from utils.constants import StatusCodes

app = Flask(__name__)


def getMySqlConnection():
    return pymysql.connect(host='localhost', port=3306, user='root', password='', db="azreel", autocommit=True)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/api/v1/login", methods=['POST', 'GET'])
def apiLogin():
    if request.method == "POST":
        requestObj = request.json
        connection = getMySqlConnection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s',
                           (requestObj['email'], requestObj['password']))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return ResponseBuilder.loginResponseBuilder(user), StatusCodes.STATUS_OK
            else:
                return "User Not Found", StatusCodes.STATUS_NOT_FOUND
        except pymysql.Error as e:
            return "SOMETHING WENT WRONG " + str(e), StatusCodes.SOMETHING_WENT_WRONG
    else:
        return "METHOD NOT ALLOWED", StatusCodes.METHOD_NOT_ALLOWED


@app.route("/api/v1/register", methods=['POST', 'GET'])
def apiRegister():
    if request.method == "POST":
        requestObj = request.json
        requestModel = register_request_model_from_dict(requestObj)
        connection = getMySqlConnection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s',
                           (requestModel.email, requestModel.password))
            user = cursor.fetchone()
            if not user:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO users (firstname,lastname,phone,age,email,password) VALUES '
                               '(%s,%s,%s,%s,%s,%s)',
                               (requestModel.first_name, requestModel.last_name, requestModel.phone, requestModel.age,
                                requestModel.email, requestModel.password))
                cursor.close()
                return "USER REGISTERED SUCCESSFULLY", StatusCodes.STATUS_OK
            else:
                return "USER EMAIL ALREADY EXIST", StatusCodes.USER_ALREADY_EXIST
        except pymysql.Error as e:
            return "SOMETHING WENT WRONG " + str(e), StatusCodes.SOMETHING_WENT_WRONG
    else:
        return "METHOD NOT ALLOWED", StatusCodes.METHOD_NOT_ALLOWED


@app.route("/api/v1/updateProfile", methods=['POST', 'GET'])
def updateProfile():
    if request.method == "POST":
        requestObj = request.json
        requestModel = register_request_model_from_dict(requestObj)
        connection = getMySqlConnection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s',
                           requestModel.email)
            user = cursor.fetchone()
            if user:
                cursor = connection.cursor()
                cursor.execute('UPDATE users SET firstname = %s,lastname = %s,phone = %s ,age =%s ,password = %s '
                               'WHERE email = %s',
                               (requestModel.first_name, requestModel.last_name, requestModel.phone, requestModel.age,
                                requestModel.password, requestModel.email))
                cursor.close()
                return "USER UPDATED SUCCESSFULLY", StatusCodes.STATUS_OK
            else:
                return "INVALID USER EMAIL", StatusCodes.USER_ALREADY_EXIST
        except pymysql.Error as e:
            return "SOMETHING WENT WRONG " + str(e), StatusCodes.SOMETHING_WENT_WRONG
    else:
        return "METHOD NOT ALLOWED", StatusCodes.METHOD_NOT_ALLOWED


@app.route("/api/v1/getUserProfile", methods=['POST', 'GET'])
def getUserProfile():
    if request.method == "POST":
        requestObj = request.json
        connection = getMySqlConnection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s',
                           requestObj['email'])
            user = cursor.fetchone()
            if user:
                res = ResponseBuilder.loginResponseBuilder(user)
                res['password'] = user[6]
                return res, StatusCodes.STATUS_OK
            else:
                return "INVALID USER EMAIL", StatusCodes.USER_ALREADY_EXIST
        except pymysql.Error as e:
            return "SOMETHING WENT WRONG " + str(e), StatusCodes.SOMETHING_WENT_WRONG
    else:
        return "METHOD NOT ALLOWED", StatusCodes.METHOD_NOT_ALLOWED


@app.route("/api/v1/changeUserPassword", methods=['POST', 'GET'])
def changeUserPassword():
    if request.method == "POST":
        requestObj = request.json
        connection = getMySqlConnection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s',
                           requestObj['email'])
            user = cursor.fetchone()
            if user:
                cursor = connection.cursor()
                cursor.execute('UPDATE users SET password = %s '
                               'WHERE email = %s',
                               (requestObj['newpassword'], requestObj['email']))
                cursor.close()
                return "PASSWORD UPDATED SUCCESSFULLY", StatusCodes.STATUS_OK
            else:
                return "INVALID USER EMAIL", StatusCodes.USER_ALREADY_EXIST
        except pymysql.Error as e:
            return "SOMETHING WENT WRONG " + str(e), StatusCodes.SOMETHING_WENT_WRONG
    else:
        return "METHOD NOT ALLOWED", StatusCodes.METHOD_NOT_ALLOWED


if __name__ == "__main__":
    app.run(host='0.0.0.0')
