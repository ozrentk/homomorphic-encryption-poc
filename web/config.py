import io
import zipfile

from flask import request
from flask_restful import Resource
from Pyfhel import Pyfhel
from web.state import State

class ConfigureCKKS(Resource):
  def post(self):
    bytes = request.files['file'].read()

    files = {}
    try:
      with zipfile.ZipFile(io.BytesIO(bytes)) as thezip:
        for zipinfo in thezip.infolist():
          with thezip.open(zipinfo) as thefile:
            files[zipinfo.filename] = thefile.read()

    except Exception as ex:
      print(f"ZIP extract exception: {ex}")
    
    s = State()
    s.HE = Pyfhel()
    s.HE.from_bytes_context(files['ctx'])
    s.HE.from_bytes_public_key(files['pub'])
    s.HE.from_bytes_relin_key(files['relin'])
    s.HE.from_bytes_rotate_key(files['rotate'])

    return { 'message': 'configured' }
