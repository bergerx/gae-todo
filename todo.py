import cgi
import webapp2
from google.appengine.api import users
from google.appengine.ext import db


class Todo(db.Model):
  text = db.StringProperty()
  createdate = db.DateTimeProperty(auto_now_add=True)
  deletedate = db.DateTimeProperty()

class TodoPage(webapp2.RequestHandler):
  warning = None
  def get(self): # delete request
    if cgi.escape(self.request.get('op')) == "delete":
      db.get(db.Key(self.request.get('key'))).delete()
      self.warning = "Removed record!"
    self.view()

  def post(self): # add request
    # buraya post isleme verileri gelecek
    if cgi.escape(self.request.get('op')) == "add":
      todo = Todo(text = cgi.escape(self.request.get('text')))
      todo.put()
      self.warning = "Added record"
    self.view()

  def login(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    return user

  def view(self):
    #user = self.login()
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write("<html><head></head><body>")
    if self.warning:
      self.response.out.write("""<font color="red">%s</font>""" % self.warning)
    todos = Todo.all()
    self.response.out.write("<ul>")
    for todo in todos:
      self.response.out.write("<li>%s "% todo.text)
      self.response.out.write("""<a href="?op=delete&key=%s">(-)</a>""" % str(todo.key()))
    self.response.out.write("</ul>")
    self.response.out.write("""
  <form method="post" action="/">
    <input size="50" name="text" />
    <input type="submit" name="op" value="add">
  </form>""")
    self.response.out.write("</body></html>")

application = webapp2.WSGIApplication(
  [('/', TodoPage)],
  debug=True)
