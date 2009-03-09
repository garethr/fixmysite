from google.appengine.ext import db

class Site(db.Model):
    name = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    
class Issue(db.Model):
    site = db.ReferenceProperty(Site, required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=True)

class Comment(db.Model):
    issue = db.ReferenceProperty(Issue, required=True)
    name = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    email = db.EmailProperty(required=True)
    comment = db.TextProperty(required=True)