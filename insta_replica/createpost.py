import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import os

from myuser import MyUser
from createconfirm import CreateConfirm


JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class CreatePost(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values = {
        'upload_url' : blobstore.create_upload_url('/createconfirm')
        }

        template = JINJA_ENVIRNOMENT.get_template('createpost.html')
        self.response.write(template.render(template_values))

    def post(self):

        if self.request.get('button') == 'Cancel':
            self.redirect('/')
