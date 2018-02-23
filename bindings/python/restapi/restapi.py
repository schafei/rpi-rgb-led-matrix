from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

DISPLAY = { 'text': 'Hello Vikings :-)', 'status': 'on' }

parser = reqparse.RequestParser()
parser.add_argument('text')
parser.add_argument('status')

class Display(Resource):
    def get(self):
        return DISPLAY

    def put(self):
        args = parser.parse_args()
        text = args['text']
        status = args['status']
        if text != None:
            DISPLAY['text'] = text
        if status != None:
            DISPLAY['status'] = status
        return text, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(Display, '/display')

if __name__ == '__main__':
    app.run(debug=True)