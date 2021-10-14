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

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        template_values = {
        }

        template = JINJA_ENVIRNOMENT.get_template('search.html')
        self.response.write(template.render(template_values))



        # for i in query:
        #         self.response.write(i.name + "  " + i.manufacturer + "  " + str(i.year) + '<br/>')
