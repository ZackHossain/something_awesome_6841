import resources

from flask import Flask
from flask_restful import Api
from database.db import initialise

from resources import Tasks

from config import username, password


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@localhost/listener'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialise(app)
api = Api(app)

print("App initialised")

api.add_resource(resources.Tasks, '/tasks', endpoint='tasks')
api.add_resource(resources.Results, '/results', endpoint='results')
api.add_resource(resources.Targets, '/targets', endpoint='targets')
api.add_resource(resources.Targets, '/keys', endpoint='keys')

if __name__ == '__main__':
    app.run(debug=True)
  

#! TODO: Implement target table with specific info & task history