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

class SearchResults(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('button') == 'Search':
            name = self.request.get('user_name')
            total_query = MyUser.query().fetch()
            query = []
            for i in total_query:
                if name in i.email:
                    query.append(i)

        template_values = {
                'search' : name,
                'total_query' : query,
                'length' : len(query),
        }

        template = JINJA_ENVIRNOMENT.get_template('searchresults.html')
        self.response.write(template.render(template_values))
