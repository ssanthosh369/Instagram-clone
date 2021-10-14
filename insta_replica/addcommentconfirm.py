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

class AddCommentConfirm(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        key = self.request.get('key')
        newKey = ndb.Key(urlsafe=key)
        user = newKey.get()

        if self.request.get('button') == 'Add':
            username = users.get_current_user().email()
            comment_text = self.request.get('comment_text')
            newComment = Comment(username = username, comment_text = comment_text)
            post = user.posts[int(self.request.get('index'))].get()
            post.comments.append(newComment)
            post.put()
            user.put()


        template_values = {
            'key' : key,
            'i' : post,
            'index' : len(post.comments) - 1,
        }

        template = JINJA_ENVIRNOMENT.get_template('addcommentconfirm.html')
        self.response.write(template.render(template_values))
