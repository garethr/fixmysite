import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api.urlfetch import fetch, DownloadError

from django.utils import simplejson

from lib import slugify
from models import Site, Issue, Comment

class Index(webapp.RequestHandler):
    """
    Main view for the application.
    """
    def get(self):
        
        query = self.request.get("q")
        
        if not query:
            sites = Site.all()
        else:
            sites = Site.gql("WHERE url=:1", "http://%s" % query)

        context = {
            'sites': sites,
            'query': query,
        }

        # prepare the context for the template
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'index.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))
        
    def post(self):
        
        """
        site = Site(
            name = 'name',
            url = 'http://url.com',            
            slug = 'slug',
        )
        site.put()
        
        issue = Issue(
            title = 'title',
            description = 'description',
            site = site,
        )
        issue.put()
        """

        # get url and then decide if we have a site already or
        # need to create one
        
        
        
        name = self.request.get("name")
        url = self.request.get("url")
        
        try:
            site = Site.gql("WHERE url=:1", url)[0]
        except IndexError:
            
            """
            import sys
            import pdb
            for attr in ('stdin', 'stdout', 'stderr'):
                setattr(sys, attr, getattr(sys, '__%s__' % attr))
            pdb.set_trace()
            """
            
            site = Site(
                name = name,
                url = url,            
                slug = slugify(name),
            )
            site.put()

        title = self.request.get("title")
        description = self.request.get("description")

        issue = Issue(
            title = title,
            description = description,
            site = site,
        )
        issue.put()


        context = {
            'issue': issue,
            'sites': Site.all(),
        }

        # prepare the context for the template
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'index.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))

        
class SiteHandler(webapp.RequestHandler):
    """
    Main view for the application.
    """
    def get(self, slug):

        site = Site.gql("WHERE slug=:1", slug)[0]

        context = {
            'site': site,
        }

        # prepare the context for the template
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'site.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))
        
class IssueHandler(webapp.RequestHandler):
    """
    Main view for the application.
    """
    def get(self, key):

        issue = db.get(key)

        context = {
            'issue': issue,
        }

        # prepare the context for the template
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'issue.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))
        
    def post(self, key):

        issue = db.get(key)

        name = self.request.get("name")
        email = self.request.get("email")
        text = self.request.get("comment")

        comment = Comment(
            name = name,
            email = email,
            comment = text,
            issue = issue,
        )
        comment.put()

        context = {
            'issue': issue,
        }

        # prepare the context for the template
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'issue.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))

class IndexJson(webapp.RequestHandler):
    """
    Main view for the application.
    """
    def get(self):

        sites = Site.all()

        context = {
            'sites': sites,
        }

        sites_for_output = {}
    
        # loop over the sites
        for site in sites:
            # and store each one in the output variable
            site_for_output = {
                "url": site.url,
                "issues": site.issue_set.count(),
            }
            sites_for_output[site.name] = site_for_output
    
        # create the JSON object we're going to return
        json = simplejson.dumps(sites_for_output, sort_keys=False)

        # serve the response with the correct content type
        #self.response.headers['Content-Type'] = 'application/json'
        # write the json to the response
        self.response.out.write(json)

# wire up the views
application = webapp.WSGIApplication([
    ('/', Index),
    ('/sites.json', IndexJson),
    ('/site/([A-Za-z0-9-]+)/?$', SiteHandler),
    ('/issue/([A-Za-z0-9-]+)/?$', IssueHandler),
], debug=True)

def main():
    "Run the application"
    run_wsgi_app(application)

if __name__ == '__main__':
    main()