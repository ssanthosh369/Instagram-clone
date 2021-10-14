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

JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class FollowList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        key = self.request.get('key')
        newKey = ndb.Key(urlsafe=key)
        user = newKey.get()

        follow = self.request.get('type')
        list = []
        if follow == "Following":
            list = user.following
            url = "Users following " + user.email

        elif follow == "Followed":
            list = user.followed
            url = "Users followed by " + user.email


        template_values = {
            'key' : key,
            'list' : list,
            'i' : user,
            'url' : url,
        }

        template = JINJA_ENVIRNOMENT.get_template('followlist.html')
        self.response.write(template.render(template_values))
