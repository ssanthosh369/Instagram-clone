from google.appengine.ext import ndb

class Comment(ndb.Model):
    # Attributes of the electric ElectricVehicle
    username = ndb.StringProperty()
    comment_text = ndb.StringProperty()
