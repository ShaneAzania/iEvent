# __init__.py
import os
from flask import Flask
UPLOAD_FOLDER = '/photographicc_app/static/img/image_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = "shhhhhhush"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER