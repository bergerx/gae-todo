import cgi
import webapp2
from google.appengine.api import users
from google.appengine.ext import db
from webapp2_extras import jinja2, sessions

class Todo(db.Model):
  text = db.StringProperty()
  details = db.TextProperty()
  user = db.UserProperty(auto_current_user=True)
  createdate = db.DateTimeProperty(auto_now_add=True)

class BaseHandler(webapp2.RequestHandler):

  @webapp2.cached_property
  def jinja2(self):
    # Returns a Jinja2 renderer cached in the app registry.
    return jinja2.get_jinja2(app=self.app)

  def render_response(self, _template, **context):
    # Renders a template and writes the result to the response.
    rv = self.jinja2.render_template(_template, **context)
    self.response.write(rv)

  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    # Returns a session using the default cookie key.
    return self.session_store.get_session()


class TodoPage(BaseHandler):

  def _add(self):
    todo = Todo(
      text=cgi.escape(self.request.get('text')),
      details=cgi.escape(self.request.get('details')),
    )
    todo.put()
    self.session.add_flash('Added: new note.')
    return self.redirect('/')

  def _delete(self):
    key_name = self.request.get('key')
    key = db.Key(key_name)
    db.get(key).delete()
    self.session.add_flash('Deletedtodo item')
    return self.redirect('/')

  def _list(self):
    todos = Todo.all()
    user = users.get_current_user()
    todos.filter('user =', user)
    template_values = {
      'todos': todos,
      'flashes': self.session.get_flashes(),
      'logout_url': users.create_logout_url('/'),
    }
    return self.render_response('index.html', **template_values)

  def get(self):
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url(self.request.uri))
    if cgi.escape(self.request.get('op')) == "delete":
      return self._delete()
    return self._list()

  def post(self): # add request
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url(self.request.uri))
    if cgi.escape(self.request.get('op')) == "add":
      return self._add()
    return self.redirect('/')

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'hebelek-hopelek-hup',
}

app = webapp2.WSGIApplication(
  [('/', TodoPage)],
  config=config,
  debug=True)
