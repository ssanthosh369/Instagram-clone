from google.appengine.ext import ndb
from comment import Comment

class UserPost(ndb.Model):
    # Attributes of the electric ElectricVehicle
    caption = ndb.StringProperty()
    image = ndb.BlobKeyProperty()
    created_time = ndb.DateTimeProperty()
    comments = ndb.StructuredProperty(Comment, repeated=True)
