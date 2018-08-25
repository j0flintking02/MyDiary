from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

Swagger = Swagger(app)

from api import entries

from api import users
