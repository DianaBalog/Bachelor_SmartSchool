from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager



app = Flask(__name__)

app.config['SECRET_KEY'] = 'school'

app.config['MONGO_DBNAME'] = 'Login'
app.config['MONGO_URI'] = 'mongodb+srv://Diana:DianaBalog@clusterschool.xiuru.mongodb.net/SmartSchool?retryWrites=true&w=majority'

app.config['JWT_SECRET_KEY'] = "smart school"  
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 604800

jwt = JWTManager(app)
mongo = PyMongo(app)
