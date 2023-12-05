from sqlalchemy.orm.state import InstanceState

""" turns a class to an array of dictionaries"""
def classToArrayOfDicts (src):
  res = []
  for i in src:
    res.append(classToDict(i))
  return res

def classToDict (src):
  obj = {}
  src.__dict__.pop("password", None)
  src.__dict__.pop("_sa_instance_state", None)
  for j , k in enumerate(src.__dict__):
    fieldType = type(src.__dict__[k])
    if fieldType is InstanceState:
      obj["id"] = src.__dict__[k]
    else :
      obj[k] = src.__dict__[k]
  return obj