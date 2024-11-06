from flask import Flask
from backend.models import db

app=None

def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///house_service.sqlite3"
    app.config['UPLOAD_FOLDER'] = 'static/proofs'
    db.init_app(app)
    app.app_context().push()
    app.debug=True
    print("Household Services app is started")
setup_app()

from backend.controller import *  #take eerything from controller. controller used to divide the length of the app file. can splits common routes etc in controller

if __name__=="__main__":
    app.run(debug=True)