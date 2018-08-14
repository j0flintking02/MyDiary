from flask import Flask
from flasgger import Swagger
from flask_cors import CORS, cross_origin
app = Flask(__name__)

Swagger = Swagger(app)
CORS(app)


from api import entries

from api import users
