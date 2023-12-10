from sqlalchemy.orm.state import InstanceState
from copy import deepcopy
""" turns a class to an array of dictionaries"""
def classToArrayOfDicts (src):
  res = []
  for i in src:
    res.append(classToDict(i))
  return res

def classToDict (src):
  cpy = deepcopy(src)
  obj = {}
  cpy.__dict__.pop("password", None)
  cpy.__dict__.pop("_sa_instance_state", None)
  for j , k in enumerate(cpy.__dict__):
    fieldType = type(cpy.__dict__[k])
    if fieldType is InstanceState:
      obj["id"] = cpy.__dict__[k]
    else :
      obj[k] = cpy.__dict__[k]
  return obj