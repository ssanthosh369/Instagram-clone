import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
import os

from myuser import MyUser
from userpost import UserPost
from comment import Comment

JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class ExpandComments(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        key = self.request.get('key')
        newKey = ndb.Key(urlsafe=key)
        post = newKey.get()
        img_url= images.get_serving_url(post.image)

        template_values = {
            'key' : key,
            'i' : post,
            'image' : img_url,
        }

        template = JINJA_ENVIRNOMENT.get_template('expandcomments.html')
        self.response.write(template.render(template_values))
