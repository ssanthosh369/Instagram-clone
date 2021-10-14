import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore
import os

from myuser import MyUser
from createpost import CreatePost
from createconfirm import CreateConfirm
from search import Search
from searchresults import SearchResults
from profilepage import ProfilePage
from followlist import FollowList
from addcomment import AddComment
from addcommentconfirm import AddCommentConfirm
from expandcomments import ExpandComments

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back,'

        user = users.get_current_user()
        myuser = None
        timeline = []
        img_url = []

        if user:
            url= users.create_logout_url(self.request.uri)
            url_string = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome new user,'
                myuser = MyUser(id=user.user_id(),email = user.email())
                myuser.put()



        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'

        if myuser != None:
            if myuser.posts:
                for i in reversed(myuser.posts):
                    if len(timeline) > 50:
                        break;
                    elif i.get().created_time != None:
                        timeline.append(i)
            if myuser.followed:
                for i in myuser.followed:
                    if i.get().posts:
                        for j in reversed(i.get().posts):
                            if len(timeline) > 50:
                                break;
                            elif j.get().created_time != None:
                                timeline.append(j)


            for i in timeline:
                img_url.append(images.get_serving_url(blob_key=i.get().image))


                timeline.sort(reverse=True,key=lambda i: i.get().created_time)

        template_values = {
                    'url' : url,
                    'url_string' : url_string,
                    'user' : user,
                    'current_user' : myuser,
                    'welcome' : welcome,
                    'timeline' : timeline,
                    't_length' : len(timeline),
                    'image' : img_url,
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
            ('/',MainPage),
            ('/createpost',CreatePost),
            ('/createconfirm',CreateConfirm),
            ('/search',Search),
            ('/searchresults',SearchResults),
            ('/profilepage',ProfilePage),
            ('/followlist',FollowList),
            ('/addcomment',AddComment),
            ('/addcommentconfirm',AddCommentConfirm),
            ('/expandcomments',ExpandComments)
            ],debug=True)
