import cgi
import webapp2
from google.appengine.api import users
from google.appengine.ext import db
import jinja2
import os

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Todo(db.Model):
  text = db.StringProperty()
  createdate = db.DateTimeProperty(auto_now_add=True)
  deletedate = db.DateTimeProperty()

class TodoPage(webapp2.RequestHandler):
  warning = None
  def get(self): # delete request
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    if cgi.escape(self.request.get('op')) == "delete":
      key_name = self.request.get('key')
      key = db.Key(key_name)
      db_key = db.get(key)
      db_key.delete()
      self.redirect('/')
    template_values = {
      'todos': Todo.all(),
      'warning': self.warning,
      }
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

  def post(self): # add request
    # buraya post isleme verileri gelecek
    if cgi.escape(self.request.get('op')) == "add":
      todo = Todo(text = cgi.escape(self.request.get('text')))
      todo.put()
    self.redirect('/')

app = webapp2.WSGIApplication(
  [('/', TodoPage)],
  debug=True)
