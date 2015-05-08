#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")


class KalkulatorHandler(BaseHandler):
    def post(self):
        prvo = self.request.get("vnos1")
        drugo = self.request.get("vnos2")
        operacija = self.request.get("operacija")
        if operacija == "+":
            rezultat = int(prvo) + int(drugo)
        elif operacija == "-":
            rezultat = int(prvo) - int(drugo)
        elif operacija == "*":
            rezultat = int(prvo) * int(drugo)
        elif operacija == "/":
            rezultat = int(prvo) / int(drugo)
        params = {"prvo": prvo, "drugo": drugo, "operacija": operacija, "rezultat": rezultat}
        self.render_template("kalkulator.html", params)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/kalkulator', KalkulatorHandler)
], debug=True)
