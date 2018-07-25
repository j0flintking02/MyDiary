from flask import Flask

app = Flask(__name__)

from api import entries

from api import users