from flask import Flask
from flask_restful import Api
from db import db
from resources.virus_total_stats import VirusTotalAPI

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usr/databases/data.db'
api.add_resource(VirusTotalAPI, '/virusCheckStats/<domain>')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)  # localhost