from google.appengine.ext import ndb
from userpost import UserPost

class MyUser(ndb.Model):
    # Attributes of the electric ElectricVehicle
    email = ndb.StringProperty()
    following = ndb.KeyProperty(kind='MyUser',repeated = True)
    followed = ndb.KeyProperty(kind='MyUser',repeated = True)
    posts = ndb.KeyProperty(kind='UserPost', repeated = True)
