import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from datetime import datetime
import os

from myuser import MyUser
from userpost import UserPost

JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class CreateConfirm(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        up = UserPost()
        up.caption = self.request.get('caption')
        upload = self.get_uploads()[0]
        up.image = upload.key()
        now = datetime.now()
        up.created_time = now
        up.put()

        length = len(myuser.posts)
        myuser.posts.append(up.put())
        myuser.put()

        img_url = images.get_serving_url(blob_key=myuser.posts[length].get().image)

        template_values = {
            'user' : myuser,
            'index' : length,
            'image' : img_url
        }

        template = JINJA_ENVIRNOMENT.get_template('createconfirm.html')
        self.response.write(template.render(template_values))
