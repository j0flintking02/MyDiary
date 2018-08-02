from flask import Flask
from flasgger import Swagger
app = Flask(__name__)

Swagger = Swagger(app)

from api import entries

from api import users
