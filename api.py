import base64
import io
import zipfile

import numpy as np
from Pyfhel import Pyfhel, PyCtxt

from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

HE = None

todos = {}

class Intro(Resource):
  def get(self):
      return { 'message': "Hi, server here. What would you like today?" }

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
    
    HE_srv = Pyfhel()
    HE_srv.from_bytes_context(files['ctx'])
    HE_srv.from_bytes_public_key(files['pub'])
    HE_srv.from_bytes_relin_key(files['relin'])
    HE_srv.from_bytes_rotate_key(files['rotate'])

    return { 'message': 'configured' }

class Tests(Resource):
  def get(self):

    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))

    HE = Pyfhel()
    HE.contextGen(scheme='bfv', n=2**14, t_bits=20)
    HE.keyGen()
    HE.relinKeyGen()
    HE.rotateKeyGen()

    integer1 = np.array([n1], dtype=np.int64)
    integer2 = np.array([n2], dtype=np.int64)

    s_context = HE.to_bytes_context()
    s_public_key = HE.to_bytes_public_key()
    s_relin_key = HE.to_bytes_relin_key()
    s_rotate_key = HE.to_bytes_rotate_key()

    ctxt1 = HE.encryptInt(integer1)
    ctxt2 = HE.encryptInt(integer2)

    s_context_b64 = base64.b64encode(s_context)
    s_public_key_b64 = base64.b64encode(s_public_key)
    s_relin_key_b64 = base64.b64encode(s_relin_key)
    s_rotate_key_b64 = base64.b64encode(s_rotate_key)

    ctxt1_b64 = base64.b64encode(ctxt1.to_bytes())
    ctxt2_b64 = base64.b64encode(ctxt2.to_bytes())





    s_context = base64.b64decode(s_context_b64)
    s_public_key = base64.b64decode(s_public_key_b64)
    s_relin_key = base64.b64decode(s_relin_key_b64)
    s_rotate_key = base64.b64decode(s_rotate_key_b64)

    HE_srv = Pyfhel()
    HE_srv.from_bytes_context(s_context)
    HE_srv.from_bytes_public_key(s_public_key)
    HE_srv.from_bytes_relin_key(s_relin_key)
    HE_srv.from_bytes_rotate_key(s_rotate_key)

    ctxt1 = PyCtxt(pyfhel=HE_srv, bytestring=base64.b64decode(ctxt1_b64))
    ctxt2 = PyCtxt(pyfhel=HE_srv, bytestring=base64.b64decode(ctxt2_b64))

    ctxtSum = ctxt1 + ctxt2         # `ctxt1 += ctxt2` for inplace operation
    ctxtSub = ctxt1 - ctxt2         # `ctxt1 -= ctxt2` for inplace operation
    ctxtMul = ctxt1 * ctxt2         # `ctxt1 *= ctxt2` for inplace operation


    # b64 encode/decode again


    resSum = HE.decryptInt(ctxtSum)
    resSub = HE.decryptInt(ctxtSub)
    resMul = HE.decryptInt(ctxtMul)

    res = { "n1": n1, "n2": n2, "sum": int(resSum[0]), "sub": int(resSub[0]), "mul": int(resMul[0]) }

    return res


class TodoSimple(Resource):
  def get(self, todo_id):
    return {todo_id: todos[todo_id]}
    
  def put(self, todo_id):
    todos[todo_id] = request.form['data']
    return {todo_id: todos[todo_id]}

api.add_resource(Intro, '/')
api.add_resource(Tests, '/tests')
api.add_resource(ConfigureCKKS, '/configure-ckks')
api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5007, debug=True)
