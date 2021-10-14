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

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        key = self.request.get('key')
        newKey = ndb.Key(urlsafe=key)
        user = newKey.get()
        myuser_key = ndb.Key('MyUser', users.get_current_user().user_id())
        current_user = myuser_key.get()

        img_url = []

        if self.request.get('button') == 'Follow/Unfollow':

            if myuser_key in user.following:
                follow = []
                followed = []

                for i in user.following:
                    if i != myuser_key:
                        follow.append(i)
                user.following = follow

                for i in current_user.followed:
                    if i != newKey:
                        followed.append(i)
                current_user.followed = followed

            else:
                user.following.append(myuser_key)
                current_user.followed.append(newKey)

            user.put()
            current_user.put()

        for i in reversed(user.posts):
            img_url.append(images.get_serving_url(i.get().image))


        if myuser_key in user.following:
            follower = True

        else:
            follower = False


        template_values = {
            'key' : key,
            'i' : user,
            'following_num' : len(user.following),
            'followed_num' : len(user.followed),
            'image' : img_url,
            'current_user' : users.get_current_user().email(),
            'follower' : follower,
        }

        template = JINJA_ENVIRNOMENT.get_template('profilepage.html')
        self.response.write(template.render(template_values))
