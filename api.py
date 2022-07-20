import os
import sys
from flask import Flask
from flask_restful import Api

sys.path.append(os.path.dirname(__file__))

from web.state import State
from web.intro import Intro
from web.config import ConfigureCKKS
from web.compute import Tests, ComputeAdd, ComputeSubstract, ComputeMean

app = Flask(__name__)
api = Api(app)

api.add_resource(Intro, '/')
api.add_resource(Tests, '/tests')
api.add_resource(ConfigureCKKS, '/configure-ckks')
api.add_resource(ComputeAdd, '/compute-add')
api.add_resource(ComputeSubstract, '/compute-substract')
api.add_resource(ComputeMean, '/compute-mean')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5007, debug=True)
