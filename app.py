from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/hello/<string:name>')
class Hello(Resource):
    def get(self, name):
        return {"message": "Welcome, %s!" % name}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)