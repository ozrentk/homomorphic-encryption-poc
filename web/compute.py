import base64
from flask import request
from flask_restful import Resource
import numpy as np
from Pyfhel import Pyfhel, PyCtxt
from web.state import State

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

class ComputeBase(Resource):
  HE = None

  def __init__(self):
    self.HE = State().HE

  def ctxtFromBase64(self, b64):
    s_num = base64.b64decode(b64)
    ctxt = PyCtxt(pyfhel=self.HE, bytestring=s_num)
    return ctxt

  def base64FromCtxt(self, ctxt):
    s_num = ctxt.to_bytes()
    b64 = base64.b64encode(s_num).decode()
    return b64

class ComputeAdd(ComputeBase, Resource):
  def post(self):
    try:
      # Deserialize cyphertext encrypted vectors from base64
      ctxt1 = self.ctxtFromBase64(request.json['n1'])
      ctxt2 = self.ctxtFromBase64(request.json['n2'])

      # Sum vectors
      csum = ctxt1 + ctxt2

      # Serialize cyphertext encrypted vectors to base64
      b64_cres = self.base64FromCtxt(csum)

      return { "message": "calculated", "result": b64_cres }

    except Exception as ex:
      print(f"Error: {ex}")
      return { "message": f"error", "error": ex }

class ComputeSubstract(ComputeBase, Resource):
  def post(self):
    try:
      # Deserialize cyphertext encrypted vectors from base64
      ctxt1 = self.ctxtFromBase64(request.json['n1'])
      ctxt2 = self.ctxtFromBase64(request.json['n2'])

      # Sum vectors
      csum = ctxt1 - ctxt2

      # Serialize cyphertext encrypted vectors to base64
      b64_cres = self.base64FromCtxt(csum)

      return { "message": "calculated", "result": b64_cres }

    except Exception as ex:
      print(f"Error: {ex}")
      return { "message": f"error", "error": ex }

class ComputeMean(ComputeBase, Resource):
  def post(self):
    try:
      # Deserialize cyphertext encrypted vectors from base64
      ctxt1 = self.ctxtFromBase64(request.json['n1'])

      # Sum vectors
      avg = sum(ctxt1) / len(ctxt1)
      #Error!

      # Serialize cyphertext encrypted vectors to base64
      b64_cres = self.base64FromCtxt(avg)

      return { "message": "calculated", "result": b64_cres }

    except Exception as ex:
      print(f"Error: {ex}")
      return { "message": f"error", "error": ex }
