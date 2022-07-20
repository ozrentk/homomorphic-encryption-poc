from flask_restful import Resource

class Intro(Resource):
  def get(self):
      return { 'message': "Hi, server here. What would you like today?" }
