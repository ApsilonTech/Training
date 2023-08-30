from flask import Flask
from flask_assets import Bundle, Environment
from flask_minify import minify


app = Flask(__name__)
app.secret_key = "Webhost@443!"
minify(app=app, html=True, js=True, cssless=True)


css = Bundle('assets/css/main.css', output='assets/css/main.css', filters='cssmin')
assets = Environment(app)
assets.register('main_css', css)