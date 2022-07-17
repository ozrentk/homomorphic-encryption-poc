from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class Intro(Resource):
    def get(self):
        return "Hi, server here. What would you like today?"

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}
    
    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(Intro, '/')
api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
